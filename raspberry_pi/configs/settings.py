"""
Cấu hình chính cho hệ thống Raspberry Pi 5
"""

# Camera settings
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 30

# Model settings
MODEL_PATH = "../../weights/best_ncnn_model"
CONFIDENCE_THRESHOLD = 0.25
DETECTION_INTERVAL = 0.1  # seconds

# UART settings (ESP32 communication)
UART_PORT = "/dev/ttyUSB0"  # hoặc "/dev/ttyACM0"
UART_BAUDRATE = 115200
UART_TIMEOUT = 1

# MQTT settings
MQTT_BROKER = "broker.hivemq.com"  # hoặc IP server của bạn
MQTT_PORT = 1883
MQTT_TOPIC_IMAGE = "fpt_hackathon/detection_image"
MQTT_TOPIC_DATA = "fpt_hackathon/detection_data"
MQTT_CLIENT_ID = "raspberry_pi_5"

# Detection classes
CLASS_NAMES = {
    0: "hands",
    # Thêm các class khác nếu có
}

# ESP32 commands
ESP32_COMMANDS = {
    "hands": "HANDS_DETECTED",
    "stop": "STOP",
    "forward": "FORWARD",
    "backward": "BACKWARD",
    "left": "LEFT",
    "right": "RIGHT"
}

# Logging settings
LOG_LEVEL = "INFO"
LOG_FILE = "logs/system.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Performance settings
MAX_FPS = 30
MIN_INFERENCE_TIME = 50  # ms 