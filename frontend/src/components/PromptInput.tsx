import { Textarea } from './ui/textarea';
import { Button } from './ui/button';
import { Sparkles, Loader2, FileText, Rows, ScanText, ChartLine, Image, Target } from 'lucide-react';
import { ScrollArea } from './ui/scroll-area';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from './ui/select';

const PROMPT_TEMPLATES = [
  {
    key: 'doc-markdown',
    label: '文档转 Markdown',
    prompt: '<image>\n<|grounding|>Convert the document to markdown.',
    icon: FileText,
  },
  {
    key: 'general-ocr',
    label: '通用 OCR',
    prompt: '<image>\n<|grounding|>OCR this image.',
    icon: ScanText,
  },
  {
    key: 'free-ocr',
    label: '无布局提取',
    prompt: '<image>\nFree OCR.',
    icon: Rows,
  },
  {
    key: 'chart-parse',
    label: '图表解析',
    prompt: '<image>\nParse the figure.',
    icon: ChartLine,
  },
  {
    key: 'image-desc',
    label: '图像描述',
    prompt: '<image>\nDescribe this image in detail.',
    icon: Image,
  },
  {
    key: 'text-locate',
    label: '文本定位',
    prompt: '<image>\nLocate <|ref|>特定文字<|/ref|> in the image.',
    icon: Target,
  },
] as const;

interface PromptInputProps {
  prompt: string;
  onPromptChange: (value: string) => void;
  onParse: () => void;
  isProcessing: boolean;
  hasFile: boolean;
  isCompact?: boolean;
}

export function PromptInput({
  prompt,
  onPromptChange,
  onParse,
  isProcessing,
  hasFile,
  isCompact = false,
}: PromptInputProps) {
  return (
    <div className="h-full flex flex-col min-h-0">
      <div className="bg-white/50 backdrop-blur-sm rounded-xl border border-gray-200 shadow-lg p-4 mb-3 flex-1 flex flex-col min-h-0">
        <div className="flex flex-col gap-2 mb-2 flex-shrink-0">
          <label className="block text-sm text-gray-600">提示词输入</label>
          <Select
            defaultValue={PROMPT_TEMPLATES[0].key}
            onValueChange={(value) => {
              const template = PROMPT_TEMPLATES.find((item) => item.key === value);
              if (template) {
                onPromptChange(template.prompt);
              }
            }}
          >
            <SelectTrigger className="w-full sm:w-64 bg-white data-[state=open]:border-teal-300 data-[state=open]:shadow-[0_16px_40px_-22px_rgba(15,118,110,0.6)]">
              <SelectValue
                placeholder="选择提示词示例"
                renderValue={(value) => {
                  const current = PROMPT_TEMPLATES.find((item) => item.key === value);
                  const Icon = current?.icon;
                  return current ? (
                    <span className="flex items-center gap-2 text-gray-800">
                      {Icon && <Icon className="h-4 w-4 text-teal-500" />}
                      <span className="font-medium">{current.label}</span>
                    </span>
                  ) : (
                    value || ''
                  );
                }}
              />
            </SelectTrigger>
            <SelectContent className="bg-white text-gray-900">
              {PROMPT_TEMPLATES.map((item) => (
                <SelectItem key={item.key} value={item.key}>
                  <div className="flex items-center gap-2">
                    <item.icon className="h-4 w-4 text-teal-500" />
                    <span className="font-medium text-gray-700">{item.label}</span>
                  </div>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="flex-1 min-h-0">
          <ScrollArea className="h-full w-full">
            <Textarea
              value={prompt}
              onChange={(e) => onPromptChange(e.target.value)}
              className={`w-full bg-white/80 border-gray-200 focus:border-teal-400 focus:ring-teal-400 resize-none ${
                isCompact ? 'min-h-[40px]' : 'min-h-[100px]'
              }`}
              placeholder="输入您的提示词..."
            />
          </ScrollArea>
        </div>
      </div>

      {!isCompact && (
        <div className="h-11 flex-shrink-0">
          <Button
            onClick={onParse}
            disabled={!hasFile || isProcessing}
            className="w-full h-full bg-gradient-to-r from-teal-500 to-cyan-500 hover:from-teal-600 hover:to-cyan-600 text-white shadow-lg disabled:opacity-50 disabled:from-gray-300 disabled:to-gray-400 transition-all hover:shadow-xl hover:scale-[1.02] cursor-pointer disabled:cursor-not-allowed"
          >
            {isProcessing ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                解析中...
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-5 w-5" />
                开始解析
              </>
            )}
          </Button>
        </div>
      )}
    </div>
  );
}
