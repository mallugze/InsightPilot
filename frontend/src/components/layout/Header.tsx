import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Bell, HelpCircle, User, FolderOpen, Settings, LogOut, Trash2 } from 'lucide-react';
import { useWorkspace } from '../../context/WorkspaceContext';

export const Header = () => {
  const navigate = useNavigate();
  const { 
    notifications, 
    markNotificationsAsRead, 
    dismissNotification, 
    resetOnboarding,
    isWorkspaceConfirmed 
  } = useWorkspace();

  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const [showNotifMenu, setShowNotifMenu] = useState(false);

  const unreadCount = notifications.filter(n => !n.read).length;

  const handleProfileNav = (path: string) => {
    setShowProfileMenu(false);
    navigate(path);
  };

  const handleSignOut = () => {
    setShowProfileMenu(false);
    resetOnboarding();
    navigate('/');
  };

  const toggleNotifications = () => {
    setShowNotifMenu(!showNotifMenu);
    if (!showNotifMenu) {
      markNotificationsAsRead();
    }
  };

  return (
    <header className="w-full sticky top-0 z-40 bg-surface/80 backdrop-blur-md h-16 border-b border-outline-variant flex justify-between items-center px-gutter shrink-0">
      {/* Brand & Sub-Navigation */}
      <div className="flex items-center gap-stack-lg">
        <h2 
          onClick={() => navigate(isWorkspaceConfirmed ? '/dashboard' : '/')} 
          className="font-headline-md text-headline-md font-semibold text-on-surface m-0 cursor-pointer"
        >
          InsightPilot
        </h2>
        {isWorkspaceConfirmed && (
          <nav className="hidden md:flex gap-stack-lg h-full items-center">
            <a className="font-label-md text-label-md text-primary border-b-2 border-primary pb-1 h-full flex items-center" href="#strategy">
              Global Strategy
            </a>
            <a className="font-label-md text-label-md text-on-surface-variant hover:text-primary transition-all h-full flex items-center" href="#forecast">
              Q3 Forecast
            </a>
          </nav>
        )}
      </div>

      {/* Action Controls */}
      <div className="flex items-center gap-stack-md relative">
        
        {/* Ask AI Search Input (Disabled for now) */}
        <div className="relative focus:ring-2 ring-secondary/10 rounded-full opacity-60">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant" />
          <input 
            disabled
            className="pl-10 pr-4 py-1.5 bg-surface-container rounded-full border-none text-xs w-64 focus:outline-none cursor-not-allowed font-medium text-slate-500" 
            placeholder="Ask AI (Enabled in Sprint 6)" 
            type="text"
          />
        </div>

        {/* Notification Bell */}
        <div className="relative">
          <button 
            onClick={toggleNotifications}
            className="text-on-surface-variant hover:text-primary transition-all relative p-1.5 rounded-lg hover:bg-surface-container-low cursor-pointer"
          >
            <Bell size={18} />
            {unreadCount > 0 && (
              <span className="absolute top-1.5 right-1.5 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-white animate-pulse"></span>
            )}
          </button>

          {/* Notifications Dropdown Panel */}
          {showNotifMenu && (
            <div className="absolute right-0 mt-2 w-80 bg-white border border-outline-variant rounded-xl shadow-lg py-3 px-4 z-50 text-left max-h-[350px] overflow-y-auto">
              <div className="flex justify-between items-center mb-3 border-b border-slate-100 pb-2">
                <span className="font-bold text-sm text-slate-800">Notifications</span>
                {unreadCount > 0 && (
                  <span className="text-[10px] bg-red-100 text-red-700 px-2 py-0.5 rounded-full font-semibold">
                    {unreadCount} new
                  </span>
                )}
              </div>

              {notifications.length === 0 ? (
                <p className="text-xs text-slate-400 text-center py-6">No notifications found.</p>
              ) : (
                <div className="space-y-3">
                  {notifications.map((notif) => (
                    <div 
                      key={notif.id} 
                      className={`flex justify-between items-start gap-2 p-2 rounded-lg transition-colors ${
                        notif.read ? 'bg-transparent' : 'bg-slate-50 border border-outline-variant/30'
                      }`}
                    >
                      <div className="flex flex-col text-xs leading-normal">
                        <span className="font-semibold text-slate-700">{notif.title}</span>
                        <span className="text-slate-500 text-[11px] mt-0.5">{notif.description}</span>
                        <span className="text-slate-400 text-[9px] mt-1">{notif.timestamp}</span>
                      </div>
                      <button 
                        onClick={() => dismissNotification(notif.id)}
                        className="text-slate-300 hover:text-red-500 p-1 rounded hover:bg-slate-100 shrink-0 cursor-pointer transition-colors"
                      >
                        <Trash2 size={12} />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Help Circle */}
        <button className="text-on-surface-variant hover:text-primary transition-all p-1.5 rounded-lg hover:bg-surface-container-low cursor-pointer">
          <HelpCircle size={18} />
        </button>

        {/* Profile Avatar Trigger dropdown */}
        <div className="relative">
          <button 
            onClick={() => setShowProfileMenu(!showProfileMenu)}
            className="w-8 h-8 rounded-full overflow-hidden border border-outline-variant ml-2 shrink-0 cursor-pointer focus:outline-none hover:opacity-90"
          >
            <img 
              alt="Executive User Profile" 
              className="w-full h-full object-cover" 
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuA7zhrT7PA6dYAmBTESh3paEBKpPT9ALQfhkpfbseggdXJqlsZNTvCX8o5RMW7WZlyKRX3dauqujIZHlwaBM7D4swnAaW-FBiVSxXHz5WcnzyJQ-o8A0M4nEgUDTQ6faVOHX799JavsvVPvVx3U48IQKxhWrPyPrJOxXW7G-7AePs4Af5c9zceU9mVyclITI98Z-3eO7FGZsm_9XLVC03k877u46rG0mM4ecRyXaI5QaSd5LUnjXaBykg"
            />
          </button>

          {/* Profile Dropdown Menu */}
          {showProfileMenu && (
            <div className="absolute right-0 mt-2 w-48 bg-white border border-outline-variant rounded-xl shadow-lg py-1.5 z-50 text-left">
              <button 
                onClick={() => handleProfileNav('/profile')}
                className="w-full px-4 py-2 text-xs text-slate-700 hover:bg-slate-50 transition-colors flex items-center gap-2 font-medium cursor-pointer"
              >
                <User size={14} />
                Profile
              </button>
              <button 
                onClick={() => handleProfileNav('/workspaces')}
                className="w-full px-4 py-2 text-xs text-slate-700 hover:bg-slate-50 transition-colors flex items-center gap-2 font-medium cursor-pointer"
              >
                <FolderOpen size={14} />
                Workspace
              </button>
              <button 
                onClick={() => handleProfileNav('/settings')}
                className="w-full px-4 py-2 text-xs text-slate-700 hover:bg-slate-50 transition-colors flex items-center gap-2 font-medium cursor-pointer"
              >
                <Settings size={14} />
                Settings
              </button>
              <div className="border-t border-slate-100 my-1"></div>
              <button 
                onClick={handleSignOut}
                className="w-full px-4 py-2 text-xs text-red-600 hover:bg-red-50 transition-colors flex items-center gap-2 font-medium cursor-pointer"
              >
                <LogOut size={14} />
                Sign Out
              </button>
            </div>
          )}
        </div>

      </div>
    </header>
  );
};
