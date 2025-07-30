"""
YOLO Detector Module
"""

import cv2
import time
import numpy as np
from ultralytics import YOLO
from configs.settings import MODEL_PATH, CONFIDENCE_THRESHOLD, CLASS_NAMES
from utils.logger import system_logger

class YOLODetector:
    def __init__(self):
        self.model = None
        self.is_loaded = False
        
    def load_model(self):
        """Load model YOLO"""
        try:
            system_logger.info(f"Loading model from {MODEL_PATH}...")
            self.model = YOLO(MODEL_PATH, task='detect')
            self.is_loaded = True
            system_logger.info("Model loaded successfully!")
            return True
        except Exception as e:
            system_logger.error(f"Model loading failed: {e}")
            self.is_loaded = False
            return False
    
    def detect(self, frame):
        """Thực hiện detection trên frame"""
        if not self.is_loaded:
            return []
        
        try:
            # Thực hiện detection
            results = self.model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
            
            detections = []
            for result in results:
                if result.boxes is not None:
                    boxes = result.boxes
                    for box in boxes:
                        # Lấy thông tin detection
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        conf = box.conf[0].cpu().numpy()
                        cls = int(box.cls[0].cpu().numpy())
                        
                        # Lấy tên class
                        class_name = CLASS_NAMES.get(cls, f"class_{cls}")
                        
                        detection = {
                            "class": class_name,
                            "confidence": float(conf),
                            "bbox": [int(x1), int(y1), int(x2), int(y2)],
                            "center": [int((x1+x2)/2), int((y1+y2)/2)]
                        }
                        detections.append(detection)
            
            return detections
        except Exception as e:
            system_logger.error(f"Detection error: {e}")
            return []
    
    def draw_detections(self, frame, detections):
        """Vẽ detections lên frame"""
        for detection in detections:
            x1, y1, x2, y2 = detection["bbox"]
            class_name = detection["class"]
            conf = detection["confidence"]
            
            # Vẽ bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Vẽ label
            label = f"{class_name}: {conf:.2f}"
            cv2.putText(frame, label, (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame 