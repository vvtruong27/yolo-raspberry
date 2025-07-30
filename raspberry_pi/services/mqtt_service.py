"""
MQTT Service cho server communication
"""

import paho.mqtt.client as mqtt
import json
import base64
import cv2
import threading
import time
from configs.settings import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC_IMAGE, MQTT_TOPIC_DATA, MQTT_CLIENT_ID
from utils.logger import system_logger

class MQTTService:
    def __init__(self):
        self.client = mqtt.Client(MQTT_CLIENT_ID)
        self.is_connected = False
        self.lock = threading.Lock()
        
        # Setup callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message
        
    def on_connect(self, client, userdata, flags, rc):
        """Callback khi kết nối MQTT"""
        if rc == 0:
            self.is_connected = True
            system_logger.info(f"MQTT connected to {MQTT_BROKER}")
        else:
            system_logger.error(f"MQTT connection failed with code {rc}")
    
    def on_disconnect(self, client, userdata, rc):
        """Callback khi ngắt kết nối MQTT"""
        self.is_connected = False
        system_logger.info("MQTT disconnected")
    
    def on_publish(self, client, userdata, mid):
        """Callback khi publish thành công"""
        system_logger.debug(f"MQTT published message ID: {mid}")
    
    def on_message(self, client, userdata, msg):
        """Callback khi nhận message"""
        try:
            payload = msg.payload.decode()
            system_logger.info(f"MQTT received on {msg.topic}: {payload}")
            self.handle_message(msg.topic, payload)
        except Exception as e:
            system_logger.error(f"Error handling MQTT message: {e}")
    
    def handle_message(self, topic, payload):
        """Xử lý message nhận được"""
        # Có thể thêm logic xử lý message ở đây
        pass
    
    def connect(self):
        """Kết nối MQTT"""
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_start()
            system_logger.info("MQTT connection initiated")
            return True
        except Exception as e:
            system_logger.error(f"MQTT connection error: {e}")
            return False
    
    def disconnect(self):
        """Ngắt kết nối MQTT"""
        if self.is_connected:
            self.client.loop_stop()
            self.client.disconnect()
            system_logger.info("MQTT disconnected")
    
    def send_detection_data(self, detections):
        """Gửi dữ liệu detection đến server"""
        if not self.is_connected:
            return False
        
        try:
            with self.lock:
                data = {
                    "timestamp": time.time(),
                    "detections": detections,
                    "device": "raspberry_pi_5"
                }
                
                message = json.dumps(data)
                result = self.client.publish(MQTT_TOPIC_DATA, message)
                return result.rc == mqtt.MQTT_ERR_SUCCESS
        except Exception as e:
            system_logger.error(f"MQTT send data error: {e}")
            return False
    
    def send_image(self, frame, detections):
        """Gửi ảnh detection đến server"""
        if not self.is_connected:
            return False
        
        try:
            with self.lock:
                # Encode ảnh thành base64
                _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                image_base64 = base64.b64encode(buffer).decode('utf-8')
                
                data = {
                    "timestamp": time.time(),
                    "image": image_base64,
                    "detections": detections,
                    "device": "raspberry_pi_5"
                }
                
                message = json.dumps(data)
                result = self.client.publish(MQTT_TOPIC_IMAGE, message)
                return result.rc == mqtt.MQTT_ERR_SUCCESS
        except Exception as e:
            system_logger.error(f"MQTT send image error: {e}")
            return False
    
    def send_custom_data(self, topic, data):
        """Gửi dữ liệu tùy chỉnh"""
        if not self.is_connected:
            return False
        
        try:
            with self.lock:
                message = json.dumps(data)
                result = self.client.publish(topic, message)
                return result.rc == mqtt.MQTT_ERR_SUCCESS
        except Exception as e:
            system_logger.error(f"MQTT send custom data error: {e}")
            return False
    
    def subscribe_topic(self, topic):
        """Subscribe topic"""
        if self.is_connected:
            self.client.subscribe(topic)
            system_logger.info(f"Subscribed to topic: {topic}")
    
    def get_connection_status(self):
        """Lấy trạng thái kết nối"""
        return {
            "connected": self.is_connected,
            "broker": MQTT_BROKER,
            "port": MQTT_PORT,
            "client_id": MQTT_CLIENT_ID
        } 