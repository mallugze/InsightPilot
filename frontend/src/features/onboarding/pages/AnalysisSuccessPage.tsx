import { useNavigate } from 'react-router-dom';
import { Button } from '../../../components/ui/Button';
import { Card } from '../../../components/ui/Card';
import { CheckCircle2, ArrowRight } from 'lucide-react';

export default function AnalysisSuccessPage() {
  const navigate = useNavigate();

  const handleProceed = () => {
    navigate('/review-analysis');
  };

  return (
    <div className="min-h-screen bg-background flex flex-col justify-center items-center px-4 antialiased selection:bg-secondary-fixed selection:text-on-secondary-fixed">
      <Card className="w-full max-w-md bg-white border border-outline-variant rounded-2xl p-10 shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)] flex flex-col items-center text-center">
        
        {/* Animated Check Circle */}
        <div className="w-16 h-16 bg-emerald-50 text-emerald-500 rounded-full flex items-center justify-center mb-6 border border-emerald-100">
          <CheckCircle2 size={36} className="animate-bounce" />
        </div>

        {/* Header Title */}
        <h1 className="font-display text-2xl font-bold text-primary m-0 tracking-tight mb-2">
          Your dashboard is ready!
        </h1>
        
        {/* Description */}
        <p className="font-sans text-sm text-on-surface-variant leading-relaxed m-0 mb-8 max-w-sm">
          InsightPilot completed scanning your spreadsheet. We parsed fields, analyzed trends, and prepared personalized recommendations.
        </p>

        {/* Action button */}
        <Button
          onClick={handleProceed}
          className="w-full bg-primary text-on-primary py-3 rounded-lg font-label-md text-label-md font-semibold hover:bg-inverse-surface transition-all flex items-center justify-center gap-2 cursor-pointer"
        >
          Review Results & Insights
          <ArrowRight size={16} />
        </Button>
      </Card>
    </div>
  );
}
