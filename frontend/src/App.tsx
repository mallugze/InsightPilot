import { useEffect } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { AppRoutes } from './routes/AppRoutes';
import { WorkspaceProvider } from './context/WorkspaceContext';

function App() {
  useEffect(() => {
    const savedTheme = localStorage.getItem('color-theme');
    if (savedTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, []);

  return (
    <WorkspaceProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </WorkspaceProvider>
  );
}

export default App;
