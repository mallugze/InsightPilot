/**
 * Dataset Upload API Service Contract for InsightPilot
 * Target Backend: FastAPI
 */

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
}

/**
 * Uploads a spreadsheet dataset to the active session workspace.
 * @endpoint POST /api/v1/datasets/upload
 * @headers X-Session-ID
 */
export const uploadDatasetFile = async (
  file: File, 
  sessionId: string
): Promise<UploadResponse> => {
  console.log('[API Request] POST /api/v1/datasets/upload', {
    fileName: file.name,
    fileSize: file.size,
    sessionId
  });

  // Simulated server upload delay
  await new Promise((resolve) => setTimeout(resolve, 800));

  const extension = file.name.split('.').pop()?.toLowerCase();
  const format = extension === 'csv' ? 'csv' : 'excel';
  const isSales = file.name.toLowerCase().includes('sales');

  return {
    success: true,
    datasetId: `ds_${Math.random().toString(36).substr(2, 9)}`,
    fileName: file.name,
    fileSize: `${(file.size / (1024 * 1024)).toFixed(1)} MB`,
    format,
    rowsCount: isSales ? 1240 : 850,
    colsCount: isSales ? 12 : 8,
    estimatedProcessingTimeSeconds: isSales ? 6 : 4,
    message: 'File successfully received and validated.',
  };
};
