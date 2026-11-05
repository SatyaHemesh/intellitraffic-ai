// frontend/src/components/ReportSummary/ReportSummary.jsx
import { useLiveTrafficData } from '../../hooks/useLiveTrafficData';
import DensityGauge from '../DensityGauge/DensityGauge';
import { Camera, Car, AlertTriangle } from 'lucide-react';

const ReportSummary = () => {
  const { data, loading, error } = useLiveTrafficData();

  if (loading) return <div className="text-gray-500 text-sm">Synchronizing data...</div>;
  if (error) return <div className="text-red-500/80 text-sm">{error}</div>;

  const currentStats = data.length > 0 ? data[data.length - 1] : { total_vehicles: 0, density_level: 'Low' };

  return (
    <div className="flex flex-col h-full space-y-8">
      <div>
        <h3 className="text-gray-400 uppercase tracking-widest text-xs font-semibold mb-6">Real-Time Status</h3>
        
        <div className="space-y-6">
          <div className="flex justify-between items-center pb-4 border-b border-gray-800/50">
            <div className="flex items-center gap-3">
              <Camera className="w-5 h-5 text-gray-500" />
              <span className="text-gray-300 font-medium">Active Cameras</span>
            </div>
            <span className="text-white font-mono">1</span>
          </div>

          <div className="flex justify-between items-center pb-4 border-b border-gray-800/50">
            <div className="flex items-center gap-3">
              <Car className="w-5 h-5 text-gray-500" />
              <span className="text-gray-300 font-medium">Current Count</span>
            </div>
            <span className="text-cyan-400 font-mono text-xl">{currentStats.total_vehicles}</span>
          </div>

          <div className="flex justify-between items-center">
            <div className="flex items-center gap-3">
              <AlertTriangle className="w-5 h-5 text-gray-500" />
              <span className="text-gray-300 font-medium">Congestion</span>
            </div>
            <DensityGauge level={currentStats.density_level} />
          </div>
        </div>
      </div>

      <div className="mt-auto bg-black/40 rounded-lg p-4 border border-gray-800">
        <p className="text-xs text-gray-500 leading-relaxed">
          IntelliTraffic AI correlates real-time YOLOv8 spatial recognition to evaluate municipal traffic flow patterns mapped to SDG 11 objectives.
        </p>
      </div>
    </div>
  );
};

export default ReportSummary;