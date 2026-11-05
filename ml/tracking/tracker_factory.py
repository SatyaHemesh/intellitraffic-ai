# ml/tracking/tracker_factory.py
import logging

class TrackerFactory:
    def __init__(self, tracker_type="bytetrack"):
        self.tracker_type = tracker_type
        logging.info(f"Initialized TrackerFactory with {tracker_type}")

    def update(self, detections, frame):
        """
        Updates the tracker with new detections and returns tracked objects with unique IDs.
        detections format: list of dicts with 'bbox', 'confidence', 'class_id'
        """
        # Note: This is a placeholder for the actual ByteTrack/DeepSORT logic.
        # For the Phase 1 PoC, we pass through the detections with mock IDs to ensure the pipeline flows.
        tracked_objects = []
        for i, det in enumerate(detections):
            tracked_objects.append({
                "track_id": i + 1,  # Mock ID assignment
                "class_id": det["class_id"],
                "confidence": det["confidence"],
                "bbox": det["bbox"]
            })
        return tracked_objects