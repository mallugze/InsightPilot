import { apiFetch } from './api';

export interface UploadResponse {
  success: boolean;
  datasetId: string;
  fileName: string;
  fileSize: string;
  format: 'csv' | 'excel';
  rowsCount: number;
  colsCount: number;
  estimatedProcessingTimeSeconds: number;
  message: string;
  datasetType?: string;
  missingValues?: number;
  duplicates?: number;
  qualityScore?: number;
  preview?: any[];
  columnMetadata?: any;
}

/**
 * Uploads a spreadsheet dataset to the active session workspace.
 * @endpoint POST /api/v1/upload
 * @headers X-Session-ID
 */
export const uploadDatasetFile = async (
  file: File, 
  sessionId: string
): Promise<UploadResponse> => {
  console.log('[API Request] POST /api/v1/upload', {
    fileName: file.name,
    fileSize: file.size,
    sessionId
  });

  const formData = new FormData();
  formData.append('file', file);

  const response = await apiFetch<any>('/v1/upload', {
    method: 'POST',
    body: formData,
  });

  const extension = file.name.split('.').pop()?.toLowerCase();
  const format = extension === 'csv' ? 'csv' : 'excel';
  
  // Calculate estimation: 1 second per 250 rows, minimum 2 seconds
  const estTime = Math.max(2, Math.ceil(response.rows / 250));

  return {
    success: response.status === 'success' || response.status === 'READY' || !!response.dataset_id,
    datasetId: String(response.dataset_id),
    fileName: file.name,
    fileSize: `${(file.size / (1024 * 1024)).toFixed(2)} MB`,
    format,
    rowsCount: response.rows,
    colsCount: response.columns,
    estimatedProcessingTimeSeconds: estTime,
    message: 'File successfully received, parsed, and validated.',
    datasetType: response.dataset_type,
    missingValues: response.missing_values,
    duplicates: response.duplicates,
    qualityScore: response.quality_score,
    preview: response.preview,
    columnMetadata: response.column_metadata,
  };
};
