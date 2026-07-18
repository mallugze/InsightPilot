import { useNavigate } from 'react-router-dom';
import {
  Zap,
  ArrowRight,
  Lock,
  FileText,
  Activity,
  TrendingUp,
  Lightbulb,
  ShieldCheck,
  Bot,
  Brain,
  Upload,
  Cpu,
  ClipboardList,
  Rocket,
  Sparkles,
} from 'lucide-react';
import { Button } from '../../../components/ui/Button';
import { Card } from '../../../components/ui/Card';
import { Badge } from '../../../components/ui/Badge';

export default function LandingPage() {
  const navigate = useNavigate();

  const handleStartApp = (e: React.MouseEvent) => {
    e.preventDefault();
    navigate('/dashboard');
  };

  return (
    <div className="bg-background text-on-background font-body-md antialiased overflow-x-hidden selection:bg-secondary-fixed selection:text-on-secondary-fixed">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 bg-surface/80 dark:bg-surface/80 backdrop-blur-xl border-b border-outline-variant dark:border-outline">
        <div className="max-w-container-max mx-auto px-margin-page flex items-center justify-between h-16">
          <div className="flex items-center gap-gutter">
            <span 
              onClick={handleStartApp} 
              className="font-display-lg text-headline-md tracking-tighter text-primary dark:text-on-primary cursor-pointer"
            >
              InsightPilot
            </span>
            <div className="hidden md:flex items-center gap-stack-md ml-stack-lg">
              <a className="text-slate-800 dark:text-slate-200 hover:text-primary transition-colors duration-200 cursor-pointer font-body-md text-body-md" href="#features">Features</a>
              <a className="text-slate-800 dark:text-slate-200 hover:text-primary transition-colors duration-200 cursor-pointer font-body-md text-body-md" href="#workflow">How It Works</a>
              <a className="text-slate-800 dark:text-slate-200 hover:text-primary transition-colors duration-200 cursor-pointer font-body-md text-body-md" href="#security">Security</a>
              <a className="text-slate-800 dark:text-slate-200 hover:text-primary transition-colors duration-200 cursor-pointer font-body-md text-body-md" href="#pricing">Pricing</a>
              <a className="text-slate-800 dark:text-slate-200 hover:text-primary transition-colors duration-200 cursor-pointer font-body-md text-body-md" href="#about">About</a>
            </div>
          </div>
          <div className="flex items-center gap-stack-md">
            <a 
              onClick={handleStartApp} 
              className="text-slate-800 dark:text-slate-200 hover:text-primary transition-colors duration-200 font-body-md text-body-md hidden md:block cursor-pointer"
            >
              Sign In
            </a>
            <Button 
              onClick={handleStartApp} 
              className="bg-primary text-on-primary font-label-md text-label-md px-4 py-2 rounded-lg hover:bg-inverse-surface transition-colors duration-200"
            >
              Get Started
            </Button>
          </div>
        </div>
      </nav>

      <main className="pt-24 pb-section-gap">
        {/* Hero Section */}
        <section className="hero-gradient relative pt-16 pb-32 px-margin-page overflow-hidden">
          <div className="max-w-container-max mx-auto grid grid-cols-1 lg:grid-cols-2 gap-section-gap items-center relative z-10">
            <div className="flex flex-col gap-stack-lg">
              <Badge className="inline-flex items-center gap-2 bg-surface-container py-1 px-3 rounded-full w-fit border border-surface-variant">
                <Zap className="text-secondary-container animate-pulse" size={16} />
                <span className="font-label-caps text-label-caps text-on-surface-variant">NEW: MULTI-FILE ANALYSIS</span>
              </Badge>
              <h1 className="font-display-lg text-display-lg text-primary leading-tight">See Beyond the Numbers.</h1>
              <p className="font-body-lg text-body-lg text-on-surface-variant max-w-xl">
                InsightPilot transforms spreadsheets and business datasets into explainable insights, executive briefs, and AI-powered recommendations in minutes.
              </p>
              <div className="flex flex-col sm:flex-row gap-stack-md pt-stack-sm">
                <Button 
                  onClick={handleStartApp} 
                  className="bg-primary text-on-primary font-label-md text-label-md px-6 py-3 rounded-lg hover:bg-inverse-surface transition-all flex items-center justify-center gap-2"
                >
                  Start Free
                  <ArrowRight size={18} />
                </Button>
              </div>
            </div>

            {/* Premium Dashboard Preview */}
            <div className="relative w-full h-[600px] bg-surface-container-lowest rounded-xl border border-outline-variant shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)] overflow-hidden flex flex-col">
              {/* Faux Browser Header */}
              <div className="h-10 bg-surface border-b border-outline-variant flex items-center px-4 gap-2">
                <div className="w-3 h-3 rounded-full bg-outline-variant"></div>
                <div className="w-3 h-3 rounded-full bg-outline-variant"></div>
                <div className="w-3 h-3 rounded-full bg-outline-variant"></div>
                <div className="mx-auto bg-surface-container-lowest border border-outline-variant rounded text-[10px] text-outline px-4 py-1 flex items-center gap-1.5 font-mono">
                  <Lock size={12} className="text-slate-400" /> app.insightpilot.com
                </div>
              </div>
              <div className="flex-1 p-6 grid grid-cols-12 gap-4 bg-background/50 overflow-hidden relative">
                {/* Left Nav Faux */}
                <div className="col-span-2 flex flex-col gap-4">
                  <div className="w-8 h-8 rounded bg-primary-container text-on-primary-container flex items-center justify-center mb-4 text-xs font-bold font-display">IP</div>
                  <div className="h-8 rounded bg-surface-container-high w-full"></div>
                  <div className="h-8 rounded bg-surface-container-lowest w-full opacity-50 border border-outline-variant/30"></div>
                  <div className="h-8 rounded bg-surface-container-lowest w-full opacity-50 border border-outline-variant/30"></div>
                </div>
                {/* Main Canvas */}
                <div className="col-span-10 flex flex-col gap-4">
                  {/* Header */}
                  <div className="flex justify-between items-center pb-2">
                    <div className="text-left">
                      <h3 className="font-headline-md text-headline-md text-primary">Q3 Performance Analysis</h3>
                      <p className="font-body-sm text-body-sm text-on-surface-variant">Generated just now</p>
                    </div>
                    <Badge className="bg-secondary-fixed text-on-secondary-fixed text-xs px-2.5 py-1 rounded-full flex items-center gap-1 font-semibold uppercase tracking-wider border border-secondary/15">
                      <Sparkles size={12} /> AI Verified
                    </Badge>
                  </div>
                  {/* Bento Grid Internal */}
                  <div className="grid grid-cols-3 gap-4 flex-1">
                    {/* Executive Brief */}
                    <Card className="col-span-2 row-span-2 bento-card p-4 rounded-lg flex flex-col text-left">
                      <h4 className="font-label-md text-label-md text-primary mb-3 flex items-center gap-2">
                        <FileText size={18} className="text-outline" />
                        Executive Brief
                      </h4>
                      <p className="font-body-sm text-body-sm text-on-surface-variant leading-relaxed">
                        Revenue grew by 14% this quarter, primarily driven by enterprise contract renewals. However, customer acquisition costs (CAC) in the mid-market segment increased by 8%, suggesting a need to optimize top-of-funnel marketing spend.
                      </p>
                      <div className="mt-auto pt-4 flex gap-2">
                        <div className="h-20 w-1/3 bg-surface-container rounded border border-outline-variant flex items-end p-2">
                          <div className="w-full bg-secondary-container h-[70%] rounded-sm"></div>
                        </div>
                        <div className="h-20 w-1/3 bg-surface-container rounded border border-outline-variant flex items-end p-2">
                          <div className="w-full bg-secondary-container h-[40%] rounded-sm"></div>
                        </div>
                        <div className="h-20 w-1/3 bg-surface-container rounded border border-outline-variant flex items-end p-2">
                          <div className="w-full bg-secondary-container h-[90%] rounded-sm"></div>
                        </div>
                      </div>
                    </Card>
                    {/* Business Pulse */}
                    <Card className="col-span-1 bento-card p-4 rounded-lg flex flex-col justify-between text-left">
                      <h4 className="font-label-md text-label-md text-primary flex items-center gap-2">
                        <Activity size={18} className="text-outline" />
                        Pulse
                      </h4>
                      <div>
                        <div className="text-3xl font-display-lg text-primary">87/100</div>
                        <div className="text-xs text-[#059669] flex items-center gap-1 mt-1 font-semibold">
                          <TrendingUp size={14} /> +3 points
                        </div>
                      </div>
                    </Card>
                    {/* AI Recommendation */}
                    <Card className="col-span-1 bento-card p-4 rounded-lg bg-surface-container-low border-secondary-fixed-dim ai-accent-border relative overflow-hidden text-left">
                      <h4 className="font-label-md text-label-md text-primary mb-2 flex items-center gap-2">
                        <Lightbulb size={16} className="text-secondary-container" />
                        Recommendation
                      </h4>
                      <p className="font-body-sm text-body-sm text-on-surface-variant text-[11px] leading-tight">
                        Reallocate 15% of mid-market ad spend to enterprise field marketing to stabilize CAC.
                      </p>
                      <Button 
                        onClick={handleStartApp} 
                        className="mt-3 text-[10px] bg-white border border-outline-variant px-2 py-1 rounded text-primary hover:bg-surface transition-colors font-semibold"
                      >
                        Apply Strategy
                      </Button>
                    </Card>
                  </div>
                </div>
              </div>
              {/* Decorative overlay for gradient fade */}
              <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-surface-container-lowest to-transparent pointer-events-none"></div>
            </div>
          </div>
          {/* Abstract Background Elements */}
          <div className="absolute top-0 right-0 -z-10 w-[800px] h-[800px] opacity-30 pointer-events-none mix-blend-multiply">
            <div className="w-full h-full bg-cover bg-center opacity-40" style={{ backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuDMHaE2s72IYN5833_HzP_JPoH1C4w0sSfeQe-guWIgL71mZ6Xieq7G3DD7LawalESWLMnwzmo0LBKclV8URlEqLFiyioE6BJJ-Fq0tlT-HntJXOiUIhACGQwtPwJWK1eywwDmonTSZ9p1HsiKPq1FKF5kMzFjLgXA3lUneLeM0KJtMC4-OSUkfiBpQjWoBqLaryymfRw_6zzKta0lOJoCHmZVU3GF3mTuQ5JRX5VM2vYogqYHREnK8aw')" }}></div>
          </div>
        </section>

        {/* Trust Section */}
        <section id="features" className="max-w-container-max mx-auto px-margin-page py-16 border-t border-outline-variant/50">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-gutter">
            <div className="flex items-start gap-4 text-left">
              <div className="p-3 bg-surface-container rounded-lg text-primary shrink-0">
                <ShieldCheck size={24} />
              </div>
              <div>
                <h3 className="font-headline-md text-headline-md text-primary text-lg mb-1">Private by Design</h3>
                <p className="font-body-sm text-body-sm text-on-surface-variant">Zero-retention architecture ensures your sensitive data is processed and instantly forgotten.</p>
              </div>
            </div>
            <div className="flex items-start gap-4 text-left">
              <div className="p-3 bg-surface-container rounded-lg text-primary shrink-0">
                <Bot size={24} />
              </div>
              <div>
                <h3 className="font-headline-md text-headline-md text-primary text-lg mb-1">AI Powered</h3>
                <p className="font-body-sm text-body-sm text-on-surface-variant">Leveraging state-of-the-art LLMs tuned specifically for financial and operational reasoning.</p>
              </div>
            </div>
            <div className="flex items-start gap-4 text-left">
              <div className="p-3 bg-surface-container rounded-lg text-primary shrink-0">
                <Brain size={24} />
              </div>
              <div>
                <h3 className="font-headline-md text-headline-md text-primary text-lg mb-1">Decision Intelligence</h3>
                <p className="font-body-sm text-body-sm text-on-surface-variant">Move beyond 'what happened' to 'why it happened' and 'what to do next'.</p>
              </div>
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section id="workflow" className="max-w-container-max mx-auto px-margin-page py-section-gap">
          <div className="text-center mb-16">
            <h2 className="font-display-lg text-headline-lg text-primary mb-4">From Raw Data to Executive Action</h2>
            <p className="font-body-lg text-body-lg text-on-surface-variant max-w-2xl mx-auto">A seamless workflow designed for leaders who need answers, not more dashboards to configure.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative">
            {/* Connecting Line (Desktop) */}
            <div className="hidden md:block absolute top-12 left-[10%] right-[10%] h-px bg-outline-variant z-0"></div>
            
            {/* Step 1 */}
            <div className="relative z-10 flex flex-col items-center text-center group">
              <div className="w-24 h-24 bg-surface-container-lowest border border-outline-variant rounded-full flex items-center justify-center mb-6 shadow-sm group-hover:border-primary transition-colors">
                <Upload size={30} className="text-on-surface-variant group-hover:text-primary transition-colors" />
              </div>
              <Badge className="bg-surface text-on-surface-variant font-label-caps text-label-caps px-2 py-1 rounded mb-3 border border-outline-variant">STEP 01</Badge>
              <h3 className="font-headline-md text-lg text-primary mb-2">Upload Dataset</h3>
              <p className="font-body-sm text-body-sm text-on-surface-variant">Securely drop in CSVs, Excel files, or connect via API.</p>
            </div>

            {/* Step 2 */}
            <div className="relative z-10 flex flex-col items-center text-center group">
              <div className="w-24 h-24 bg-surface-container-lowest border border-outline-variant rounded-full flex items-center justify-center mb-6 shadow-sm group-hover:border-primary transition-colors">
                <Cpu size={30} className="text-on-surface-variant group-hover:text-primary transition-colors" />
              </div>
              <Badge className="bg-surface text-on-surface-variant font-label-caps text-label-caps px-2 py-1 rounded mb-3 border border-outline-variant">STEP 02</Badge>
              <h3 className="font-headline-md text-lg text-primary mb-2">AI Understands</h3>
              <p className="font-body-sm text-body-sm text-on-surface-variant">The engine models relationships, identifies anomalies, and structures the context.</p>
            </div>

            {/* Step 3 */}
            <div className="relative z-10 flex flex-col items-center text-center group">
              <div className="w-24 h-24 bg-surface-container-lowest border border-outline-variant rounded-full flex items-center justify-center mb-6 shadow-sm group-hover:border-primary transition-colors">
                <ClipboardList size={30} className="text-on-surface-variant group-hover:text-primary transition-colors" />
              </div>
              <Badge className="bg-surface text-on-surface-variant font-label-caps text-label-caps px-2 py-1 rounded mb-3 border border-outline-variant">STEP 03</Badge>
              <h3 className="font-headline-md text-lg text-primary mb-2">Receive Brief</h3>
              <p className="font-body-sm text-body-sm text-on-surface-variant">Get a plain-English, executive-ready summary of key findings.</p>
            </div>

            {/* Step 4 */}
            <div className="relative z-10 flex flex-col items-center text-center group">
              <div className="w-24 h-24 bg-surface-container-lowest border border-outline-variant rounded-full flex items-center justify-center mb-6 shadow-sm group-hover:border-primary transition-colors">
                <Rocket size={30} className="text-on-surface-variant group-hover:text-primary transition-colors" />
              </div>
              <Badge className="bg-surface-container text-primary font-label-caps text-label-caps px-2 py-1 rounded mb-3 border border-outline-variant font-bold">STEP 04</Badge>
              <h3 className="font-headline-md text-lg text-primary mb-2">Make Decisions</h3>
              <p className="font-body-sm text-body-sm text-on-surface-variant">Act on AI-generated recommendations backed by source data.</p>
            </div>
          </div>
        </section>

        {/* Final CTA Section */}
        <section id="pricing" className="max-w-container-max mx-auto px-margin-page py-section-gap">
          <div className="bg-primary-container rounded-2xl p-12 md:p-20 text-center relative overflow-hidden flex flex-col items-center">
            {/* Subtle background pattern for CTA */}
            <div className="absolute inset-0 opacity-10" style={{ backgroundImage: "radial-gradient(circle at 2px 2px, white 1px, transparent 0)", backgroundSize: "24px 24px" }}></div>
            <h2 className="font-display-lg text-headline-lg text-on-primary mb-6 relative z-10">Ready to Understand Your Business Better?</h2>
            <p className="font-body-lg text-body-lg text-on-primary-container max-w-2xl mx-auto mb-10 relative z-10">
              Join forward-thinking enterprise teams who have replaced endless dashboard digging with clear, actionable intelligence.
            </p>
            <div className="flex flex-col sm:flex-row gap-stack-md relative z-10">
              <Button 
                onClick={handleStartApp} 
                className="bg-on-primary text-primary-container font-label-md text-label-md px-8 py-4 rounded-lg hover:bg-surface-container transition-all"
              >
                Start Free Trial
              </Button>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer id="about" className="w-full py-stack-lg border-t border-outline-variant dark:border-outline bg-surface dark:bg-background">
        <div className="max-w-container-max mx-auto px-margin-page flex flex-col md:flex-row justify-between items-center gap-stack-md">
          <div className="flex flex-col gap-2 text-center md:text-left">
            <span 
              onClick={handleStartApp} 
              className="font-display-lg text-headline-sm text-primary dark:text-on-primary cursor-pointer"
            >
              InsightPilot
            </span>
            <span className="font-body-sm text-body-sm text-on-surface-variant dark:text-outline">© 2024 InsightPilot. Sophisticated Functionalism for Enterprise.</span>
          </div>
          <div className="inline-flex flex-wrap justify-center gap-gutter font-body-sm text-body-sm text-on-surface-variant dark:text-outline">
            <a className="hover:text-secondary dark:hover:text-secondary-fixed transition-colors" href="#">Product</a>
            <a className="hover:text-secondary dark:hover:text-secondary-fixed transition-colors" href="#">Company</a>
            <a className="hover:text-secondary dark:hover:text-secondary-fixed transition-colors" href="#">Privacy</a>
            <a className="hover:text-secondary dark:hover:text-secondary-fixed transition-colors" href="#">Terms</a>
            <a className="hover:text-secondary dark:hover:text-secondary-fixed transition-colors" href="#">Contact</a>
            <a className="hover:text-secondary dark:hover:text-secondary-fixed transition-colors" href="#">GitHub</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
