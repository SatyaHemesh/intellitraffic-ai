// frontend/src/App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-[#0a0a0a] text-gray-200 selection:bg-cyan-500/30">
        <nav className="border-b border-gray-800 bg-[#111] px-8 py-4 sticky top-0 z-50">
          <h1 className="text-2xl font-bold tracking-widest text-white">
            INTELLI<span className="text-cyan-500">TRAFFIC</span>
          </h1>
        </nav>
        
        <main className="p-8">
          <Routes>
            <Route path="/" element={<Home />} />
            {/* Future routes for Analytics and CameraManagement can be added here */}
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;