import React, { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useWorkspace } from '../../../context/WorkspaceContext';
import { UploadCloud, ShieldCheck, FileSpreadsheet, Play, RefreshCw, AlertCircle } from 'lucide-react';
import { Card } from '../../../components/ui/Card';
import { Button } from '../../../components/ui/Button';

import { getOrCreateSessionId } from '../../../utils/storage';
import { uploadDatasetFile } from '../../../services/upload';

interface SelectedFileMetadata {
  name: string;
  size: string;
  type: string;
  rowsCount: number;
  colsCount: number;
  estimatedTime: string;
  datasetId?: string;
  datasetType?: string;
  missingValues?: number;
  duplicates?: number;
  qualityScore?: number;
  preview?: any[];
  columnMetadata?: any;
}

export default function UploadPage() {
  const { startUpload } = useWorkspace();
  const navigate = useNavigate();
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const [selectedFile, setSelectedFile] = useState<SelectedFileMetadata | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileUpload = async (file: File) => {
    setValidationError(null);
    setSelectedFile(null);
    
    const extension = file.name.split('.').pop()?.toLowerCase();
    if (!['csv', 'xls', 'xlsx'].includes(extension || '')) {
      setValidationError('Unsupported file format. Please upload a CSV or Excel spreadsheet (.csv, .xls, .xlsx).');
      return;
    }

    if (file.size > 50 * 1024 * 1024) {
      setValidationError('File is too large. Max supported size is 50MB.');
      return;
    }

    setIsUploading(true);
    try {
      const sessionId = getOrCreateSessionId();
      const response = await uploadDatasetFile(file, sessionId);
      
      if (response.success) {
        setSelectedFile({
          name: response.fileName,
          size: response.fileSize,
          type: response.format === 'csv' ? 'CSV Dataset' : 'Excel Workbook',
          rowsCount: response.rowsCount,
          colsCount: response.colsCount,
          estimatedTime: `${response.estimatedProcessingTimeSeconds} seconds`,
          datasetId: response.datasetId,
          datasetType: response.datasetType,
          missingValues: response.missingValues,
          duplicates: response.duplicates,
          qualityScore: response.qualityScore,
          preview: response.preview,
          columnMetadata: response.columnMetadata,
        });
      } else {
        setValidationError(response.message || 'Upload failed during validation.');
      }
    } catch (err: any) {
      console.error(err);
      setValidationError(err.message || 'An error occurred while uploading the file.');
    } finally {
      setIsUploading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileUpload(file);
    }
  };

  const triggerBrowse = (e: React.MouseEvent) => {
    e.stopPropagation();
    fileInputRef.current?.click();
  };

  const handleStartAnalysis = () => {
    if (selectedFile) {
      startUpload({
        fileName: selectedFile.name,
        fileSize: selectedFile.size,
        datasetId: selectedFile.datasetId,
        datasetType: selectedFile.datasetType,
        rowsCount: selectedFile.rowsCount,
        colsCount: selectedFile.colsCount,
        missingValues: selectedFile.missingValues,
        duplicates: selectedFile.duplicates,
        qualityScore: selectedFile.qualityScore,
        preview: selectedFile.preview,
        columnMetadata: selectedFile.columnMetadata,
      });
      navigate('/analysis-progress');
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setValidationError(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto pt-8 text-left px-margin-page pb-section-gap">
      <div>
        <h1 className="text-3xl font-bold text-slate-900 m-0">Upload Dataset</h1>
        <p className="text-slate-500 mt-1">Import your CSV or Excel spreadsheets to trigger immediate analytics.</p>
      </div>

      <input 
        type="file" 
        ref={fileInputRef} 
        onChange={handleFileChange} 
        accept=".csv,.xls,.xlsx" 
        className="hidden" 
      />

      {/* Stage 1: File Selector Dropzone */}
      {!selectedFile && !isUploading && (
        <Card 
          onClick={triggerBrowse}
          className="border-2 border-dashed border-slate-300 hover:border-blue-500 bg-white rounded-xl p-12 text-center transition-colors cursor-pointer group shadow-sm"
        >
          <div className="space-y-4">
            <div className="w-16 h-16 bg-slate-50 group-hover:bg-blue-50 text-slate-400 group-hover:text-blue-500 rounded-full flex items-center justify-center mx-auto transition-colors">
              <UploadCloud size={32} />
            </div>
            <div>
              <p className="text-lg font-semibold text-slate-800 m-0">
                Drag & drop your file here, or{' '}
                <span className="text-blue-600 font-bold group-hover:underline">browse</span>
              </p>
              <p className="text-sm text-slate-400 mt-1.5 m-0">Supports CSV, XLS, XLSX formats (Max 50MB)</p>
            </div>
          </div>
        </Card>
      )}

      {/* Uploading Progress Loader */}
      {isUploading && (
        <Card className="border border-slate-200 bg-white rounded-xl p-12 text-center shadow-sm">
          <div className="space-y-4">
            <div className="w-16 h-16 bg-blue-50 text-blue-500 rounded-full flex items-center justify-center mx-auto animate-spin">
              <RefreshCw size={32} />
            </div>
            <div>
              <p className="text-lg font-semibold text-slate-800 m-0 animate-pulse">Uploading and profiling dataset...</p>
              <p className="text-sm text-slate-400 mt-1.5 m-0">FastAPI is validating headers and running statistical checks.</p>
            </div>
          </div>
        </Card>
      )}

      {/* Format Validation Error Message */}
      {validationError && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl flex items-start gap-3 text-sm">
          <AlertCircle className="shrink-0 mt-0.5" size={16} />
          <p className="m-0 font-medium">{validationError}</p>
        </div>
      )}

      {/* Stage 2 & 3: Selected File Preview Metadata Table */}
      {selectedFile && (
        <Card className="bg-white rounded-xl p-8 border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center gap-3 border-b border-slate-100 pb-4">
            <div className="w-10 h-10 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
              <FileSpreadsheet size={20} />
            </div>
            <div className="text-left">
              <h3 className="font-semibold text-slate-800 text-base m-0 leading-tight">
                {selectedFile.name}
              </h3>
              <span className="text-xs text-slate-400 font-bold mt-1 inline-block uppercase tracking-wider">
                Ready for AI Processing
              </span>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-6 text-sm">
            <div className="flex flex-col">
              <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">File Type</span>
              <span className="font-medium text-slate-800 mt-1">{selectedFile.type}</span>
            </div>
            <div className="flex flex-col">
              <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">File Size</span>
              <span className="font-medium text-slate-800 mt-1">{selectedFile.size}</span>
            </div>
            <div className="flex flex-col">
              <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">Estimated Ingestion</span>
              <span className="font-medium text-slate-800 mt-1">{selectedFile.estimatedTime}</span>
            </div>
            <div className="flex flex-col">
              <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">Rows Detected</span>
              <span className="font-medium text-slate-800 mt-1">{selectedFile.rowsCount.toLocaleString()}</span>
            </div>
            <div className="flex flex-col">
              <span className="text-xs text-slate-400 font-bold uppercase tracking-wider">Columns Detected</span>
              <span className="font-medium text-slate-800 mt-1">{selectedFile.colsCount}</span>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-100 flex flex-col sm:flex-row gap-3">
            <Button
              onClick={handleStartAnalysis}
              className="flex-1 bg-primary text-on-primary py-2.5 px-4 rounded-lg font-semibold hover:bg-inverse-surface transition-all flex items-center justify-center gap-2 cursor-pointer"
            >
              <Play size={16} />
              Start Analysis
            </Button>
            <Button
              onClick={handleReset}
              className="bg-transparent border border-outline-variant text-slate-600 hover:text-slate-900 py-2.5 px-4 rounded-lg font-semibold hover:bg-slate-50 transition-all flex items-center justify-center gap-2 cursor-pointer"
            >
              <RefreshCw size={16} />
              Change File
            </Button>
          </div>
        </Card>
      )}

      {/* Safety & Compliance Disclaimer banner */}
      <div className="bg-slate-50 rounded-xl p-6 border border-slate-200 flex items-start gap-4">
        <div className="p-2 bg-emerald-50 text-emerald-600 rounded-lg shrink-0">
          <ShieldCheck size={20} />
        </div>
        <div className="space-y-1 text-left">
          <h4 className="font-semibold text-slate-800 text-sm m-0">Security & Privacy First</h4>
          <p className="text-xs text-slate-500 leading-relaxed m-0 mt-1">
            Your data is encrypted during transfer, processed locally using native statistical modules, and stored temporarily inside your active workspace session. We do not use your proprietary dataset details to train general models.
          </p>
        </div>
      </div>
    </div>
  );
}
