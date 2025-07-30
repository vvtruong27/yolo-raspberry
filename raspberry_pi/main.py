#!/usr/bin/env python3
"""
Main script cho Raspberry Pi 5 - Cấu trúc module hóa
Realtime detection + UART + MQTT
"""

import cv2
import time
import threading
import signal
import sys
import os

# Thêm đường dẫn để import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from configs.settings import CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_FPS, DETECTION_INTERVAL
from modules.yolo_detector import YOLODetector
from modules.camera_manager import CameraManager
from services.uart_service import UARTService
from services.mqtt_service import MQTTService
from utils.performance_monitor import PerformanceMonitor
from utils.logger import system_logger

class RaspberryPiSystem:
    def __init__(self):
        self.running = False
        
        # Khởi tạo các components
        self.detector = YOLODetector()
        self.camera_manager = CameraManager()
        self.uart_service = UARTService()
        self.mqtt_service = MQTTService()
        self.performance_monitor = PerformanceMonitor()
        
        # Detection tracking
        self.last_detection_time = 0
        self.last_detections = []
        
    def setup(self):
        """Khởi tạo hệ thống"""
        system_logger.info("🚀 Khởi tạo hệ thống Raspberry Pi 5...")
        
        # Load model
        if not self.detector.load_model():
            system_logger.error("❌ Không thể load model!")
            return False
        
        # Khởi tạo camera
        if not self.camera_manager.initialize():
            system_logger.error("❌ Không thể khởi tạo camera!")
            return False
        
        # Bắt đầu camera capture
        if not self.camera_manager.start_capture():
            system_logger.error("❌ Không thể bắt đầu camera capture!")
            return False
        
        # Kết nối UART
        if not self.uart_service.connect():
            system_logger.warning("⚠️ Không thể kết nối UART, tiếp tục không có UART...")
        
        # Kết nối MQTT
        if not self.mqtt_service.connect():
            system_logger.warning("⚠️ Không thể kết nối MQTT, tiếp tục không có MQTT...")
        
        # Bắt đầu performance monitoring
        self.performance_monitor.start_monitoring()
        
        system_logger.info("✅ Hệ thống khởi tạo thành công!")
        return True
    
    def process_frame(self, frame):
        """Xử lý một frame"""
        # Thực hiện detection
        start_inference = time.time()
        detections = self.detector.detect(frame)
        inference_time = (time.time() - start_inference) * 1000
        
        # Cập nhật performance monitor
        self.performance_monitor.update_fps()
        self.performance_monitor.add_inference_time(inference_time)
        
        # Vẽ detections
        frame = self.detector.draw_detections(frame, detections)
        
        # Lấy performance stats
        stats = self.performance_monitor.get_performance_stats()
        
        # Vẽ thông tin
        cv2.putText(frame, f"FPS: {stats['fps']:.1f}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Inference: {inference_time:.1f}ms", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Detections: {len(detections)}", (10, 110), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"CPU: {stats['cpu_usage']:.1f}%", (10, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Xử lý detections
        if detections:
            self.handle_detections(detections, frame)
        
        return frame
    
    def handle_detections(self, detections, frame):
        """Xử lý khi có detections"""
        current_time = time.time()
        
        # Chỉ xử lý nếu đã qua khoảng thời gian interval
        if current_time - self.last_detection_time > DETECTION_INTERVAL:
            self.last_detection_time = current_time
            self.last_detections = detections
            
            # Gửi lệnh đến ESP32
            for detection in detections:
                class_name = detection["class"]
                confidence = detection["confidence"]
                self.uart_service.send_detection(class_name, confidence)
            
            # Gửi dữ liệu đến MQTT
            self.mqtt_service.send_detection_data(detections)
            
            # Gửi ảnh đến MQTT (chỉ khi có detection)
            self.mqtt_service.send_image(frame, detections)
    
    def run(self):
        """Chạy hệ thống chính"""
        system_logger.info("🎥 Bắt đầu chạy hệ thống...")
        print("💡 Nhấn 'q' để thoát")
        
        self.running = True
        
        while self.running:
            # Lấy frame từ camera manager
            frame = self.camera_manager.get_frame()
            if frame is None:
                time.sleep(0.01)
                continue
            
            # Xử lý frame
            processed_frame = self.process_frame(frame)
            
            # Hiển thị
            cv2.imshow('Raspberry Pi 5 - YOLO Detection', processed_frame)
            
            # Kiểm tra phím
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        
        self.cleanup()
    
    def cleanup(self):
        """Dọn dẹp tài nguyên"""
        system_logger.info("🧹 Đang dọn dẹp...")
        self.running = False
        
        # Dừng performance monitoring
        self.performance_monitor.stop_monitoring()
        
        # Dừng camera
        self.camera_manager.stop_capture()
        self.camera_manager.release()
        
        # Ngắt kết nối services
        self.uart_service.disconnect()
        self.mqtt_service.disconnect()
        
        cv2.destroyAllWindows()
        system_logger.info("👋 Đã thoát!")
    
    def signal_handler(self, sig, frame):
        """Xử lý signal để thoát an toàn"""
        system_logger.info("🛑 Nhận signal, đang thoát...")
        self.cleanup()
        sys.exit(0)

def main():
    # Đăng ký signal handler
    signal.signal(signal.SIGINT, lambda sig, frame: None)
    
    # Tạo và chạy hệ thống
    system = RaspberryPiSystem()
    
    if system.setup():
        system.run()
    else:
        system_logger.error("❌ Khởi tạo hệ thống thất bại!")

if __name__ == "__main__":
    main() 