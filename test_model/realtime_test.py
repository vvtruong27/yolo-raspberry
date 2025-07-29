#!/usr/bin/env python3
"""
Test mô hình NCNN realtime với camera
"""

import cv2
import time
from ultralytics import YOLO

def main():
    # Load model NCNN
    print("🔄 Đang load model NCNN...")
    model = YOLO("weights/best_ncnn_model", task='detect')
    print("✅ Model đã load xong!")
    
    # Mở camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print("❌ Không thể mở camera!")
        return
    
    print("🎥 Camera đã mở!")
    print("💡 Nhấn 'q' để thoát")
    
    # Theo dõi FPS
    fps = 0
    frame_count = 0
    start_time = time.time()
    
    while True:
        # Đọc frame
        ret, frame = cap.read()
        if not ret:
            print("❌ Không thể đọc frame!")
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
                    cls = int(box.cls[0].cpu().numpy())
                    
                    # Lấy tên class
                    class_name = model.names[cls]
                    
                    # Vẽ bounding box
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    
                    # Vẽ label
                    label = f"{class_name}: {conf:.2f}"
                    cv2.putText(frame, label, (int(x1), int(y1)-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Tính FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            fps = frame_count / elapsed_time
        
        # Vẽ thông tin
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Inference: {inference_time:.1f}ms", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Hiển thị
        cv2.imshow('NCNN Realtime Test', frame)
        
        # Kiểm tra phím
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Dọn dẹp
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Đã thoát!")

if __name__ == "__main__":
    main() 