"""
Performance monitoring utility
"""

import time
import psutil
import threading
from utils.logger import system_logger

class PerformanceMonitor:
    def __init__(self):
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        self.inference_times = []
        self.cpu_usage = 0
        self.memory_usage = 0
        self.is_monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self):
        """Bắt đầu monitoring"""
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        system_logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Dừng monitoring"""
        self.is_monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        system_logger.info("Performance monitoring stopped")
    
    def _monitor_loop(self):
        """Loop monitoring performance"""
        while self.is_monitoring:
            try:
                # CPU usage
                self.cpu_usage = psutil.cpu_percent(interval=1)
                
                # Memory usage
                memory = psutil.virtual_memory()
                self.memory_usage = memory.percent
                
                # Log performance mỗi 10 giây
                if int(time.time()) % 10 == 0:
                    system_logger.info(f"Performance - CPU: {self.cpu_usage}%, Memory: {self.memory_usage}%, FPS: {self.fps:.1f}")
                
                time.sleep(1)
            except Exception as e:
                system_logger.error(f"Performance monitoring error: {e}")
    
    def update_fps(self):
        """Cập nhật FPS"""
        self.frame_count += 1
        elapsed_time = time.time() - self.start_time
        if elapsed_time > 0:
            self.fps = self.frame_count / elapsed_time
    
    def add_inference_time(self, inference_time):
        """Thêm thời gian inference"""
        self.inference_times.append(inference_time)
        
        # Giữ chỉ 100 giá trị gần nhất
        if len(self.inference_times) > 100:
            self.inference_times.pop(0)
    
    def get_avg_inference_time(self):
        """Lấy thời gian inference trung bình"""
        if self.inference_times:
            return sum(self.inference_times) / len(self.inference_times)
        return 0
    
    def get_performance_stats(self):
        """Lấy thống kê hiệu suất"""
        return {
            "fps": self.fps,
            "avg_inference_time": self.get_avg_inference_time(),
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "frame_count": self.frame_count
        } 