# ml/pipeline/video_processor.py
import cv2
import time
import threading
import numpy as np
from ml.detection.detector import YOLODetector
from ml.tracking.tracker_factory import TrackerFactory
from ml.analytics.density_calculator import DensityCalculator

class VideoProcessor:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.detector = YOLODetector()
        self.tracker = TrackerFactory()
        self.density_calc = DensityCalculator()

        # Threading & State Variables
        self.is_running = True
        self.frame_to_process = None
        self.latest_tracked_objects = []
        self.latest_stats = {"total_vehicles": 0, "density_level": "Calculating..."}
        self.lock = threading.Lock()

        # Playback & Video Stats
        self.is_paused = False
        self.speed_multiplier = 1
        self.direction = 1
        self.quit = False
        self.total_frames = 1
        self.current_frame = 0
        self.seek_to_frame = None
        
        # New Extensions: Looping and Mouse Tracking
        self.is_looping = False
        self.mouse_x = 0
        self.mouse_y = 0
        
        # Window & UI Setup
        self.window_name = 'IntelliTraffic AI - Stage 1 PoC'
        self.frame_shape = (720, 1280)

    def _inference_worker(self):
        """Background thread that runs the heavy YOLO AI."""
        while self.is_running:
            if self.frame_to_process is not None:
                with self.lock:
                    frame = self.frame_to_process.copy()
                    self.frame_to_process = None
                
                detections = self.detector.detect(frame)
                tracked = self.tracker.update(detections, frame)
                stats = self.density_calc.get_stats(tracked)
                
                with self.lock:
                    self.latest_tracked_objects = tracked
                    self.latest_stats = stats
            else:
                time.sleep(0.01)

    def _draw_vlc_ui(self, frame):
        """Draws a sleek, VLC-style media player control bar with extensions."""
        h, w = self.frame_shape[:2]
        bar_y = h - 80
        
        # Bottom Bar Background
        cv2.rectangle(frame, (0, bar_y), (w, h), (15, 15, 15), -1)
        cv2.line(frame, (0, bar_y), (w, bar_y), (50, 50, 50), 1)

        # 1. Timeline Progress Bar (VLC Orange)
        progress_ratio = self.current_frame / max(1, self.total_frames)
        prog_w = int(w * progress_ratio)
        
        cv2.rectangle(frame, (0, bar_y + 10), (w, bar_y + 16), (40, 40, 40), -1)
        cv2.rectangle(frame, (0, bar_y + 10), (prog_w, bar_y + 16), (0, 140, 255), -1) # Orange fill
        cv2.circle(frame, (prog_w, bar_y + 13), 6, (255, 255, 255), -1) # Scrubber handle

        # --- Timeline Hover Tooltip ---
        if bar_y + 5 <= self.mouse_y <= bar_y + 25:
            hover_ratio = self.mouse_x / w
            hover_frame = int(hover_ratio * self.total_frames)
            tooltip_text = f"Frame: {hover_frame}"
            
            # Draw Tooltip Box dynamically above cursor
            cv2.rectangle(frame, (self.mouse_x - 45, bar_y - 20), (self.mouse_x + 55, bar_y), (20, 20, 20), -1)
            cv2.putText(frame, tooltip_text, (self.mouse_x - 40, bar_y - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        # Center coordinates for media buttons
        cx = w // 2
        cy = bar_y + 45
        base_color = (200, 200, 200)
        active_color = (0, 140, 255) # Orange

        # 2. Rewind Icon (<<)
        rew_color = active_color if self.direction == -1 else base_color
        pts1 = np.array([[cx-70, cy-8], [cx-70, cy+8], [cx-85, cy]], np.int32)
        pts2 = np.array([[cx-55, cy-8], [cx-55, cy+8], [cx-70, cy]], np.int32)
        cv2.fillPoly(frame, [pts1, pts2], rew_color)

        # 3. Play / Pause Icon
        if self.is_paused:
            # Play Triangle
            pts = np.array([[cx-8, cy-12], [cx-8, cy+12], [cx+14, cy]], np.int32)
            cv2.fillPoly(frame, [pts], base_color)
        else:
            # Pause Bars
            cv2.rectangle(frame, (cx-8, cy-10), (cx-3, cy+10), base_color, -1)
            cv2.rectangle(frame, (cx+3, cy-10), (cx+8, cy+10), base_color, -1)

        # 4. Fast Forward Icon (>>)
        ff_color = active_color if (self.direction == 1 and self.speed_multiplier > 1) else base_color
        pts1 = np.array([[cx+55, cy-8], [cx+55, cy+8], [cx+70, cy]], np.int32)
        pts2 = np.array([[cx+70, cy-8], [cx+70, cy+8], [cx+85, cy]], np.int32)
        cv2.fillPoly(frame, [pts1, pts2], ff_color)

        # 5. Frame Step Icon (|>|)
        cv2.rectangle(frame, (cx + 120, cy - 8), (cx + 122, cy + 8), base_color, -1)
        pts_step = np.array([[cx + 126, cy - 8], [cx + 126, cy + 8], [cx + 140, cy]], np.int32)
        cv2.fillPoly(frame, [pts_step], base_color)

        # 6. Loop Toggle
        loop_color = active_color if self.is_looping else base_color
        cv2.putText(frame, "LOOP", (w - 135, cy + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, loop_color, 2)

        # 7. Stop / Quit Icon (Square)
        cv2.rectangle(frame, (w - 60, cy - 10), (w - 40, cy + 10), (50, 50, 200), -1)

        # --- System Info Overlay (Top Right) ---
        cv2.putText(frame, f"Frame: {self.current_frame}/{self.total_frames}", (w - 220, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        cv2.putText(frame, f"Speed: {self.speed_multiplier}x", (w - 220, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    def _handle_mouse_click(self, event, x, y, flags, param):
        """Listens for mouse clicks and tracks hover state for the timeline."""
        # Track hover coordinates
        if event == cv2.EVENT_MOUSEMOVE:
            self.mouse_x = x
            self.mouse_y = y

        if event == cv2.EVENT_LBUTTONDOWN:
            h, w = self.frame_shape[:2]
            bar_y = h - 80
            
            # If clicked inside the control bar area
            if y >= bar_y:
                # 1. Handle Timeline Scrubber Click
                if y <= bar_y + 25:
                    clicked_ratio = max(0.0, min(1.0, x / w))
                    self.seek_to_frame = int(clicked_ratio * self.total_frames)
                    return

                # 2. Handle Media Buttons
                cx = w // 2
                if cx - 90 <= x <= cx - 50:     # REWIND
                    self.direction = -1
                    self.speed_multiplier = 1
                elif cx - 20 <= x <= cx + 20:   # PLAY/PAUSE
                    self.is_paused = not self.is_paused
                elif cx + 50 <= x <= cx + 90:   # FAST FORWARD
                    self.direction = 1
                    self.speed_multiplier = min(8, self.speed_multiplier * 2)
                elif cx + 110 <= x <= cx + 160: # FRAME STEP
                    self.is_paused = True
                    self.seek_to_frame = min(self.total_frames, self.current_frame + 1)
                elif w - 145 <= x <= w - 90:    # LOOP TOGGLE
                    self.is_looping = not self.is_looping
                elif w - 70 <= x <= w - 30:     # QUIT
                    self.quit = True

    def process(self):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError(f"Error opening video file: {self.video_path}")

        self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        base_delay = 1.0 / fps

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(self.window_name, self._handle_mouse_click)

        ai_thread = threading.Thread(target=self._inference_worker)
        ai_thread.start()

        prev_time = time.time()

        while cap.isOpened() and not self.quit:
            
            # Handle Timeline Seeking
            if self.seek_to_frame is not None:
                cap.set(cv2.CAP_PROP_POS_FRAMES, self.seek_to_frame)
                self.current_frame = self.seek_to_frame
                self.seek_to_frame = None

            if not self.is_paused:
                if self.direction == -1:
                    next_pos = max(0, self.current_frame - 2)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, next_pos)
                    if next_pos == 0: self.direction = 1
                
                ret, frame = cap.read()
                
                # --- Auto-Loop Logic ---
                if not ret:
                    if self.is_looping or self.direction == -1:
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        self.direction = 1
                        continue
                    else:
                        break
                
                self.current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                self.frame_shape = frame.shape
                
                with self.lock:
                    if self.frame_to_process is None:
                        self.frame_to_process = frame.copy()

            with self.lock:
                display_frame = frame.copy() if 'frame' in locals() else None
                tracked = list(self.latest_tracked_objects)
                stats = dict(self.latest_stats)
            
            if display_frame is not None:
                annotated_frame = self.detector.draw_boxes(display_frame, tracked)
                
                # Draw Top Statistics Panel
                cv2.rectangle(annotated_frame, (10, 10), (450, 60), (10, 10, 10), -1)
                cv2.rectangle(annotated_frame, (10, 10), (450, 60), (100, 100, 100), 1)
                cv2.putText(annotated_frame, f"Density: {stats['density_level']} ({stats['total_vehicles']})", 
                            (20, 43), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
                
                # Draw VLC Style UI
                self._draw_vlc_ui(annotated_frame)
                cv2.imshow(self.window_name, annotated_frame)
            
            elapsed_time = time.time() - prev_time
            target_delay = (base_delay / self.speed_multiplier) if not self.is_paused else 0.1
            
            time_to_wait = max(1, int((target_delay - elapsed_time) * 1000))
            key = cv2.waitKey(time_to_wait) & 0xFF
            
            prev_time = time.time()
            if key == ord('q'): self.quit = True

        self.is_running = False
        ai_thread.join()
        cap.release()
        cv2.destroyAllWindows()