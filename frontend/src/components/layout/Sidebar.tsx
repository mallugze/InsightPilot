import { useState } from 'react';
import { useNavigate, NavLink } from 'react-router-dom';
import { 
  TrendingUp, 
  LayoutDashboard, 
  FolderOpen, 
  History, 
  FileText, 
  Settings, 
  Plus,
  Upload,
  MessageSquareCode,
  User,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import { useWorkspace } from '../../context/WorkspaceContext';
import { Button } from '../ui/Button';

export const Sidebar = () => {
  const navigate = useNavigate();
  const { isWorkspaceConfirmed, workspaceName, profile, resetOnboardingKeepProfile } = useWorkspace();
  
  const [isCollapsed, setIsCollapsed] = useState(() => {
    return localStorage.getItem('sidebar-collapsed') === 'true';
  });

  const toggleSidebar = () => {
    const newState = !isCollapsed;
    setIsCollapsed(newState);
    localStorage.setItem('sidebar-collapsed', String(newState));
  };

  // Progressive Disclosure Nav Items
  const navItems = isWorkspaceConfirmed
    ? [
        { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
        { to: '/workspaces', label: 'Workspace', icon: FolderOpen },
        { to: '/history', label: 'Analysis History', icon: History },
        { to: '/ai-analyst', label: 'AI Analyst', icon: MessageSquareCode },
        { to: '/reports', label: 'Reports', icon: FileText },
        { to: '/settings', label: 'Settings', icon: Settings },
      ]
    : [
        { to: '/workspaces', label: 'Workspace', icon: FolderOpen },
        { to: '/upload', label: 'Upload', icon: Upload },
      ];

  return (
    <nav className={`h-screen border-r border-outline-variant bg-surface-container-lowest flex flex-col p-4 gap-2 z-50 sticky top-0 shrink-0 transition-all duration-300 ${isCollapsed ? 'w-20' : 'w-64'}`}>
      {/* Brand Header */}
      <div className={`flex items-center justify-between py-2 mb-4 ${isCollapsed ? 'px-0' : 'px-4'}`}>
        <div className="flex items-center gap-3 overflow-hidden">
          <div className="h-8 w-8 rounded-lg bg-primary text-on-primary flex items-center justify-center font-bold text-lg shadow-sm shrink-0">
            <TrendingUp size={20} />
          </div>
          {!isCollapsed && (
            <div className="text-left">
              <div className="text-headline-md font-headline-md font-semibold text-primary leading-tight">InsightPilot</div>
              <div className="text-label-caps font-label-caps text-on-surface-variant tracking-wider">Decision Intelligence</div>
            </div>
          )}
        </div>
        <button 
          onClick={toggleSidebar}
          className={`p-1.5 rounded-lg hover:bg-surface-container-low text-on-surface-variant hover:text-primary transition-colors cursor-pointer shrink-0 ${isCollapsed ? 'mx-auto' : ''}`}
        >
          {isCollapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
        </button>
      </div>

      {/* New Analysis Button */}
      {isWorkspaceConfirmed && (
        <Button 
          className={`bg-primary text-on-primary font-medium mb-6 hover:bg-inverse-surface transition-colors shadow-sm flex items-center justify-center gap-2 cursor-pointer ${
            isCollapsed ? 'w-12 h-12 rounded-full p-0 mx-auto' : 'w-full py-2.5 px-4 rounded-lg text-label-md'
          }`}
          onClick={() => {
            resetOnboardingKeepProfile();
            navigate('/upload');
          }}
          title={isCollapsed ? "New Analysis" : undefined}
        >
          <Plus size={20} />
          {!isCollapsed && <span>New Analysis</span>}
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
              title={isCollapsed ? item.label : undefined}
              className={({ isActive }) =>
                `flex items-center transition-colors duration-200 rounded-lg group ${
                  isCollapsed ? 'justify-center p-3' : 'gap-3 px-4 py-2'
                } ${
                  isActive
                    ? 'text-secondary font-bold bg-surface-container-low border-r-2 border-secondary'
                    : 'text-on-surface-variant hover:text-primary hover:bg-surface-container-low opacity-90 scale-[0.99] duration-150'
                }`
              }
            >
              <Icon size={18} className="group-active:scale-[0.98] transition-transform shrink-0" />
              {!isCollapsed && <span className="font-body-md text-body-md text-left flex-1 truncate">{item.label}</span>}
            </NavLink>
          );
        })}
      </div>

      {/* Profile Section */}
      <div className="mt-auto pt-4 border-t border-outline-variant/50">
        <div className={`flex items-center rounded-lg hover:bg-surface-container-low cursor-pointer transition-colors ${
          isCollapsed ? 'justify-center p-2' : 'gap-3 px-4 py-3'
        }`}>
          <div className="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center border border-outline-variant shrink-0 text-on-surface-variant">
            <User size={16} />
          </div>
          {!isCollapsed && (
            <div className="flex flex-col text-left overflow-hidden">
              <span className="font-label-md text-label-md text-on-surface truncate">
                {profile?.fullName || 'Guest User'}
              </span>
              <span className="font-body-sm text-body-sm text-on-surface-variant text-[12px] truncate">
                {workspaceName || 'No Workspace'}
              </span>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};
