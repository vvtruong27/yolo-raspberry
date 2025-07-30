# Raspberry Pi 5 - YOLO Detection System (Modular)

Hệ thống detection realtime trên Raspberry Pi 5 với cấu trúc module hóa.

## 📁 Cấu trúc thư mục

```
raspberry_pi/
├── main.py                    # Script chính
├── requirements_pi.txt        # Dependencies cho Pi
├── setup_pi.sh               # Script setup tự động
├── README.md                 # Hướng dẫn này
├── configs/
│   └── settings.py           # Cấu hình hệ thống
├── modules/
│   ├── yolo_detector.py      # Module YOLO detection
│   └── camera_manager.py     # Module quản lý camera
├── services/
│   ├── uart_service.py       # Service UART với ESP32
│   └── mqtt_service.py       # Service MQTT với server
├── utils/
│   ├── logger.py             # Utility logging
│   └── performance_monitor.py # Utility monitoring hiệu suất
└── logs/                     # Thư mục chứa log files
```

## 🚀 Cài đặt

### 1. Setup tự động
```bash
cd raspberry_pi
chmod +x setup_pi.sh
./setup_pi.sh
```

### 2. Setup thủ công
```bash
# Cài đặt dependencies hệ thống
sudo apt update
sudo apt install -y python3-pip python3-venv libopencv-dev

# Tạo môi trường ảo
python3 -m venv venv_pi
source venv_pi/bin/activate

# Cài đặt Python packages
pip install -r requirements_pi.txt

# Cấp quyền UART
sudo usermod -a -G dialout $USER
```

## ⚙️ Cấu hình

### 1. UART Settings (configs/settings.py)
```python
UART_PORT = "/dev/ttyUSB0"  # hoặc "/dev/ttyACM0"
UART_BAUDRATE = 115200
```

### 2. MQTT Settings (configs/settings.py)
```python
MQTT_BROKER = "broker.hivemq.com"  # hoặc IP server của bạn
MQTT_PORT = 1883
```

### 3. Model Settings (configs/settings.py)
```python
MODEL_PATH = "../../weights/best_ncnn_model"
CONFIDENCE_THRESHOLD = 0.25
```

## 🎯 Sử dụng

### Chạy thủ công
```bash
cd raspberry_pi
source venv_pi/bin/activate
python main.py
```

### Chạy tự động (service)
```bash
# Bật service
sudo systemctl start yolo-detection.service

# Kiểm tra trạng thái
sudo systemctl status yolo-detection.service

# Xem log
sudo journalctl -u yolo-detection.service -f
```

## 📡 Tính năng

### 1. Realtime Detection
- Camera realtime 640x480 với thread riêng
- Model NCNN tối ưu cho Pi
- Performance monitoring (FPS, CPU, Memory)

### 2. UART Communication
- Gửi lệnh đến ESP32 khi detect
- Thread-safe communication
- Response monitoring từ ESP32

### 3. MQTT Communication
- Gửi dữ liệu detection đến server
- Gửi ảnh detection (base64 encoded)
- Subscribe topics để nhận lệnh từ server

### 4. Logging System
- File logging với rotation
- Console logging
- Performance logging

## 🔧 Troubleshooting

### UART không hoạt động
```bash
# Kiểm tra port
ls /dev/tty*

# Cấp quyền
sudo chmod 666 /dev/ttyUSB0

# Reboot
sudo reboot
```

### Camera không hoạt động
```bash
# Kiểm tra camera
vcgencmd get_camera

# Enable camera
sudo raspi-config
# Interface Options > Camera > Enable
```

### MQTT không kết nối
- Kiểm tra kết nối internet
- Thay đổi MQTT_BROKER trong configs/settings.py
- Kiểm tra firewall

## 📊 Performance

- **FPS**: 15-30 FPS (tùy thuộc Pi model)
- **Inference time**: 50-100ms
- **Memory usage**: ~200-300MB
- **CPU usage**: 60-80%

## 🔄 Cập nhật

```bash
cd raspberry_pi
git pull
source venv_pi/bin/activate
pip install -r requirements_pi.txt
sudo systemctl restart yolo-detection.service
```

## 🏗️ Kiến trúc Module

### Modules
- **YOLODetector**: Xử lý detection
- **CameraManager**: Quản lý camera với threading

### Services
- **UARTService**: Giao tiếp với ESP32
- **MQTTService**: Giao tiếp với server

### Utils
- **SystemLogger**: Logging system
- **PerformanceMonitor**: Monitoring hiệu suất

### Configs
- **settings.py**: Tất cả cấu hình hệ thống 