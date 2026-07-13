import { UploadCloud, ShieldCheck } from 'lucide-react';

export default function UploadPage() {
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold text-slate-900 m-0">Upload Dataset</h1>
        <p className="text-slate-500 mt-1">Import your CSV or Excel spreadsheets to trigger immediate analytics.</p>
      </div>

      <div className="border-2 border-dashed border-slate-300 hover:border-blue-500 bg-white rounded-xl p-12 text-center transition-colors cursor-pointer group shadow-sm">
        <div className="space-y-4">
          <div className="w-16 h-16 bg-slate-50 group-hover:bg-blue-50 text-slate-400 group-hover:text-blue-500 rounded-full flex items-center justify-center mx-auto transition-colors">
            <UploadCloud size={32} />
          </div>
          <div>
            <p className="text-lg font-semibold text-slate-800">
              Drag & drop your file here, or <span className="text-blue-600 font-bold group-hover:underline">browse</span>
            </p>
            <p className="text-sm text-slate-400 mt-1">Supports CSV, XLS, XLSX formats (Max 50MB)</p>
          </div>
        </div>
      </div>

      <div className="bg-slate-50 rounded-xl p-6 border border-slate-200 flex items-start gap-4">
        <div className="p-2 bg-emerald-50 text-emerald-600 rounded-lg shrink-0">
          <ShieldCheck size={20} />
        </div>
        <div className="space-y-1">
          <h4 className="font-semibold text-slate-800 text-sm">Security & Privacy First</h4>
          <p className="text-xs text-slate-500 leading-relaxed">
            Your data is encrypted during transfer, processed locally using native statistical modules, and stored temporarily inside your active workspace session. We do not use your proprietary dataset details to train general models.
          </p>
        </div>
      </div>
    </div>
  );
}
