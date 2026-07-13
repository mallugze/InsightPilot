import { Search, Bell, HelpCircle } from 'lucide-react';

export const Header = () => {
  return (
    <header className="w-full sticky top-0 z-40 bg-surface/80 backdrop-blur-md h-16 border-b border-outline-variant flex justify-between items-center px-gutter shrink-0">
      {/* Brand & Sub-Navigation */}
      <div className="flex items-center gap-stack-lg">
        <h2 className="font-headline-md text-headline-md font-semibold text-on-surface m-0">InsightPilot</h2>
        <nav className="hidden md:flex gap-stack-lg h-full items-center">
          <a className="font-label-md text-label-md text-primary border-b-2 border-primary pb-1 h-full flex items-center" href="#strategy">
            Global Strategy
          </a>
          <a className="font-label-md text-label-md text-on-surface-variant hover:text-primary transition-all h-full flex items-center" href="#forecast">
            Q3 Forecast
          </a>
        </nav>
      </div>

      {/* Action Controls */}
      <div className="flex items-center gap-stack-md">
        {/* Ask AI Search Input */}
        <div className="relative focus:ring-2 ring-secondary/10 rounded-full">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant" />
          <input 
            className="pl-10 pr-4 py-1.5 bg-surface-container rounded-full border-none focus:ring-1 focus:ring-secondary text-sm w-48 focus:outline-none" 
            placeholder="Ask AI..." 
            type="text"
          />
        </div>

        {/* Notification Bell */}
        <button className="text-on-surface-variant hover:text-primary transition-all relative p-1.5 rounded-lg hover:bg-surface-container-low">
          <Bell size={18} />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-secondary rounded-full"></span>
        </button>

        {/* Help Circle */}
        <button className="text-on-surface-variant hover:text-primary transition-all p-1.5 rounded-lg hover:bg-surface-container-low">
          <HelpCircle size={18} />
        </button>

        {/* Profile Avatar */}
        <div className="w-8 h-8 rounded-full overflow-hidden border border-outline-variant ml-2 shrink-0">
          <img 
            alt="Executive User Profile" 
            className="w-full h-full object-cover" 
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuA7zhrT7PA6dYAmBTESh3paEBKpPT9ALQfhkpfbseggdXJqlsZNTvCX8o5RMW7WZlyKRX3dauqujIZHlwaBM7D4swnAaW-FBiVSxXHz5WcnzyJQ-o8A0M4nEgUDTQ6faVOHX799JavsvVPvVx3U48IQKxhWrPyPrJOxXW7G-7AePs4Af5c9zceU9mVyclITI98Z-3eO7FGZsm_9XLVC03k877u46rG0mM4ecRyXaI5QaSd5LUnjXaBykg"
          />
        </div>
      </div>
    </header>
  );
};
