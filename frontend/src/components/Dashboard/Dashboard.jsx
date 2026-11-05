// frontend/src/components/Dashboard/Dashboard.jsx
import LiveFeedViewer from '../LiveFeedViewer/LiveFeedViewer';
import CongestionChart from '../CongestionChart/CongestionChart';
import ReportSummary from '../ReportSummary/ReportSummary';

const Dashboard = () => {
  return (
    <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
      {/* Left Column: Live Feed and Charts (Takes up 2/3 of the screen) */}
      <div className="xl:col-span-2 space-y-6">
        {/* Live Feed Card */}
        <div className="bg-[#151515] border border-gray-800 rounded-xl overflow-hidden shadow-2xl">
          <LiveFeedViewer />
        </div>
        
        {/* Chart Card */}
        <div className="bg-[#151515] border border-gray-800 rounded-xl p-6 shadow-xl">
          <CongestionChart />
        </div>
      </div>
      
      {/* Right Column: Statistics and Summaries */}
      <div className="space-y-6">
        <div className="bg-[#151515] border border-gray-800 rounded-xl p-6 shadow-xl h-full">
          <ReportSummary />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;