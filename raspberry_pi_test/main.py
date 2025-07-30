#!/usr/bin/env python3
"""
Script test mô hình realtime trên Raspberry Pi 5
Thu thập ảnh và nhãn khi detect được object
"""

import cv2
import numpy as np
import os
import time
import json
from datetime import datetime
from ultralytics import YOLO

class RealtimeDataCollector:
    def __init__(self):
        # Cấu hình
        self.model_path = "../weights/best.pt"  # hoặc best.torchscript
        self.confidence_threshold = 0.25
        self.save_interval = 2.0  # Lưu ảnh mỗi 2 giây khi detect
        
        # Thư mục lưu dữ liệu
        self.images_dir = "data/images"
        self.labels_dir = "data/labels"
        
        # Tạo thư mục nếu chưa có
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.labels_dir, exist_ok=True)
        
        # Khởi tạo model và camera
        self.model = None
        self.camera = None
        self.last_save_time = 0
        self.detection_count = 0
        
        # Class names (từ metadata.yaml)
        self.class_names = {0: "hands"}
        
    def load_model(self):
        """Load YOLO model"""
        try:
            print("🔄 Loading model...")
            self.model = YOLO(self.model_path)
            print("✅ Model loaded successfully!")
            return True
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def initialize_camera(self):
        """Khởi tạo camera"""
        try:
            print("🔄 Initializing camera...")
            self.camera = cv2.VideoCapture(0)
            
            # Cấu hình camera
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            if not self.camera.isOpened():
                print("❌ Cannot open camera!")
                return False
            
            print("✅ Camera initialized successfully!")
            return True
        except Exception as e:
            print(f"❌ Error initializing camera: {e}")
            return False
    
    def save_detection_data(self, frame, detections):
        """Lưu ảnh và nhãn khi detect được object"""
        current_time = time.time()
        
        # Chỉ lưu nếu đã qua khoảng thời gian save_interval
        if current_time - self.last_save_time < self.save_interval:
            return
        
        # Tạo timestamp cho tên file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        
        # Lưu ảnh
        image_path = os.path.join(self.images_dir, f"detection_{timestamp}.jpg")
        cv2.imwrite(image_path, frame)
        
        # Tạo file nhãn YOLO format
        label_path = os.path.join(self.labels_dir, f"detection_{timestamp}.txt")
        
        with open(label_path, 'w') as f:
            for detection in detections:
                # Lấy thông tin detection
                bbox = detection["bbox"]  # [x1, y1, x2, y2]
                class_id = detection["class_id"]
                conf = detection["confidence"]
                
                # Chuyển đổi sang YOLO format (center_x, center_y, width, height)
                img_height, img_width = frame.shape[:2]
                
                center_x = (bbox[0] + bbox[2]) / 2 / img_width
                center_y = (bbox[1] + bbox[3]) / 2 / img_height
                width = (bbox[2] - bbox[0]) / img_width
                height = (bbox[3] - bbox[1]) / img_height
                
                # Ghi nhãn theo format YOLO: class_id center_x center_y width height
                f.write(f"{class_id} {center_x:.6f} {center_y:.6f} {width:.6f} {height:.6f}\n")
        
        self.last_save_time = current_time
        self.detection_count += 1
        
        print(f"💾 Saved detection data: {image_path}")
        print(f"   Labels: {label_path}")
        print(f"   Total detections saved: {self.detection_count}")
    
    def draw_detections(self, frame, detections):
        """Vẽ detections lên frame"""
        for detection in detections:
            bbox = detection["bbox"]
            class_name = detection["class_name"]
            conf = detection["confidence"]
            
            # Vẽ bounding box
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            
            # Vẽ label
            label = f"{class_name}: {conf:.2f}"
            cv2.putText(frame, label, (bbox[0], bbox[1]-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame
    
    def run(self):
        """Chạy detection realtime"""
        print("🚀 Starting realtime detection and data collection...")
        print(f"📁 Saving images to: {self.images_dir}")
        print(f"📁 Saving labels to: {self.labels_dir}")
        print("Press 'q' to quit")
        
        while True:
            # Đọc frame từ camera
            ret, frame = self.camera.read()
            if not ret:
                print("❌ Failed to read frame from camera")
                break
            
            # Thực hiện detection
            results = self.model(frame, conf=self.confidence_threshold, verbose=False)
            
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
                        class_name = self.class_names.get(cls, f"class_{cls}")
                        
                        detection = {
                            "bbox": [int(x1), int(y1), int(x2), int(y2)],
                            "class_id": cls,
                            "class_name": class_name,
                            "confidence": float(conf)
                        }
                        detections.append(detection)
            
            # Lưu dữ liệu nếu có detection
            if detections:
                self.save_detection_data(frame, detections)
            
            # Vẽ detections lên frame
            frame = self.draw_detections(frame, detections)
            
            # Hiển thị thông tin
            cv2.putText(frame, f"Detections: {len(detections)}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Saved: {self.detection_count}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Hiển thị frame
            cv2.imshow("Realtime Detection", frame)
            
            # Kiểm tra phím thoát
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        self.camera.release()
        cv2.destroyAllWindows()
        print(f"\n✅ Data collection completed!")
        print(f"📊 Total detections saved: {self.detection_count}")

def main():
    # Tạo collector
    collector = RealtimeDataCollector()
    
    # Load model
    if not collector.load_model():
        print("❌ Failed to load model!")
        return
    
    # Khởi tạo camera
    if not collector.initialize_camera():
        print("❌ Failed to initialize camera!")
        return
    
    # Chạy detection
    try:
        collector.run()
    except KeyboardInterrupt:
        print("\n⏹️ Stopped by user")
    except Exception as e:
        print(f"❌ Error during execution: {e}")

if __name__ == "__main__":
    main() 