import React, { useState } from 'react';
import { useWorkspace } from '../../../context/WorkspaceContext';
import { Button } from '../../../components/ui/Button';
import { Card } from '../../../components/ui/Card';
import { KeyRound, ShieldAlert } from 'lucide-react';

export default function VerifyEmailPage() {
  const { verifyEmailCode, profile } = useWorkspace();
  const [code, setCode] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (code.trim().length !== 6) {
      setError('Please enter a 6-digit verification code');
      return;
    }

    setLoading(true);
    setError('');

    // Wait slightly to simulate API latency
    const success = await verifyEmailCode(code.trim());
    setLoading(false);

    if (!success) {
      setError('Invalid verification code. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-background flex flex-col justify-center items-center px-4 antialiased selection:bg-secondary-fixed selection:text-on-secondary-fixed">
      <Card className="w-full max-w-md bg-white border border-outline-variant rounded-2xl p-8 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)] flex flex-col text-left">
        {/* Header Icon */}
        <div className="flex items-center gap-2 mb-6">
          <div className="w-8 h-8 rounded bg-primary text-white flex items-center justify-center font-bold text-sm shrink-0">
            <KeyRound size={16} />
          </div>
          <span className="font-display text-xl font-bold tracking-tighter text-primary">Email Verification</span>
        </div>

        {/* Title Group */}
        <div className="space-y-2 mb-8 text-left">
          <h1 className="font-display text-2xl font-bold text-primary m-0 tracking-tight">
            Verify your Email
          </h1>
          <p className="font-sans text-sm text-on-surface-variant leading-relaxed m-0">
            We sent a verification code to <span className="font-semibold text-slate-800">{profile?.email}</span>.
          </p>
        </div>

        {/* Verification Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="space-y-1.5">
            <label htmlFor="code" className="font-display text-xs font-semibold text-on-surface uppercase tracking-wider block">
              6-Digit Verification Code <span className="text-red-500">*</span>
            </label>
            <input
              id="code"
              type="text"
              maxLength={6}
              value={code}
              onChange={(e) => {
                const val = e.target.value.replace(/\D/g, ''); // Numeric only
                setCode(val);
                if (val.length === 6) setError('');
              }}
              placeholder="123456"
              className={`w-full bg-surface border rounded-lg px-4 py-2.5 text-center text-lg font-mono tracking-widest focus:outline-none focus:ring-2 transition-all ${
                error 
                  ? 'border-red-500 focus:ring-red-100 focus:border-red-500' 
                  : 'border-outline-variant focus:ring-secondary/10 focus:border-secondary'
              }`}
            />
            {error && (
              <p className="text-xs text-red-600 font-semibold m-0">
                {error}
              </p>
            )}
          </div>

          {/* Action Trigger */}
          <Button
            type="submit"
            disabled={loading}
            className="w-full bg-primary text-on-primary py-3 rounded-lg font-label-md text-label-md font-semibold hover:bg-inverse-surface transition-all flex items-center justify-center gap-2 cursor-pointer mt-4"
          >
            {loading ? 'Verifying...' : 'Verify & Continue'}
          </Button>
        </form>

        {/* Architecture Note */}
        <div className="mt-6 bg-slate-50 border border-slate-200 rounded-xl p-4 flex gap-3 text-left">
          <ShieldAlert className="text-slate-500 shrink-0" size={18} />
          <div>
            <h5 className="font-semibold text-slate-700 text-xs m-0">Sprint 4 Architecture Mode</h5>
            <p className="text-xs text-slate-500 m-0 mt-1 leading-relaxed">
              Email delivery is stubbed. For verification testing, please enter any 6-digit sequence.
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}
