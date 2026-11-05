# ml/detection/detector.py
import cv2
import numpy as np
from ultralytics import YOLO
import logging

class YOLODetector:
    # UPGRADE 1: Switch to the Medium model (yolov8m.pt) for better accuracy
    # UPGRADE 2: Lower confidence to 0.25 to catch harder-to-see vehicles
    # Change 'yolov8m.pt' to 'yolov8s.pt'
    def __init__(self, model_path: str = 'yolov8s.pt', conf_threshold: float = 0.25):
        """
        Initializes the YOLO model for vehicle detection.
        """
        try:
            self.model = YOLO(model_path)
            self.conf_threshold = conf_threshold
            # COCO dataset class IDs for vehicles: 2 (car), 3 (motorcycle), 5 (bus), 7 (truck)
            self.vehicle_classes = [2, 3, 5, 7] 
            logging.info(f"Successfully loaded YOLO model from {model_path}")
        except Exception as e:
            logging.error(f"Error loading YOLO model: {e}")
            raise e

    def detect(self, frame: np.ndarray):
        """
        Processes a single frame and returns bounding boxes for detected vehicles.
        """
        # UPGRADE 3: Set imgsz=1280. This forces the AI to look at a higher-resolution 
        # grid, drastically improving the detection of small/distant vehicles.
        # Ensure verbose=False is present
        results = self.model(frame, imgsz=640, conf=self.conf_threshold, verbose=False)[0]
        detections = []

        for box in results.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            
            # Filter for vehicles
            if class_id in self.vehicle_classes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append({
                    "class_id": class_id,
                    "confidence": confidence,
                    "bbox": [x1, y1, x2, y2]
                })
                
        return detections

    def draw_boxes(self, frame: np.ndarray, detections: list) -> np.ndarray:
        """
        Utility to draw bounding boxes on the frame for visual testing.
        """
        annotated_frame = frame.copy()
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            # Color mapping for clarity: Cars (Green), Bikes (Red), Buses/Trucks (Blue)
            color = (0, 255, 0) if det['class_id'] == 2 else (0, 0, 255) if det['class_id'] == 3 else (255, 0, 0)
            
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(annotated_frame, f"ID:{det['class_id']} {det['confidence']:.2f}", 
                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        return annotated_frame