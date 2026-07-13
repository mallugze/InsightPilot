import { 
  Activity, 
  Sparkles, 
  ArrowRight, 
  ArrowUp, 
  ArrowDown, 
  AlertTriangle, 
  Award, 
  TrendingDown, 
  Lightbulb, 
  MoreVertical, 
  Brain, 
  MessageSquareCode, 
  Send, 
  Check, 
  TrendingUp 
} from 'lucide-react';
import { Card } from '../../../components/ui/Card';
import { Button } from '../../../components/ui/Button';
import { Badge } from '../../../components/ui/Badge';

export default function DashboardPage() {
  const handleStartAnalysis = (e: React.MouseEvent) => {
    e.preventDefault();
    alert('Analysis started');
  };

  return (
    <main className="pt-8 px-margin-page pb-section-gap max-w-container-max mx-auto flex flex-col gap-section-gap">
      {/* Top Section: Pulse & Hero Brief */}
      <section className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
        {/* Business Pulse Scorecard (Col 1-3) */}
        <Card className="lg:col-span-3 bg-surface rounded-lg card-border p-gutter flex flex-col justify-between hover:shadow-[0_4px_6px_-1px_rgb(0,0,0,0.05)] transition-shadow text-left">
          <div>
            <div className="flex justify-between items-start mb-stack-sm">
              <h3 className="font-label-caps text-label-caps text-on-surface-variant m-0">Business Pulse</h3>
              <Activity className="text-secondary" size={20} />
            </div>
            <div className="flex items-baseline gap-2 mb-unit">
              <span className="font-display-lg text-display-lg text-on-surface">87</span>
              <span className="font-body-sm text-body-sm text-on-surface-variant">/100</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-emerald-500"></div>
              <span className="font-label-md text-label-md text-emerald-700">Healthy</span>
            </div>
          </div>
          <div className="mt-stack-md pt-stack-md border-t border-outline-variant/30 space-y-2">
            <div className="flex justify-between text-sm">
              <span className="font-body-sm text-body-sm text-on-surface-variant">AI Confidence</span>
              <span className="font-label-md text-label-md text-on-surface">High (92%)</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="font-body-sm text-body-sm text-on-surface-variant">30-Day Trend</span>
              <div className="flex items-center text-emerald-600 gap-1">
                <TrendingUp size={14} />
                <span className="font-label-md text-label-md">+4.2%</span>
              </div>
            </div>
          </div>
        </Card>

        {/* Today's Brief (Hero) (Col 4-12) */}
        <div className="lg:col-span-9 bg-[#F0F7FF] rounded-lg card-border ai-accent-border p-[32px] hover:shadow-[0_4px_6px_-1px_rgb(0,0,0,0.05)] transition-shadow text-left">
          <div className="flex items-center gap-2 mb-stack-md">
            <Sparkles className="text-secondary" size={20} />
            <h2 className="font-headline-md text-headline-md text-on-surface m-0">Executive Brief</h2>
            <Badge className="ml-auto font-label-caps text-label-caps bg-secondary/10 text-secondary px-3 py-1 rounded-full border border-secondary/15">
              Generated just now
            </Badge>
          </div>
          <div className="prose prose-sm max-w-none text-on-surface font-body-lg text-body-lg leading-relaxed space-y-4">
            <p>
              Overall business health is strong, driven by a <strong>12% outperformance in Q3 Enterprise Sales</strong> across the EMEA region. The recent pricing structural changes have stabilized churn rates, currently resting below the 2% threshold. 
            </p>
            <p>
              However, operational costs in the APAC sector require attention. Logistics overhead has increased by 4.5% month-over-month due to supply chain friction. <strong>Strategic Priority:</strong> Reallocate Q4 marketing surplus to accelerate the automated onboarding initiative to offset these margin pressures.
            </p>
          </div>
          <div className="mt-stack-lg flex gap-stack-md">
            <Button 
              onClick={handleStartAnalysis}
              className="bg-primary text-on-primary font-label-md text-label-md px-4 py-2 rounded flex items-center gap-2"
            >
              View Full Analysis
              <ArrowRight size={16} />
            </Button>
            <Button className="border border-outline-variant bg-transparent text-on-surface font-label-md text-label-md px-4 py-2 rounded hover:bg-surface-container transition-colors">
              Share Brief
            </Button>
          </div>
        </div>
      </section>

      {/* SECTION 1: Business Signals */}
      <section>
        <div className="grid grid-cols-1 md:grid-cols-5 gap-stack-md">
          {/* Revenue */}
          <Card className="bg-surface rounded-lg card-border p-stack-md flex flex-col justify-between text-left h-24">
            <span className="font-label-caps text-label-caps text-on-surface-variant mb-unit">Revenue</span>
            <div className="flex items-center gap-2 mt-auto">
              <ArrowUp className="text-emerald-600" size={16} />
              <span className="font-label-md text-label-md text-emerald-700">+18%</span>
              <span className="font-body-sm text-body-sm text-on-surface-variant ml-auto">Healthy</span>
            </div>
          </Card>

          {/* Profit */}
          <Card className="bg-surface rounded-lg card-border p-stack-md flex flex-col justify-between text-left h-24">
            <span className="font-label-caps text-label-caps text-on-surface-variant mb-unit">Profit</span>
            <div className="flex items-center gap-2 mt-auto">
              <ArrowUp className="text-emerald-600" size={16} />
              <span className="font-label-md text-label-md text-emerald-700">+6%</span>
              <span className="font-body-sm text-body-sm text-on-surface-variant ml-auto">Stable</span>
            </div>
          </Card>

          {/* Customer Health */}
          <Card className="bg-surface rounded-lg card-border p-stack-md flex flex-col justify-between text-left h-24">
            <span className="font-label-caps text-label-caps text-on-surface-variant mb-unit">Customer Health</span>
            <div className="flex items-center gap-2 mt-auto">
              <ArrowDown className="text-orange-600" size={16} />
              <span className="font-label-md text-label-md text-orange-700">-2.4%</span>
              <span className="font-body-sm text-body-sm text-on-surface-variant ml-auto">Needs Attention</span>
            </div>
          </Card>

          {/* Growth */}
          <Card className="bg-surface rounded-lg card-border p-stack-md flex flex-col justify-between text-left h-24">
            <span className="font-label-caps text-label-caps text-on-surface-variant mb-unit">Growth</span>
            <div className="flex items-center gap-2 mt-auto">
              <ArrowUp className="text-emerald-600" size={16} />
              <span className="font-label-md text-label-md text-emerald-700">+11%</span>
              <span className="font-body-sm text-body-sm text-on-surface-variant ml-auto">Strong</span>
            </div>
          </Card>

          {/* Risk Level */}
          <Card className="bg-surface rounded-lg card-border p-stack-md flex flex-col justify-between text-left h-24">
            <span className="font-label-caps text-label-caps text-on-surface-variant mb-unit">Risk Level</span>
            <div className="flex items-center gap-2 mt-auto">
              <AlertTriangle className="text-amber-600" size={16} />
              <span className="font-label-md text-label-md text-amber-700">Medium</span>
              <span className="font-body-sm text-body-sm text-on-surface-variant ml-auto">Monitoring</span>
            </div>
          </Card>
        </div>
      </section>

      {/* SECTION 2: Hero & Zero */}
      <section>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-gutter">
          {/* Hero Card */}
          <Card className="bg-surface rounded-lg card-border p-gutter flex flex-col text-left">
            <div className="flex items-center gap-2 mb-stack-md">
              <div className="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-700 shrink-0">
                <Award size={16} />
              </div>
              <h3 className="font-headline-md text-headline-md text-on-surface m-0">Top Performer: Electronics</h3>
            </div>
            <p className="font-body-md text-body-md text-on-surface-variant mb-stack-md">
              Electronics category is showing the highest repeat purchase rate this quarter, driving overall revenue growth.
            </p>
            <div className="mt-auto bg-surface-container-low p-stack-md rounded-lg border border-outline-variant/30 flex items-start gap-stack-sm">
              <Lightbulb size={16} className="text-secondary mt-0.5" />
              <div>
                <span className="font-label-md text-label-md text-on-surface block mb-1 font-semibold">Recommendation</span>
                <span className="font-body-sm text-body-sm text-on-surface-variant block">Increase inventory levels for top 5 electronics SKUs ahead of Q4.</span>
              </div>
            </div>
          </Card>

          {/* Zero Card */}
          <Card className="bg-surface rounded-lg card-border p-gutter flex flex-col text-left">
            <div className="flex items-center gap-2 mb-stack-md">
              <div className="w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center text-orange-700 shrink-0">
                <TrendingDown size={16} />
              </div>
              <h3 className="font-headline-md text-headline-md text-on-surface m-0">Underperforming: Furniture</h3>
            </div>
            <p className="font-body-md text-body-md text-on-surface-variant mb-stack-md">
              Furniture margins have decreased by 4% due to rising freight costs and increased return rates in the EU market.
            </p>
            <div className="mt-auto bg-surface-container-low p-stack-md rounded-lg border border-outline-variant/30 flex items-start gap-stack-sm">
              <Lightbulb size={16} className="text-secondary mt-0.5" />
              <div>
                <span className="font-label-md text-label-md text-on-surface block mb-1 font-semibold">Recommendation</span>
                <span className="font-body-sm text-body-sm text-on-surface-variant block">Review pricing strategy and negotiate new freight contracts immediately.</span>
              </div>
            </div>
          </Card>
        </div>
      </section>

      {/* SECTION 3: Smart Charts */}
      <section>
        <div className="flex items-center justify-between mb-stack-md">
          <h2 className="font-headline-md text-headline-md text-on-surface m-0">Supporting Analytics</h2>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-gutter">
          {/* Revenue Trend */}
          <Card className="bg-surface rounded-lg card-border p-gutter flex flex-col h-72 text-left">
            <div className="flex justify-between items-center mb-stack-md">
              <h4 className="font-label-md text-label-md text-on-surface m-0 font-semibold">Revenue Trend</h4>
              <MoreVertical className="text-on-surface-variant" size={16} />
            </div>
            <div className="flex-1 border-b border-l border-outline-variant/30 relative flex items-end">
              <svg className="w-full h-full" preserveAspectRatio="none" viewBox="0 0 100 50">
                <path d="M0,45 Q10,30 20,40 T40,20 T60,25 T80,10 T100,5" fill="none" stroke="#2170e4" strokeWidth="2"></path>
                <path d="M0,50 L0,45 Q10,30 20,40 T40,20 T60,25 T80,10 T100,5 L100,50 Z" fill="#2170e4" fillOpacity="0.1"></path>
              </svg>
            </div>
          </Card>

          {/* Regional Performance */}
          <Card className="bg-surface rounded-lg card-border p-gutter flex flex-col h-72 text-left">
            <div className="flex justify-between items-center mb-stack-md">
              <h4 className="font-label-md text-label-md text-on-surface m-0 font-semibold">Regional Performance</h4>
              <MoreVertical className="text-on-surface-variant" size={16} />
            </div>
            <div className="flex-1 border-b border-l border-outline-variant/30 flex items-end justify-around px-4 pb-0">
              <div className="w-8 bg-secondary rounded-t-sm" style={{ height: '80%' }}></div>
              <div className="w-8 bg-secondary/60 rounded-t-sm" style={{ height: '60%' }}></div>
              <div className="w-8 bg-secondary/40 rounded-t-sm" style={{ height: '45%' }}></div>
              <div className="w-8 bg-secondary/20 rounded-t-sm" style={{ height: '30%' }}></div>
            </div>
          </Card>

          {/* Top Products */}
          <Card className="bg-surface rounded-lg card-border p-gutter flex flex-col h-72 text-left">
            <div className="flex justify-between items-center mb-stack-md">
              <h4 className="font-label-md text-label-md text-on-surface m-0 font-semibold">Top Products</h4>
              <MoreVertical className="text-on-surface-variant" size={16} />
            </div>
            <div className="flex-1 flex flex-col justify-center gap-4">
              <div className="w-full">
                <div className="flex justify-between text-xs text-on-surface-variant mb-1 font-semibold">
                  <span>Product A</span>
                  <span>45%</span>
                </div>
                <div className="w-full h-2 bg-surface-container rounded-full overflow-hidden">
                  <div className="h-full bg-secondary w-[45%]"></div>
                </div>
              </div>
              <div className="w-full">
                <div className="flex justify-between text-xs text-on-surface-variant mb-1 font-semibold">
                  <span>Product B</span>
                  <span>30%</span>
                </div>
                <div className="w-full h-2 bg-surface-container rounded-full overflow-hidden">
                  <div className="h-full bg-secondary/70 w-[30%]"></div>
                </div>
              </div>
              <div className="w-full">
                <div className="flex justify-between text-xs text-on-surface-variant mb-1 font-semibold">
                  <span>Product C</span>
                  <span>15%</span>
                </div>
                <div className="w-full h-2 bg-surface-container rounded-full overflow-hidden">
                  <div className="h-full bg-secondary/50 w-[15%]"></div>
                </div>
              </div>
            </div>
          </Card>

          {/* Profit Distribution */}
          <Card className="bg-surface rounded-lg card-border p-gutter flex flex-col h-72 text-left">
            <div className="flex justify-between items-center mb-stack-md">
              <h4 className="font-label-md text-label-md text-on-surface m-0 font-semibold">Profit Distribution</h4>
              <MoreVertical className="text-on-surface-variant" size={16} />
            </div>
            <div className="flex-1 flex items-center justify-center relative">
              <div className="w-32 h-32 rounded-full border-[16px] border-surface-container relative">
                <div className="absolute inset-[-16px] rounded-full border-[16px] border-secondary border-t-transparent border-l-transparent transform rotate-45"></div>
                <div className="absolute inset-[-16px] rounded-full border-[16px] border-secondary/60 border-b-transparent border-r-transparent transform -rotate-45"></div>
              </div>
            </div>
          </Card>
        </div>
      </section>

      {/* SECTION 4: AI Recommendations */}
      <section>
        <Card className="bg-surface rounded-lg card-border overflow-hidden">
          <div className="p-gutter border-b border-outline-variant/50 flex items-center gap-2 bg-surface-container-low text-left">
            <Brain className="text-secondary" size={20} />
            <h2 className="font-headline-md text-headline-md text-on-surface m-0">Prioritized Recommendations</h2>
          </div>
          <div className="flex flex-col divide-y divide-outline-variant/30 text-left">
            {/* Recommendation 1 */}
            <div className="p-gutter flex flex-col md:flex-row gap-stack-md items-start">
              <div className="w-full md:w-32 shrink-0">
                <Badge className="inline-block px-2 py-1 rounded text-xs font-semibold bg-red-100 text-red-700 border border-red-200">
                  High Priority
                </Badge>
              </div>
              <div className="flex-1">
                <h4 className="font-label-md text-label-md text-on-surface mb-1 font-semibold">Improve customer retention campaign</h4>
                <p className="font-body-sm text-body-sm text-on-surface-variant block m-0">
                  Churn risk detected in mid-market segment. Proactive outreach recommended.
                </p>
              </div>
              <div className="flex flex-col gap-1 w-full md:w-48 shrink-0">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-on-surface-variant">Expected Impact:</span>
                  <span className="text-emerald-600 font-semibold">High</span>
                </div>
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-on-surface-variant">AI Confidence:</span>
                  <span className="text-on-surface">94%</span>
                </div>
              </div>
            </div>

            {/* Recommendation 2 */}
            <div className="p-gutter flex flex-col md:flex-row gap-stack-md items-start">
              <div className="w-full md:w-32 shrink-0">
                <Badge className="inline-block px-2 py-1 rounded text-xs font-semibold bg-amber-100 text-amber-700 border border-amber-200">
                  Medium Priority
                </Badge>
              </div>
              <div className="flex-1">
                <h4 className="font-label-md text-label-md text-on-surface mb-1 font-semibold">Optimize supply chain logistics</h4>
                <p className="font-body-sm text-body-sm text-on-surface-variant block m-0">
                  Route inefficiencies identified in APAC region contributing to margin compression.
                </p>
              </div>
              <div className="flex flex-col gap-1 w-full md:w-48 shrink-0">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-on-surface-variant">Expected Impact:</span>
                  <span className="text-emerald-600 font-semibold">Medium</span>
                </div>
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-on-surface-variant">AI Confidence:</span>
                  <span className="text-on-surface">82%</span>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </section>

      {/* SECTION 5: AI Analyst */}
      <section>
        <Card className="bg-surface rounded-lg card-border p-gutter bg-gradient-to-b from-surface to-surface-container-low/50 text-left">
          <div className="flex items-center gap-2 mb-stack-lg">
            <MessageSquareCode className="text-secondary" size={20} />
            <h2 className="font-headline-md text-headline-md text-on-surface m-0">AI Analyst</h2>
          </div>
          <div className="flex flex-wrap gap-2 mb-stack-md">
            <button className="px-3 py-1.5 rounded-full border border-outline-variant/50 bg-surface text-on-surface-variant font-body-sm text-body-sm hover:bg-surface-container hover:text-on-surface transition-colors cursor-pointer font-semibold">
              "Why did profit decrease?"
            </button>
            <button className="px-3 py-1.5 rounded-full border border-outline-variant/50 bg-surface text-on-surface-variant font-body-sm text-body-sm hover:bg-surface-container hover:text-on-surface transition-colors cursor-pointer font-semibold">
              "Compare with last month"
            </button>
            <button className="px-3 py-1.5 rounded-full border border-outline-variant/50 bg-surface text-on-surface-variant font-body-sm text-body-sm hover:bg-surface-container hover:text-on-surface transition-colors cursor-pointer font-semibold">
              "Show unusual trends"
            </button>
            <button className="px-3 py-1.5 rounded-full border border-outline-variant/50 bg-surface text-on-surface-variant font-body-sm text-body-sm hover:bg-surface-container hover:text-on-surface transition-colors cursor-pointer font-semibold">
              "Explain customer retention"
            </button>
          </div>
          <div className="relative">
            <input 
              className="w-full bg-white border border-outline-variant rounded-lg pl-4 pr-12 py-3 focus:ring-2 focus:ring-secondary/20 focus:border-secondary transition-all font-body-md text-on-surface shadow-sm focus:outline-none" 
              placeholder="Ask a follow-up question..." 
              type="text"
            />
            <button className="absolute right-2 top-1/2 -translate-y-1/2 w-8 h-8 flex items-center justify-center rounded-md bg-secondary text-on-primary hover:bg-secondary/90 transition-colors cursor-pointer">
              <Send size={14} />
            </button>
          </div>
        </Card>
      </section>

      {/* SECTION 6: Analysis Timeline */}
      <section className="border-t border-outline-variant/30 pt-stack-lg pb-stack-md">
        <div className="flex flex-col md:flex-row items-center justify-between gap-stack-md">
          {/* Step 1 */}
          <div className="flex flex-col items-center text-center max-w-[120px] shrink-0">
            <div className="w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mb-2 shadow-sm font-bold">
              <Check size={16} />
            </div>
            <span className="font-label-caps text-label-caps text-on-surface-variant">Dataset Uploaded</span>
          </div>
          <div className="hidden md:block flex-1 h-[1px] bg-outline-variant/50 mx-4"></div>

          {/* Step 2 */}
          <div className="flex flex-col items-center text-center max-w-[120px] shrink-0">
            <div className="w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mb-2 shadow-sm font-bold">
              <Check size={16} />
            </div>
            <span className="font-label-caps text-label-caps text-on-surface-variant">Validated</span>
          </div>
          <div className="hidden md:block flex-1 h-[1px] bg-outline-variant/50 mx-4"></div>

          {/* Step 3 */}
          <div className="flex flex-col items-center text-center max-w-[120px] shrink-0">
            <div className="w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mb-2 shadow-sm font-bold">
              <Check size={16} />
            </div>
            <span className="font-label-caps text-label-caps text-on-surface-variant">Insights Generated</span>
          </div>
          <div className="hidden md:block flex-1 h-[1px] bg-outline-variant/50 mx-4"></div>

          {/* Step 4 */}
          <div className="flex flex-col items-center text-center max-w-[120px] shrink-0">
            <div className="w-8 h-8 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center mb-2 shadow-sm font-bold">
              <Check size={16} />
            </div>
            <span className="font-label-caps text-label-caps text-on-surface-variant">Recommendations Ready</span>
          </div>
          <div className="hidden md:block flex-1 h-[1px] bg-secondary text-secondary mx-4 relative">
            <div className="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-secondary"></div>
          </div>

          {/* Step 5 */}
          <div className="flex flex-col items-center text-center max-w-[120px] shrink-0">
            <div className="w-8 h-8 rounded-full bg-secondary text-on-primary flex items-center justify-center mb-2 shadow-sm font-bold">
              <Sparkles size={16} />
            </div>
            <span className="font-label-caps text-label-caps text-secondary font-bold">Brief Generated</span>
          </div>
        </div>
      </section>
    </main>
  );
}
