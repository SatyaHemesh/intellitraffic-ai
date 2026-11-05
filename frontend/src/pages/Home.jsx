// frontend/src/pages/Home.jsx
import Dashboard from '../components/Dashboard/Dashboard';

const Home = () => {
  return (
    <div className="max-w-[1600px] mx-auto space-y-8 animate-fade-in">
      <header className="mb-8">
        <h2 className="text-4xl font-semibold tracking-tight text-white">System Overview</h2>
        <p className="text-gray-400 text-sm mt-2 uppercase tracking-widest">
          Real-time Urban Traffic Monitoring & Predictive Analytics
        </p>
      </header>
      
      <Dashboard />
    </div>
  );
};

export default Home;