import { BrowserRouter } from 'react-router-dom';
import { AppRoutes } from './routes/AppRoutes';
import { WorkspaceProvider } from './context/WorkspaceContext';

function App() {
  return (
    <WorkspaceProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </WorkspaceProvider>
  );
}

export default App;
