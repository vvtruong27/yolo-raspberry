#!/usr/bin/env python3
"""
Simple Realtime NCNN Model Test
Test NCNN model với camera realtime
"""

import cv2
import time
from ultralytics import YOLO

def main():
    # Load NCNN model
    print("🔄 Loading NCNN model...")
    model = YOLO("weights/best_ncnn_model")
    print("✅ Model loaded!")
    
    # Mở camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print("❌ Cannot open camera!")
        return
    
    print("🎥 Camera opened!")
    print("💡 Press 'q' to quit")
    
    # Performance tracking
    fps = 0
    frame_count = 0
    start_time = time.time()
    
    while True:
        # Đọc frame
        ret, frame = cap.read()
        if not ret:
            print("❌ Cannot read frame!")
            break
        
        # Detect
        start_inference = time.time()
        results = model(frame, conf=0.25, verbose=False)
        inference_time = (time.time() - start_inference) * 1000
        
        # Vẽ kết quả
        for result in results:
            if result.boxes is not None:
                boxes = result.boxes
                for box in boxes:
                    # Lấy tọa độ
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = box.conf[0].cpu().numpy()
                    
                    # Vẽ bounding box
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    
                    # Vẽ label
                    label = f"Hand: {conf:.2f}"
                    cv2.putText(frame, label, (int(x1), int(y1)-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Tính FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            fps = frame_count / elapsed_time
        
        # Vẽ stats
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Inference: {inference_time:.1f}ms", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Hiển thị
        cv2.imshow('NCNN Realtime Test', frame)
        
        # Kiểm tra key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Exited!")

if __name__ == "__main__":
    main() 