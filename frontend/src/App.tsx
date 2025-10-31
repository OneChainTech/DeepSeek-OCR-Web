import { useState } from 'react';
import { FileUploader } from './components/FileUploader';
import { PromptInput } from './components/PromptInput';
import { FileExplorer } from './components/FileExplorer';
import { FilePreview } from './components/FilePreview';
import { Toaster } from './components/ui/sonner';
import { toast } from 'sonner@2.0.3';
import API_CONFIG from './config/api';

interface FileNode {
  name: string;
  type: 'folder' | 'file';
  fileType?: 'markdown' | 'image' | 'pdf';
  content?: string;
}

const API_BASE_URL = API_CONFIG.BASE_URL;

export default function App() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [uploadedFilePath, setUploadedFilePath] = useState<string>('');
  const [prompt, setPrompt] = useState('<image>\n<|grounding|>Convert the document to markdown.');
  const [isProcessing, setIsProcessing] = useState(false);
  const [taskId, setTaskId] = useState<string>('');
  const [resultDir, setResultDir] = useState<string>('');
  const [parseCompleted, setParseCompleted] = useState(false);
  const [selectedPreviewFile, setSelectedPreviewFile] = useState<any>(null);
  const [isPreviewExpanded, setIsPreviewExpanded] = useState(false);

  const handleFileChange = async (file: File | null) => {
    setUploadedFile(file);
    // Reset states when file is deleted
    if (!file) {
      setParseCompleted(false);
      setSelectedPreviewFile(null);
      setIsProcessing(false);
      setUploadedFilePath('');
      setTaskId('');
      setResultDir('');
    } else {
      // Upload file to backend
      try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${API_BASE_URL}/api/upload`, {
          method: 'POST',
          body: formData,
        });
        
        const data = await response.json();
        if (data.status === 'success') {
          setUploadedFilePath(data.file_path);
          toast.success('文件上传成功', {
            description: `已上传 ${file.name}`,
          });
        } else {
          toast.error('文件上传失败');
        }
      } catch (error) {
        console.error('Upload error:', error);
        toast.error('文件上传失败', {
          description: '无法连接到后端服务',
        });
      }
    }
  };

  const handleStartParsing = async () => {
    if (!uploadedFilePath) {
      toast.error('请先上传文件');
      return;
    }

    setIsProcessing(true);
    setParseCompleted(false);
    setResultDir('');

    try {
      const response = await fetch(`${API_BASE_URL}/api/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          file_path: uploadedFilePath,
          prompt: prompt,
        }),
      });

      const data = await response.json();
      if (data.status === 'running' && data.task_id) {
        setTaskId(data.task_id);
        
        let isTaskFinished = false;
        
        // Poll for completion from backend
        const pollInterval = setInterval(async () => {
          try {
            const progressRes = await fetch(`${API_BASE_URL}/api/progress/${data.task_id}`);
            const progressData = await progressRes.json();
            
            if (progressData.status === 'success' && progressData.state === 'finished') {
              isTaskFinished = true;
              clearInterval(pollInterval);
              setIsProcessing(false);
              
              // Fetch result
              const resultRes = await fetch(`${API_BASE_URL}/api/result/${data.task_id}`);
              const resultData = await resultRes.json();
              
              if (resultData.status === 'success' && resultData.state === 'finished') {
                setResultDir(resultData.result_dir);
                setParseCompleted(true);
                toast.success('解析完成！', {
                  description: '已经顺利完成解析',
                });
              }
            }
          } catch (error) {
            console.error('Progress poll error:', error);
          }
        }, 2000); // Poll every 2 seconds
      } else {
        toast.error('启动解析任务失败');
        setIsProcessing(false);
      }
    } catch (error) {
      console.error('Parse error:', error);
      toast.error('解析失败', {
        description: '无法连接到后端服务',
      });
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-teal-50">
      <Toaster position="top-right" />
      
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-gray-200 shadow-sm sticky top-0 z-10">
        <div className="container mx-auto px-8 py-4 flex items-center justify-center">
          <h1 className="text-center text-2xl text-transparent bg-clip-text bg-gradient-to-r from-teal-600 to-cyan-600 font-semibold">
            DeepSeek OCR
          </h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-8 py-6">
        <div className="grid grid-cols-2 gap-6 h-[calc(100vh-120px)]">
          {/* Left Panel - File Upload */}
          <div className="flex flex-col min-h-0">
            <FileUploader onFileChange={handleFileChange} />
          </div>

          {/* Right Panel - Results */}
          <div className="flex flex-col gap-4 min-h-0">
            {/* Prompt Input and File Explorer in Tabs */}
            <div 
              className={`flex gap-4 flex-shrink-0 transition-all duration-300 overflow-hidden ${
                isPreviewExpanded ? 'h-0 opacity-0' : 'h-[280px] opacity-100'
              }`}
            >
              <div className="flex-1 min-h-0">
                <PromptInput
                  prompt={prompt}
                  onPromptChange={setPrompt}
                  onParse={handleStartParsing}
                  isProcessing={isProcessing}
                  hasFile={!!uploadedFile}
                  isCompact={isPreviewExpanded}
                />
              </div>
              <div className="w-[320px] min-h-0">
                <FileExplorer
                  onFileSelect={setSelectedPreviewFile}
                  selectedFile={selectedPreviewFile}
                  parseCompleted={parseCompleted}
                  resultDir={resultDir}
                />
              </div>
            </div>

            {/* File Preview */}
            <div className="flex-1 min-h-0">
              <FilePreview 
                file={selectedPreviewFile}
                isExpanded={isPreviewExpanded}
                onToggleExpand={() => setIsPreviewExpanded(!isPreviewExpanded)}
              />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
