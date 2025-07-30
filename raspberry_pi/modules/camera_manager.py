"""
Camera Manager Module
"""

import cv2
import threading
import time
from configs.settings import CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_FPS
from utils.logger import system_logger

class CameraManager:
    def __init__(self):
        self.camera = None
        self.is_running = False
        self.current_frame = None
        self.frame_lock = threading.Lock()
        self.camera_thread = None
        
    def initialize(self):
        """Khởi tạo camera"""
        try:
            self.camera = cv2.VideoCapture(0)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
            self.camera.set(cv2.CAP_PROP_FPS, CAMERA_FPS)
            
            if not self.camera.isOpened():
                system_logger.error("Cannot open camera!")
                return False
            
            system_logger.info("Camera initialized successfully")
            return True
        except Exception as e:
            system_logger.error(f"Camera initialization failed: {e}")
            return False
    
    def start_capture(self):
        """Bắt đầu capture frames"""
        if not self.camera:
            system_logger.error("Camera not initialized!")
            return False
        
        self.is_running = True
        self.camera_thread = threading.Thread(target=self._capture_loop)
        self.camera_thread.daemon = True
        self.camera_thread.start()
        system_logger.info("Camera capture started")
        return True
    
    def stop_capture(self):
        """Dừng capture frames"""
        self.is_running = False
        if self.camera_thread:
            self.camera_thread.join()
        system_logger.info("Camera capture stopped")
    
    def _capture_loop(self):
        """Loop capture frames"""
        while self.is_running:
            try:
                ret, frame = self.camera.read()
                if ret:
                    with self.frame_lock:
                        self.current_frame = frame.copy()
                else:
                    system_logger.warning("Failed to read frame from camera")
                    time.sleep(0.1)
            except Exception as e:
                system_logger.error(f"Camera capture error: {e}")
                time.sleep(0.1)
    
    def get_frame(self):
        """Lấy frame hiện tại"""
        with self.frame_lock:
            if self.current_frame is not None:
                return self.current_frame.copy()
        return None
    
    def release(self):
        """Giải phóng camera"""
        self.stop_capture()
        if self.camera:
            self.camera.release()
        system_logger.info("Camera released")
    
    def get_camera_info(self):
        """Lấy thông tin camera"""
        if not self.camera:
            return None
        
        try:
            width = int(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = self.camera.get(cv2.CAP_PROP_FPS)
            
            return {
                "width": width,
                "height": height,
                "fps": fps,
                "is_opened": self.camera.isOpened()
            }
        except Exception as e:
            system_logger.error(f"Error getting camera info: {e}")
            return None 