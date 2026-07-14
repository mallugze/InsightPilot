import { NavLink } from 'react-router-dom';
import { 
  TrendingUp, 
  LayoutDashboard, 
  FolderOpen, 
  History, 
  FileText, 
  Settings, 
  Plus,
  Upload,
  MessageSquareCode
} from 'lucide-react';
import { useWorkspace } from '../../context/WorkspaceContext';
import { Button } from '../ui/Button';

export const Sidebar = () => {
  const { isWorkspaceConfirmed, workspaceName, profile } = useWorkspace();

  // Progressive Disclosure Nav Items
  const navItems = isWorkspaceConfirmed
    ? [
        { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
        { to: '/workspaces', label: 'Workspace', icon: FolderOpen },
        { to: '/history', label: 'Analysis History', icon: History },
        { to: '/chat', label: 'AI Analyst', icon: MessageSquareCode },
        { to: '/reports', label: 'Reports', icon: FileText },
        { to: '/settings', label: 'Settings', icon: Settings },
      ]
    : [
        { to: '/workspaces', label: 'Workspace', icon: FolderOpen },
        { to: '/upload', label: 'Upload', icon: Upload },
      ];

  return (
    <nav className="h-screen w-64 border-r border-outline-variant bg-surface-container-lowest flex flex-col p-4 gap-2 z-50 sticky top-0 shrink-0">
      {/* Brand Header */}
      <div className="flex items-center gap-3 px-4 py-4 mb-4">
        <div className="h-8 w-8 rounded-lg bg-primary text-on-primary flex items-center justify-center font-bold text-lg shadow-sm shrink-0">
          <TrendingUp size={20} />
        </div>
        <div className="text-left">
          <div className="text-headline-md font-headline-md font-semibold text-primary leading-tight">InsightPilot</div>
          <div className="text-label-caps font-label-caps text-on-surface-variant tracking-wider">Decision Intelligence</div>
        </div>
      </div>

      {/* New Analysis Button (only visible after onboarding is completed) */}
      {isWorkspaceConfirmed && (
        <Button 
          className="w-full bg-primary text-on-primary py-2.5 px-4 rounded-lg font-label-md text-label-md font-medium mb-6 hover:bg-inverse-surface transition-colors shadow-sm flex items-center justify-center gap-2 cursor-pointer"
          onClick={() => alert('New analysis session started')}
        >
          <Plus size={20} />
          New Analysis
        </Button>
      )}

      {/* Navigation Links */}
      <div className="flex-1 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-2 transition-colors duration-200 rounded-lg group ${
                  isActive
                    ? 'text-secondary font-bold bg-surface-container-low border-r-2 border-secondary'
                    : 'text-on-surface-variant hover:text-primary hover:bg-surface-container-low opacity-90 scale-[0.99] duration-150'
                }`
              }
            >
              <Icon size={18} className="group-active:scale-[0.98] transition-transform shrink-0" />
              <span className="font-body-md text-body-md">{item.label}</span>
            </NavLink>
          );
        })}
      </div>

      {/* Profile Section (Elena Rostova or customized profile) */}
      <div className="mt-auto pt-4 border-t border-outline-variant/50">
        <div className="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-surface-container-low cursor-pointer transition-colors">
          <img 
            className="w-8 h-8 rounded-full object-cover border border-outline-variant shrink-0" 
            alt="User Avatar" 
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuD1R6mVnj-9I2q9qpSljtnkmpu355R7TD8JL_ASuAmbTg6TwW1_JCxvZ6N3RV9iDtpn9ZShYz1ox_OKC6GzOUl6_y0ZjjgEI0emUG4gzgTRZLi66dbPf9arbRv3BsnIYK7rgKcBz1o8cpUzHga9eloqZVszQuDB9gaYfyhuMNcTuxeyGmdU6llYpujSIndiVeZyBrcP8qJ87-_msxfHmo91rLOrfEW-Kp_-jwlEsNT_E1DlvruCm3zLQQ"
          />
          <div className="flex flex-col text-left">
            <span className="font-label-md text-label-md text-on-surface">
              {profile?.fullName || 'Guest User'}
            </span>
            <span className="font-body-sm text-body-sm text-on-surface-variant text-[12px]">
              {workspaceName || 'No Workspace'}
            </span>
          </div>
        </div>
      </div>
    </nav>
  );
};
