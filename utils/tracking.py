import cv2
import torch
from pathlib import Path
from deep_sort_realtime.deepsort_tracker import DeepSort
from ultralytics import YOLO
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CupTracker:
    def __init__(self):
        """Initialize with YOLOv5 model and DeepSORT tracker"""
        self.model = YOLO('yolov5s.pt')
        self.tracker = DeepSort(max_age=30)
        
    def process_video(self, video_path: str) -> str:
        """Process video and return path to processed output"""
        try:
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                raise ValueError("Could not open video file")

            # Get video properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            
            # Create output video writer
            output_path = str(Path(video_path).with_suffix('.processed.mp4'))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Detect cups using YOLO
                results = self.model(frame)
                detections = []
                
                # Convert YOLO detections to DeepSORT format
                for box in results[0].boxes.xyxy:
                    if box is not None:
                        x1, y1, x2, y2 = box.tolist()
                        detections.append(([x1, y1, x2-x1, y2-y1], 1.0, 'cup'))

                # Update tracker
                tracks = self.tracker.update_tracks(detections, frame=frame)
                
                # Draw tracking results
                for track in tracks:
                    if not track.is_confirmed():
                        continue
                        
                    ltrb = track.to_ltrb()
                    cv2.rectangle(frame, 
                                (int(ltrb[0]), int(ltrb[1])), 
                                (int(ltrb[2]), int(ltrb[3])), 
                                (0, 255, 0), 2)
                    cv2.putText(frame, 
                              f"Cup #{track.track_id}", 
                              (int(ltrb[0]), int(ltrb[1]-10)), 
                              cv2.FONT_HERSHEY_SIMPLEX, 
                              0.9, 
                              (0, 255, 0), 
                              2)

                out.write(frame)

            # Cleanup
            cap.release()
            out.release()
            
            return output_path

        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            raise

        finally:
            cv2.destroyAllWindows()
