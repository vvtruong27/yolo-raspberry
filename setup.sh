#!/bin/bash

echo "🚀 Bắt đầu setup môi trường YOLO Raspberry Pi..."

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 không được tìm thấy. Vui lòng cài đặt Python3 trước."
    exit 1
fi

# Tạo môi trường ảo
echo "📦 Tạo môi trường ảo..."
python3 -m venv venv

# Kích hoạt môi trường ảo
echo "🔧 Kích hoạt môi trường ảo..."
source venv/bin/activate

# Cập nhật pip
echo "⬆️ Cập nhật pip..."
pip install --upgrade pip

# Cài đặt dependencies
echo "📥 Cài đặt dependencies từ requirements.txt..."
pip install -r requirements.txt

# Kích hoạt môi trường ảo
source venv/bin/activate

echo "✅ Hoàn tất setup!"
echo ""
echo "💡 Để chạy training:"
echo "   cd train_model && python train_yolo.py"
echo ""
echo "💡 Để chạy test realtime:"
echo "   cd test_model && python realtime_test.py" 