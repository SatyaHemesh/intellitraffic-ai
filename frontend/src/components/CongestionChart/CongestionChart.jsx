// frontend/src/components/CongestionChart/CongestionChart.jsx
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Filler,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { useLiveTrafficData } from '../../hooks/useLiveTrafficData';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Filler, Legend);

const CongestionChart = () => {
  const { data, loading } = useLiveTrafficData();

  if (loading) return <div className="h-64 flex items-center justify-center text-gray-500">Loading chart data...</div>;

  const chartData = {
    labels: data.map(record => new Date(record.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })),
    datasets: [
      {
        label: 'Detected Vehicles',
        data: data.map(record => record.total_vehicles),
        borderColor: '#06b6d4', // Cyan 500
        backgroundColor: 'rgba(6, 182, 212, 0.1)', // Faded Cyan
        borderWidth: 2,
        tension: 0.4,
        fill: true,
        pointBackgroundColor: '#0a0a0a',
        pointBorderColor: '#06b6d4',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: 'rgba(10, 10, 10, 0.9)',
        titleColor: '#d1d5db',
        bodyColor: '#06b6d4',
        borderColor: '#1f2937',
        borderWidth: 1,
      },
    },
    scales: {
      y: {
        grid: { color: '#1f2937', borderDash: [5, 5] },
        ticks: { color: '#9ca3af' },
        beginAtZero: true,
      },
      x: {
        grid: { display: false },
        ticks: { color: '#9ca3af', maxTicksLimit: 5 },
      },
    },
  };

  return (
    <div className="w-full h-72">
      <h3 className="text-gray-400 uppercase tracking-widest text-xs font-semibold mb-4">Traffic Volume Trends</h3>
      <div className="h-[220px]">
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
};

export default CongestionChart;