// frontend/src/components/DensityGauge/DensityGauge.jsx
const DensityGauge = ({ level }) => {
  // Determine colors based on density level
  const colors = {
    Low: 'bg-green-500/20 text-green-400 border-green-500/30',
    Medium: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
    High: 'bg-red-500/20 text-red-400 border-red-500/30',
  };

  const activeColor = colors[level] || 'bg-gray-800 text-gray-400 border-gray-700';

  return (
    <div className={`px-4 py-2 rounded-md border ${activeColor} flex items-center justify-center`}>
      <span className="font-bold tracking-wider uppercase text-sm">{level || 'Unknown'}</span>
    </div>
  );
};

export default DensityGauge;