import { MessageSquareCode, Send } from 'lucide-react';

export default function ChatPage() {
  return (
    <div className="h-[calc(100vh-10rem)] flex flex-col space-y-4">
      <div>
        <h1 className="text-3xl font-bold text-slate-900 m-0">AI Analyst</h1>
        <p className="text-slate-500 mt-1">Ask questions, request calculations, or discover hidden correlations.</p>
      </div>

      <div className="flex-1 bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col overflow-hidden">
        {/* Chat Stream Panel */}
        <div className="flex-1 p-6 overflow-y-auto flex flex-col items-center justify-center text-center text-slate-400">
          <div className="max-w-xs space-y-3">
            <MessageSquareCode size={48} className="mx-auto text-slate-300" />
            <h3 className="font-semibold text-slate-700 text-base">Start the Conversation</h3>
            <p className="text-sm text-slate-500">
              Upload a dataset first. Once loaded, you can run custom queries, ask for trends, or test recommendations.
            </p>
          </div>
        </div>

        {/* Input Controls */}
        <div className="p-4 border-t border-slate-100 bg-slate-50 flex gap-3">
          <input
            type="text"
            placeholder="Ask a question about your data..."
            disabled
            className="flex-1 bg-white border border-slate-200 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-blue-500 disabled:bg-slate-100 disabled:text-slate-400"
          />
          <button
            disabled
            className="px-4 py-2 bg-slate-300 text-slate-600 font-semibold text-sm rounded-lg flex items-center justify-center cursor-not-allowed"
          >
            <Send size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}
