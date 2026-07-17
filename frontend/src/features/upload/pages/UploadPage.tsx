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
          
          {/* Universal Ingestion Validation Report */}
          {selectedFile.columnMetadata?.validation_report && (
            <div className="mt-6 border-t border-slate-100 pt-6 space-y-4 text-left">
              <div className="flex items-center justify-between">
                <h4 className="text-xs font-semibold text-slate-800 uppercase tracking-wider m-0">Ingestion & Validation Report</h4>
                <span className="text-[10px] px-2.5 py-0.5 bg-emerald-50 text-emerald-700 font-bold rounded-full border border-emerald-100 uppercase tracking-wide">
                  {selectedFile.columnMetadata.validation_report.validation_status}
                </span>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 bg-slate-50 rounded-xl p-4 text-xs">
                <div>
                  <span className="text-slate-400 font-bold block uppercase tracking-wider text-[9px]">Encoding</span>
                  <span className="font-semibold text-slate-700 block mt-1 uppercase">
                    {selectedFile.columnMetadata.validation_report.encoding || 'N/A'}
                  </span>
                </div>
                <div>
                  <span className="text-slate-400 font-bold block uppercase tracking-wider text-[9px]">Delimiter</span>
                  <span className="font-semibold text-slate-700 block mt-1">
                    {selectedFile.columnMetadata.validation_report.delimiter === '\t' ? 'Tab (\\t)' : 
                     selectedFile.columnMetadata.validation_report.delimiter === ',' ? 'Comma (,)' : 
                     selectedFile.columnMetadata.validation_report.delimiter === ';' ? 'Semicolon (;)' : 
                     selectedFile.columnMetadata.validation_report.delimiter === '|' ? 'Pipe (|)' : 
                     selectedFile.columnMetadata.validation_report.delimiter || 'N/A'}
                  </span>
                </div>
                <div>
                  <span className="text-slate-400 font-bold block uppercase tracking-wider text-[9px]">Header State</span>
                  <span className="font-semibold text-slate-700 block mt-1">
                    {selectedFile.columnMetadata.validation_report.header_detected ? 'Header Detected' : 'Headerless (Recovered)'}
                  </span>
                </div>
                <div>
                  <span className="text-slate-400 font-bold block uppercase tracking-wider text-[9px]">Completeness</span>
                  <span className="font-semibold text-slate-700 block mt-1">
                    {selectedFile.columnMetadata.validation_report.missing_values?.completeness_score ?? 100}%
                  </span>
                </div>
              </div>

              {/* Inferred Types Panel */}
              <div>
                <span className="text-[10px] text-slate-400 font-bold uppercase tracking-wider block mb-2">Inferred Column Types</span>
                <div className="flex flex-wrap gap-2 max-h-36 overflow-y-auto p-1">
                  {Object.entries(selectedFile.columnMetadata.validation_report.inferred_types || {}).map(([col, type]: [any, any]) => (
                    <div key={col} className="flex items-center gap-1.5 px-2 py-0.5 bg-white border border-slate-200 rounded-lg text-xs">
                      <span className="font-medium text-slate-700 text-[11px]">{col}:</span>
                      <span className="text-blue-600 font-bold text-[9px] uppercase bg-blue-50 px-1 py-0.5 rounded tracking-wide">
                        {type}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Warnings and Fixes */}
              {((selectedFile.columnMetadata.validation_report.warnings && selectedFile.columnMetadata.validation_report.warnings.length > 0) ||
                (selectedFile.columnMetadata.validation_report.recommended_fixes && selectedFile.columnMetadata.validation_report.recommended_fixes.length > 0)) && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                  {selectedFile.columnMetadata.validation_report.warnings.length > 0 && (
                    <div className="bg-amber-50/50 border border-amber-100 rounded-xl p-4 text-xs space-y-2">
                      <span className="text-amber-800 font-bold uppercase tracking-wider block text-[9px]">Ingestion Warnings</span>
                      <ul className="list-disc pl-4 space-y-1 text-amber-700 m-0">
                        {selectedFile.columnMetadata.validation_report.warnings.map((w: string, i: number) => (
                          <li key={i}>{w}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {selectedFile.columnMetadata.validation_report.recommended_fixes.length > 0 && (
                    <div className="bg-blue-50/50 border border-blue-100 rounded-xl p-4 text-xs space-y-2">
                      <span className="text-blue-800 font-bold uppercase tracking-wider block text-[9px]">Auto-Applied Normalizations</span>
                      <ul className="list-disc pl-4 space-y-1 text-blue-700 m-0">
                        {selectedFile.columnMetadata.validation_report.recommended_fixes.map((f: string, i: number) => (
                          <li key={i}>{f}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

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
