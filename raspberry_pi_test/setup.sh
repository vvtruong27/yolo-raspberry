#!/bin/bash

echo "🚀 Setup Raspberry Pi 5 cho Data Collection..."

# Cập nhật hệ thống
echo "📦 Cập nhật hệ thống..."
sudo apt update && sudo apt upgrade -y

# Cài đặt dependencies cần thiết
echo "📥 Cài đặt dependencies..."
sudo apt install -y python3-pip python3-venv
sudo apt install -y libopencv-dev python3-opencv
sudo apt install -y libatlas-base-dev

# Tạo môi trường ảo
echo "🔧 Tạo môi trường ảo..."
python3 -m venv venv
source venv/bin/activate

# Cập nhật pip
echo "⬆️ Cập nhật pip..."
pip install --upgrade pip

# Cài đặt dependencies Python
echo "📥 Cài đặt Python packages..."
pip install -r requirements.txt

# Tạo thư mục data
echo "📁 Tạo thư mục data..."
mkdir -p data/images
mkdir -p data/labels

echo "✅ Setup hoàn tất!"
echo ""
echo "💡 Để chạy:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "💡 Để thoát:"
echo "   Nhấn 'q' trong cửa sổ camera"
echo ""
echo "📊 Dữ liệu sẽ được lưu trong:"
echo "   data/images/ - Ảnh detection"
echo "   data/labels/ - Nhãn YOLO format" 