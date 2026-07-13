import { FileSpreadsheet } from 'lucide-react';

export default function ReportsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-slate-900 m-0">Executive Reports</h1>
        <p className="text-slate-500 mt-1">Compile executive summaries and statistical briefs into downloadable PDF files.</p>
      </div>

      <div className="bg-white rounded-xl p-8 border border-slate-200 shadow-sm flex flex-col items-center justify-center text-center min-h-[400px]">
        <div className="max-w-md space-y-4">
          <div className="w-16 h-16 bg-slate-50 text-slate-400 rounded-full flex items-center justify-center mx-auto">
            <FileSpreadsheet size={28} />
          </div>
          <h2 className="text-xl font-semibold text-slate-800">No Reports Available</h2>
          <p className="text-slate-500">
            Generate an executive brief by uploading your dataset and completing your first workspace analysis.
          </p>
        </div>
      </div>
    </div>
  );
}
