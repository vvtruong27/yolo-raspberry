#!/bin/bash

echo "🚀 Setup Raspberry Pi 5 cho YOLO Detection..."

# Cập nhật hệ thống
echo "📦 Cập nhật hệ thống..."
sudo apt update && sudo apt upgrade -y

# Cài đặt dependencies cần thiết
echo "📥 Cài đặt dependencies..."
sudo apt install -y python3-pip python3-venv
sudo apt install -y libopencv-dev python3-opencv
sudo apt install -y libatlas-base-dev
sudo apt install -y libhdf5-dev libhdf5-serial-dev
sudo apt install -y libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5

# Tạo môi trường ảo
echo "🔧 Tạo môi trường ảo..."
python3 -m venv venv_pi
source venv_pi/bin/activate

# Cập nhật pip
echo "⬆️ Cập nhật pip..."
pip install --upgrade pip

# Cài đặt dependencies Python
echo "📥 Cài đặt Python packages..."
pip install -r requirements_pi.txt

# Cấp quyền cho UART
echo "🔧 Cấu hình UART..."
sudo usermod -a -G dialout $USER
echo "✅ Đã thêm user vào group dialout"
echo "⚠️ Cần reboot để UART hoạt động!"

# Tạo service để tự động chạy
echo "🔧 Tạo systemd service..."
sudo tee /etc/systemd/system/yolo-detection.service > /dev/null <<EOF
[Unit]
Description=YOLO Detection Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv_pi/bin
ExecStart=$(pwd)/venv_pi/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Kích hoạt service
sudo systemctl daemon-reload
sudo systemctl enable yolo-detection.service

echo "✅ Setup hoàn tất!"
echo ""
echo "💡 Để chạy thủ công:"
echo "   source venv_pi/bin/activate"
echo "   python main.py"
echo ""
echo "💡 Để chạy tự động:"
echo "   sudo systemctl start yolo-detection.service"
echo "   sudo systemctl status yolo-detection.service"
echo ""
echo "💡 Để xem log:"
echo "   sudo journalctl -u yolo-detection.service -f"
echo ""
echo "⚠️ Nhớ reboot để UART hoạt động!" 