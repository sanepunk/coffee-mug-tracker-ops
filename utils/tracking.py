import cv2
import torch
import logging
from pathlib import Path
from deep_sort_realtime.deepsort_tracker import DeepSort
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self):
        """Initialize the video processor with YOLOv5 model and DeepSORT tracker"""
        # Load YOLOv5 model
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        # Only detect cups (class 41 in COCO dataset)
        self.model.classes = [41]
        
        # Initialize DeepSORT tracker
        self.tracker = DeepSort(
            max_age=30,
            n_init=3,
            nms_max_overlap=1.0,
            max_cosine_distance=0.3,
            nn_budget=None,
            override_track_class=None,
            embedder="mobilenet",
            half=True,
            bgr=True,
            embedder_gpu=True
        )

    def process_frame(self, frame):
        """Process a single frame with detection and tracking"""
        # YOLOv5 inference
        results = self.model(frame)
        detections = results.xyxy[0].cpu().numpy()
        
        # Filter for cups only (confidence > 0.5)
        cup_detections = detections[detections[:, -1] == 41]
        cup_detections = cup_detections[cup_detections[:, 4] > 0.5]
        
        # Update tracker
        tracks = self.tracker.update_tracks(cup_detections, frame=frame)
        
        # Draw detections and tracks
        for track in tracks:
            if not track.is_confirmed():
                continue
            
            track_id = track.track_id
            ltrb = track.to_ltrb()
            
            # Draw bounding box
            cv2.rectangle(frame, 
                        (int(ltrb[0]), int(ltrb[1])), 
                        (int(ltrb[2]), int(ltrb[3])), 
                        (0, 255, 0), 2)
            
            # Draw ID
            cv2.putText(frame, 
                       f"Cup #{track_id}", 
                       (int(ltrb[0]), int(ltrb[1] - 10)),
                       cv2.FONT_HERSHEY_SIMPLEX, 
                       0.9, 
                       (0, 255, 0), 
                       2)
        
        return frame

    def process_video(self, input_path: str) -> Optional[str]:
        """Process entire video file and return path to processed output"""
        try:
            # Open video file
            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                raise ValueError("Could not open video file")

            # Get video properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            # Create output video writer
            output_path = str(Path(input_path).with_suffix('.processed.mp4'))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Process frame
                processed_frame = self.process_frame(frame)
                out.write(processed_frame)

                frame_count += 1
                if frame_count % 30 == 0:
                    logger.info(f"Processed {frame_count}/{total_frames} frames")

            # Cleanup
            cap.release()
            out.release()
            
            return output_path

        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            raise

        finally:
            cv2.destroyAllWindows()
