"""
UART Service cho ESP32 communication
"""

import serial
import time
import threading
from configs.settings import UART_PORT, UART_BAUDRATE, UART_TIMEOUT, ESP32_COMMANDS
from utils.logger import system_logger

class UARTService:
    def __init__(self):
        self.serial = None
        self.is_connected = False
        self.lock = threading.Lock()
        self.is_running = False
        self.response_thread = None
        
    def connect(self):
        """Kết nối UART với ESP32"""
        try:
            self.serial = serial.Serial(
                port=UART_PORT,
                baudrate=UART_BAUDRATE,
                timeout=UART_TIMEOUT
            )
            self.is_connected = True
            system_logger.info(f"UART connected to {UART_PORT}")
            
            # Bắt đầu thread đọc response
            self.start_response_monitor()
            
            return True
        except Exception as e:
            system_logger.error(f"UART connection failed: {e}")
            self.is_connected = False
            return False
    
    def disconnect(self):
        """Ngắt kết nối UART"""
        self.stop_response_monitor()
        if self.serial and self.serial.is_open:
            self.serial.close()
        self.is_connected = False
        system_logger.info("UART disconnected")
    
    def start_response_monitor(self):
        """Bắt đầu monitor response từ ESP32"""
        self.is_running = True
        self.response_thread = threading.Thread(target=self._response_loop)
        self.response_thread.daemon = True
        self.response_thread.start()
        system_logger.info("UART response monitor started")
    
    def stop_response_monitor(self):
        """Dừng monitor response"""
        self.is_running = False
        if self.response_thread:
            self.response_thread.join()
        system_logger.info("UART response monitor stopped")
    
    def _response_loop(self):
        """Loop đọc response từ ESP32"""
        while self.is_running and self.is_connected:
            try:
                if self.serial.in_waiting > 0:
                    response = self.serial.readline().decode().strip()
                    if response:
                        system_logger.info(f"UART received: {response}")
                        self.handle_response(response)
            except Exception as e:
                system_logger.error(f"UART read error: {e}")
                time.sleep(0.1)
    
    def handle_response(self, response):
        """Xử lý response từ ESP32"""
        # Có thể thêm logic xử lý response ở đây
        pass
    
    def send_command(self, command):
        """Gửi lệnh đến ESP32"""
        if not self.is_connected:
            return False
        
        try:
            with self.lock:
                # Thêm ký tự xuống dòng để ESP32 nhận biết
                message = f"{command}\n"
                self.serial.write(message.encode())
                self.serial.flush()
                system_logger.info(f"UART sent: {command}")
                return True
        except Exception as e:
            system_logger.error(f"UART send error: {e}")
            return False
    
    def send_detection(self, class_name, confidence):
        """Gửi thông tin detection đến ESP32"""
        if class_name in ESP32_COMMANDS:
            command = ESP32_COMMANDS[class_name]
            return self.send_command(command)
        return False
    
    def send_custom_command(self, command):
        """Gửi lệnh tùy chỉnh"""
        return self.send_command(command)
    
    def get_connection_status(self):
        """Lấy trạng thái kết nối"""
        return {
            "connected": self.is_connected,
            "port": UART_PORT,
            "baudrate": UART_BAUDRATE
        } 