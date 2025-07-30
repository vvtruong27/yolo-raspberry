# Raspberry Pi 5 - Realtime Data Collection

Script đơn giản để test mô hình YOLO realtime trên Raspberry Pi 5 và thu thập dữ liệu.

## 📁 Cấu trúc thư mục

```
raspberry_pi_test/
├── main.py              # Script chính
├── requirements.txt     # Dependencies
├── README.md           # Hướng dẫn này
└── data/               # Thư mục lưu dữ liệu (tự động tạo)
    ├── images/         # Ảnh được lưu khi detect
    └── labels/         # Nhãn YOLO format
```

## 🚀 Cài đặt

### 1. Tạo môi trường ảo
```bash
cd raspberry_pi_test
python3 -m venv venv
source venv/bin/activate
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

## 🎯 Sử dụng

### Chạy script
```bash
python main.py
```

### Tính năng
- **Realtime Detection**: Chạy detection realtime với camera
- **Auto Save**: Tự động lưu ảnh và nhãn khi detect được object
- **YOLO Format**: Nhãn được lưu theo format YOLO chuẩn
- **Interval Control**: Chỉ lưu mỗi 2 giây để tránh spam

### Cấu hình
Trong `main.py`, bạn có thể thay đổi:
- `model_path`: Đường dẫn đến model (best.pt hoặc best.torchscript)
- `confidence_threshold`: Ngưỡng confidence (mặc định 0.25)
- `save_interval`: Khoảng thời gian giữa các lần lưu (mặc định 2.0s)

## 📊 Dữ liệu thu thập

### Ảnh
- Được lưu trong `data/images/`
- Format: `detection_YYYYMMDD_HHMMSS_microseconds.jpg`
- Chỉ lưu khi có detection

### Nhãn
- Được lưu trong `data/labels/`
- Format: `detection_YYYYMMDD_HHMMSS_microseconds.txt`
- YOLO format: `class_id center_x center_y width height`

## 🎮 Điều khiển

- **'q'**: Thoát chương trình
- **Ctrl+C**: Dừng chương trình

## 📈 Thống kê

Script sẽ hiển thị:
- Số lượng detections hiện tại
- Số lượng ảnh đã lưu
- Thông tin về file được lưu

## 🔧 Troubleshooting

### Camera không hoạt động
```bash
# Kiểm tra camera
vcgencmd get_camera

# Enable camera
sudo raspi-config
# Interface Options > Camera > Enable
```

### Model không load được
- Kiểm tra đường dẫn model trong `main.py`
- Đảm bảo file model tồn tại
- Thử với `best.torchscript` thay vì `best.pt`

### Performance
- FPS: 15-30 FPS (tùy thuộc Pi model)
- Memory usage: ~200-300MB
- CPU usage: 60-80%

## 📝 Ghi chú

- Script này chỉ tập trung vào thu thập dữ liệu
- Không có giao tiếp UART/MQTT
- Dữ liệu thu thập có thể dùng để train thêm model
- Đảm bảo có đủ dung lượng ổ cứng để lưu ảnh 