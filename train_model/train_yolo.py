"""
Script train YOLOv8n để nhận diện biển báo giao thông
Tối ưu để deploy trên Raspberry Pi 5 (train trên GPU mạnh)
"""

import yaml
from ultralytics import YOLO
import torch
import os

print("\n💻 KIỂM TRA PHẦN CỨNG TRAINING")
print("=" * 50)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name())
    print(f"Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    print("✅ Sử dụng GPU để training nhanh hơn")
else:
    print("⚠️  Training trên CPU (sẽ chậm hơn)")

# Khởi tạo model YOLOv8n với pretrained weights
model = YOLO('yolov8n.pt')

# Cấu hình các hyperparameters
train_params = {
    'data': "dataset.yaml",          # File cấu hình dataset
    'epochs': 30,                   # Số epoch
    'patience': 15,                  # Early stopping
    'batch': -1,                     # Auto batch size
    'workers': 8,                   # Số worker
    'name': 'fpt_hackathon',        # Tên experiment
    'exist_ok': True,                # Ghi đè nếu đã tồn tại
    'cache': True,                   # Cache dữ liệu
    'cos_lr': True,                  # Sử dụng cosine LR scheduler
    'close_mosaic': 10,              # Đóng mosaic sau 10 epoch
}

# # Cấu hình hyperparameters (chỉ các tham số khác mặc định)
# train_params = {
#         'data': "dataset.yaml",          # File cấu hình dataset
#         'epochs': 200,                   # Mặc định: 100
#         'patience': 30,                  # Mặc định: 100
#         'batch': -1,                     # Auto batch size (mặc định: 16)
#         'workers': 16,                   # Mặc định: 8
#         'name': 'fpt_hackathon',        # Mặc định: None
#         'exist_ok': True,                # Mặc định: False
#         'cache': True,                   # Mặc định: False
#         'cos_lr': True,                  # Mặc định: False
#         'close_mosaic': 10,              # Mặc định: 0
#     }

print("📊 Training parameters:")
for k, v in train_params.items():
    print(f"{k}: {v}")

print("\n=== 🔧 BẮT ĐẦU TRAINING ===")
results = model.train(**train_params)

print("\n=== 📤 BẮT ĐẦU EXPORT ===")
try:
    export_path = model.export(format='ncnn')
    print(f"✅ Export thành công: {export_path}")
except Exception as e:
    export_path = None
    print(f"❌ Export thất bại: {e}")

# Lấy đường dẫn đến best model
best_model_path = os.path.join('runs', 'detect', 'fpt_hackathon', 'weights', 'best.pt')

if export_path and os.path.exists(best_model_path):
    print("\n🎉 HOÀN TẤT QUÁ TRÌNH TRAIN & EXPORT!")
    print(f"📁 PyTorch model: {best_model_path}")
    print(f"📱 NCNN model directory: {export_path}")
    size_mb = os.path.getsize(best_model_path) / (1024*1024)
    print(f"📊 Kích thước model (PyTorch): {size_mb:.2f} MB")
    
    # Kiểm tra kích thước NCNN model files
    ncnn_param_path = os.path.join(export_path, 'model.ncnn.param')
    ncnn_bin_path = os.path.join(export_path, 'model.ncnn.bin')
    
    if os.path.exists(ncnn_param_path) and os.path.exists(ncnn_bin_path):
        param_size_mb = os.path.getsize(ncnn_param_path) / (1024*1024)
        bin_size_mb = os.path.getsize(ncnn_bin_path) / (1024*1024)
        total_ncnn_size = param_size_mb + bin_size_mb
        print(f"📊 Kích thước NCNN param: {param_size_mb:.2f} MB")
        print(f"📊 Kích thước NCNN bin: {bin_size_mb:.2f} MB")
        print(f"📊 Tổng kích thước NCNN: {total_ncnn_size:.2f} MB")
    else:
        print("⚠️ Không tìm thấy file NCNN model")
else:
    print("⚠️ Không export được model sang NCNN hoặc không tìm thấy best model.")