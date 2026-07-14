import React, { useState, useEffect } from 'react';
import { useWorkspace } from '../../../context/WorkspaceContext';
import { Button } from '../../../components/ui/Button';
import { Card } from '../../../components/ui/Card';
import { User, CheckCircle2, AlertCircle } from 'lucide-react';

export default function WelcomePage() {
  const { saveProfile } = useWorkspace();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [companyName, setCompanyName] = useState('');
  
  // Validation States
  const [fullNameError, setFullNameError] = useState<string | null>(null);
  const [emailError, setEmailError] = useState<string | null>(null);
  
  const [emailTouched, setEmailTouched] = useState(false);
  const [isEmailValid, setIsEmailValid] = useState(false);

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  // Real-time email validation
  useEffect(() => {
    if (!email.trim()) {
      setIsEmailValid(false);
      if (emailTouched) {
        setEmailError('Please enter a valid email address.');
      }
    } else if (!emailRegex.test(email.trim())) {
      setIsEmailValid(false);
      if (emailTouched) {
        setEmailError('Please enter a valid email address.');
      }
    } else {
      setIsEmailValid(true);
      setEmailError(null);
    }
  }, [email, emailTouched]);

  const handleEmailBlur = () => {
    setEmailTouched(true);
  };

  const handleFullNameChange = (val: string) => {
    setFullName(val);
    if (val.trim()) {
      setFullNameError(null);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Final verification before submit
    let isValid = true;
    if (!fullName.trim()) {
      setFullNameError('Full Name is required');
      isValid = false;
    }
    
    if (!isEmailValid) {
      setEmailTouched(true);
      setEmailError('Please enter a valid email address.');
      isValid = false;
    }

    if (isValid) {
      saveProfile(fullName.trim(), email.trim(), companyName.trim() || undefined);
    }
  };

  // Button disabled state
  const isButtonDisabled = !fullName.trim() || !isEmailValid;

  return (
    <div className="min-h-screen bg-background flex flex-col justify-center items-center px-4 antialiased selection:bg-secondary-fixed selection:text-on-secondary-fixed">
      <Card className="w-full max-w-md bg-white border border-outline-variant rounded-2xl p-8 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)] flex flex-col text-left">
        {/* Brand/Logo Header */}
        <div className="flex items-center gap-2 mb-6">
          <div className="w-8 h-8 rounded bg-primary text-white flex items-center justify-center font-bold text-sm shrink-0">
            IP
          </div>
          <span className="font-display text-xl font-bold tracking-tighter text-primary">InsightPilot</span>
        </div>

        {/* Title Group */}
        <div className="space-y-2 mb-8">
          <h1 className="font-display text-3xl font-bold text-primary m-0 tracking-tight">
            Welcome to InsightPilot
          </h1>
          <p className="font-sans text-sm text-on-surface-variant leading-relaxed m-0">
            Let's personalize your workspace before we analyze your first dataset.
          </p>
        </div>

        {/* Form Fields */}
        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Full Name input */}
          <div className="space-y-1.5">
            <label htmlFor="fullName" className="font-display text-xs font-semibold text-on-surface uppercase tracking-wider block">
              Full Name <span className="text-red-500">*</span>
            </label>
            <input
              id="fullName"
              type="text"
              value={fullName}
              onChange={(e) => handleFullNameChange(e.target.value)}
              placeholder="Elena Rostova"
              className={`w-full bg-surface border rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 transition-all ${
                fullNameError 
                  ? 'border-red-500 focus:ring-red-100 focus:border-red-500' 
                  : 'border-outline-variant focus:ring-secondary/10 focus:border-secondary'
              }`}
            />
            {fullNameError && (
              <p className="text-xs text-red-600 font-semibold m-0 flex items-center gap-1">
                <AlertCircle size={12} />
                {fullNameError}
              </p>
            )}
          </div>

          {/* Email Address input */}
          <div className="space-y-1.5">
            <label htmlFor="email" className="font-display text-xs font-semibold text-on-surface uppercase tracking-wider block">
              Email Address <span className="text-red-500">*</span>
            </label>
            <div className="relative">
              <input
                id="email"
                type="text"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onBlur={handleEmailBlur}
                placeholder="elena@example.com"
                className={`w-full bg-surface border rounded-lg pl-4 pr-10 py-2.5 text-sm focus:outline-none focus:ring-2 transition-all ${
                  emailTouched && emailError 
                    ? 'border-red-500 focus:ring-red-100 focus:border-red-500' 
                    : emailTouched && isEmailValid
                    ? 'border-emerald-500 focus:ring-emerald-100 focus:border-emerald-500'
                    : 'border-outline-variant focus:ring-secondary/10 focus:border-secondary'
                }`}
              />
              {/* Validation feedback check icon */}
              {emailTouched && isEmailValid && (
                <CheckCircle2 size={16} className="absolute right-3 top-1/2 -translate-y-1/2 text-emerald-500" />
              )}
            </div>
            {emailTouched && emailError && (
              <p className="text-xs text-red-600 font-semibold m-0 flex items-center gap-1">
                <AlertCircle size={12} />
                {emailError}
              </p>
            )}
          </div>

          {/* Company Name input */}
          <div className="space-y-1.5">
            <label htmlFor="company" className="font-display text-xs font-semibold text-on-surface uppercase tracking-wider block">
              Company Name <span className="text-xs text-on-surface-variant font-normal lowercase">(optional)</span>
            </label>
            <input
              id="company"
              type="text"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              placeholder="Insight Corp"
              className="w-full bg-surface border border-outline-variant rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-secondary/10 focus:border-secondary transition-all"
            />
          </div>

          {/* Action Trigger */}
          <Button
            type="submit"
            disabled={isButtonDisabled}
            className={`w-full py-3 rounded-lg font-label-md text-label-md font-semibold transition-all flex items-center justify-center gap-2 ${
              isButtonDisabled 
                ? 'bg-slate-200 text-slate-400 border border-slate-300/40 cursor-not-allowed hover:bg-slate-200' 
                : 'bg-primary text-on-primary hover:bg-inverse-surface cursor-pointer'
            }`}
          >
            <User size={16} />
            Continue
          </Button>
        </form>
      </Card>
    </div>
  );
}
