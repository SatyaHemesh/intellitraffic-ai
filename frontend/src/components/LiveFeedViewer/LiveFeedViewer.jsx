// frontend/src/components/LiveFeedViewer/LiveFeedViewer.jsx
import { Activity } from 'lucide-react';

const LiveFeedViewer = () => {
  return (
    <div className="relative w-full aspect-video bg-black flex flex-col items-center justify-center group">
      {/* Decorative corners for a high-tech UI feel */}
      <div className="absolute top-4 left-4 w-8 h-8 border-t-2 border-l-2 border-cyan-500/50"></div>
      <div className="absolute top-4 right-4 w-8 h-8 border-t-2 border-r-2 border-cyan-500/50"></div>
      <div className="absolute bottom-4 left-4 w-8 h-8 border-b-2 border-l-2 border-cyan-500/50"></div>
      <div className="absolute bottom-4 right-4 w-8 h-8 border-b-2 border-r-2 border-cyan-500/50"></div>

      {/* Recording Indicator */}
      <div className="absolute top-6 right-8 flex items-center gap-2">
        <span className="w-2.5 h-2.5 rounded-full bg-red-600 animate-pulse"></span>
        <span className="text-red-500 text-xs font-bold tracking-widest">REC</span>
      </div>

      {/* Main Content */}
      <Activity className="w-12 h-12 text-gray-700 mb-4 group-hover:text-cyan-500/50 transition-colors duration-500" />
      <p className="text-gray-500 uppercase tracking-widest text-sm font-medium">
        Camera Feed Offline
      </p>
      <p className="text-gray-700 text-xs mt-2 font-mono">Awaiting YOLO Pipeline Connection</p>
      
      {/* Overlay Scanline Effect */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[length:100%_4px,3px_100%] pointer-events-none opacity-20"></div>
    </div>
  );
};

export default LiveFeedViewer;