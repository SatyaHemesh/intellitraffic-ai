# scripts/run_pipeline_demo.py
import sys
import os
import argparse
import logging

# Ensure the parent directory is in the Python path to import ml modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.pipeline.video_processor import VideoProcessor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Run the IntelliTraffic AI Pipeline PoC")
    parser.add_argument('--video', type=str, required=True, help="Path to the sample CCTV video file")
    args = parser.parse_args()

    if not os.path.exists(args.video):
        logging.error(f"Video file not found: {args.video}")
        return

    logging.info(f"Starting pipeline on video: {args.video}")
    
    try:
        processor = VideoProcessor(video_path=args.video)
        processor.process()
    except Exception as e:
        logging.error(f"Pipeline crashed: {e}")

if __name__ == "__main__":
    main()