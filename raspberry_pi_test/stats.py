#!/usr/bin/env python3
"""
Script xem thống kê dữ liệu đã thu thập
"""

import os
import glob
from datetime import datetime

def get_data_stats():
    """Lấy thống kê dữ liệu đã thu thập"""
    
    images_dir = "data/images"
    labels_dir = "data/labels"
    
    # Kiểm tra thư mục tồn tại
    if not os.path.exists(images_dir):
        print("❌ Thư mục data/images không tồn tại!")
        return
    
    if not os.path.exists(labels_dir):
        print("❌ Thư mục data/labels không tồn tại!")
        return
    
    # Đếm số file
    image_files = glob.glob(os.path.join(images_dir, "*.jpg"))
    label_files = glob.glob(os.path.join(labels_dir, "*.txt"))
    
    print("📊 Thống kê dữ liệu thu thập")
    print("=" * 40)
    print(f"📁 Ảnh: {len(image_files)} files")
    print(f"📁 Nhãn: {len(label_files)} files")
    
    if len(image_files) == 0:
        print("⚠️ Chưa có dữ liệu nào được thu thập!")
        return
    
    # Thống kê theo thời gian
    print("\n📅 Thống kê theo thời gian:")
    
    # Lấy thời gian của file đầu tiên và cuối cùng
    image_files.sort()
    first_image = image_files[0]
    last_image = image_files[-1]
    
    first_time = os.path.getctime(first_image)
    last_time = os.path.getctime(last_image)
    
    first_dt = datetime.fromtimestamp(first_time)
    last_dt = datetime.fromtimestamp(last_time)
    
    print(f"🕐 Bắt đầu: {first_dt.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🕐 Kết thúc: {last_dt.strftime('%Y-%m-%d %H:%M:%S')}")
    
    duration = last_dt - first_dt
    print(f"⏱️ Thời gian thu thập: {duration}")
    
    # Thống kê theo ngày
    print("\n📈 Thống kê theo ngày:")
    daily_stats = {}
    
    for image_file in image_files:
        file_time = os.path.getctime(image_file)
        file_dt = datetime.fromtimestamp(file_time)
        date_key = file_dt.strftime('%Y-%m-%d')
        
        if date_key not in daily_stats:
            daily_stats[date_key] = 0
        daily_stats[date_key] += 1
    
    for date, count in sorted(daily_stats.items()):
        print(f"   {date}: {count} detections")
    
    # Thống kê nhãn
    print("\n🏷️ Thống kê nhãn:")
    class_counts = {}
    
    for label_file in label_files:
        try:
            with open(label_file, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        class_id = int(parts[0])
                        if class_id not in class_counts:
                            class_counts[class_id] = 0
                        class_counts[class_id] += 1
        except Exception as e:
            print(f"⚠️ Lỗi đọc file {label_file}: {e}")
    
    class_names = {0: "hands"}
    for class_id, count in sorted(class_counts.items()):
        class_name = class_names.get(class_id, f"class_{class_id}")
        print(f"   {class_name} (ID {class_id}): {count} objects")
    
    # Dung lượng ổ cứng
    print("\n💾 Dung lượng:")
    total_size = 0
    for image_file in image_files:
        total_size += os.path.getsize(image_file)
    
    size_mb = total_size / (1024 * 1024)
    print(f"   Tổng dung lượng ảnh: {size_mb:.2f} MB")
    print(f"   Trung bình mỗi ảnh: {size_mb/len(image_files):.2f} MB")
    
    # Gợi ý
    print("\n💡 Gợi ý:")
    if len(image_files) < 100:
        print("   ⚠️ Cần thu thập thêm dữ liệu (ít nhất 100 ảnh)")
    elif len(image_files) < 500:
        print("   ✅ Dữ liệu đủ để train thêm model")
    else:
        print("   🎉 Dữ liệu rất phong phú!")
    
    print(f"   📁 Thư mục ảnh: {os.path.abspath(images_dir)}")
    print(f"   📁 Thư mục nhãn: {os.path.abspath(labels_dir)}")

def main():
    get_data_stats()

if __name__ == "__main__":
    main() 