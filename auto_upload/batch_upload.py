"""
Batch Upload Script - Upload multiple face images to database
Tự động upload hàng loạt ảnh khuôn mặt từ folder
"""

import os
import sys
import requests
from pathlib import Path
import time

# Configuration
API_BASE_URL = "http://localhost:8000/api"
IMAGES_FOLDER = "batch_images"  # Folder chứa ảnh cần upload

def extract_name_from_filename(filename: str) -> str:
    """
    Trích xuất tên từ tên file
    
    Ví dụ:
    - "nguyen_van_a.jpg" -> "Nguyen Van A"
    - "john_doe_01.jpg" -> "John Doe"
    - "IMG_001_tran_thi_b.png" -> "Tran Thi B"
    """
    # Remove extension
    name = Path(filename).stem
    
    # Remove số thứ tự ở cuối (01, 02, _1, _2, etc.)
    import re
    name = re.sub(r'[_\-]\d+$', '', name)
    name = re.sub(r'_\d+$', '', name)
    
    # Remove prefix như IMG_, DSC_, etc.
    name = re.sub(r'^(IMG|DSC|PIC|PHOTO|IMAGE)[_\-]?\d*[_\-]?', '', name, flags=re.IGNORECASE)
    
    # Replace underscores and dashes with spaces
    name = name.replace('_', ' ').replace('-', ' ')
    
    # Capitalize each word
    name = ' '.join(word.capitalize() for word in name.split())
    
    return name if name else "Unknown Person"


def generate_description(filename: str, index: int, total: int) -> str:
    """
    Tự động tạo mô tả cho ảnh
    """
    descriptions = [
        f"Person #{index + 1} of {total}",
        f"Face image imported from batch upload",
        f"Auto-imported face data",
        f"Batch upload - Image {index + 1}/{total}",
    ]
    
    # Thêm thông tin từ filename nếu có
    name = extract_name_from_filename(filename)
    if name != "Unknown Person":
        return f"{name} - Auto imported from {filename}"
    
    return descriptions[index % len(descriptions)]


def upload_single_image(image_path: str, name: str, description: str) -> dict:
    """
    Upload một ảnh lên server
    """
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            data = {
                'name': name,
                'description': description
            }
            
            response = requests.post(
                f"{API_BASE_URL}/add-face",
                files=files,
                data=data,
                timeout=30
            )
            
            return {
                'success': response.status_code == 200,
                'response': response.json() if response.status_code == 200 else None,
                'error': response.text if response.status_code != 200 else None
            }
    except Exception as e:
        return {
            'success': False,
            'response': None,
            'error': str(e)
        }


def batch_upload(folder_path: str, name_mapping: dict = None):
    """
    Upload hàng loạt ảnh từ folder
    
    Args:
        folder_path: Đường dẫn folder chứa ảnh
        name_mapping: Dict mapping filename -> name (optional)
    """
    # Kiểm tra folder tồn tại
    if not os.path.exists(folder_path):
        print(f"❌ Folder không tồn tại: {folder_path}")
        return
    
    # Lấy danh sách file ảnh
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = [
        f for f in os.listdir(folder_path)
        if Path(f).suffix.lower() in image_extensions
    ]
    
    if not image_files:
        print(f"❌ Không tìm thấy file ảnh trong folder: {folder_path}")
        return
    
    total = len(image_files)
    print(f"\n{'='*60}")
    print(f"🚀 Bắt đầu upload {total} ảnh từ folder: {folder_path}")
    print(f"{'='*60}\n")
    
    success_count = 0
    failed_count = 0
    failed_files = []
    
    for index, filename in enumerate(image_files):
        image_path = os.path.join(folder_path, filename)
        
        # Lấy tên từ mapping hoặc tự động extract
        if name_mapping and filename in name_mapping:
            name = name_mapping[filename]
        else:
            name = extract_name_from_filename(filename)
        
        # Tạo description
        description = generate_description(filename, index, total)
        
        print(f"[{index + 1}/{total}] Uploading: {filename}")
        print(f"    Name: {name}")
        print(f"    Description: {description}")
        
        # Upload
        result = upload_single_image(image_path, name, description)
        
        if result['success']:
            print(f"    ✅ Success!\n")
            success_count += 1
        else:
            print(f"    ❌ Failed: {result['error']}\n")
            failed_count += 1
            failed_files.append({
                'filename': filename,
                'error': result['error']
            })
        
        # Delay nhẹ để không quá tải server
        time.sleep(0.5)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 KẾT QUẢ UPLOAD")
    print(f"{'='*60}")
    print(f"✅ Thành công: {success_count}/{total}")
    print(f"❌ Thất bại: {failed_count}/{total}")
    
    if failed_files:
        print(f"\n📋 Danh sách file thất bại:")
        for item in failed_files:
            print(f"  - {item['filename']}: {item['error'][:100]}")
    
    print(f"\n{'='*60}\n")


def batch_upload_with_csv(folder_path: str, csv_file: str):
    """
    Upload hàng loạt với thông tin từ CSV file
    
    CSV format:
    filename,name,description
    person1.jpg,Nguyen Van A,Employee
    person2.jpg,Tran Thi B,Manager
    """
    import csv
    
    name_mapping = {}
    desc_mapping = {}
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                filename = row['filename']
                name_mapping[filename] = row['name']
                if 'description' in row:
                    desc_mapping[filename] = row['description']
    except Exception as e:
        print(f"❌ Lỗi đọc CSV file: {e}")
        return
    
    # Modify batch_upload to use desc_mapping
    if not os.path.exists(folder_path):
        print(f"❌ Folder không tồn tại: {folder_path}")
        return
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = [
        f for f in os.listdir(folder_path)
        if Path(f).suffix.lower() in image_extensions
    ]
    
    total = len(image_files)
    print(f"\n🚀 Uploading {total} images with CSV data...\n")
    
    success_count = 0
    for index, filename in enumerate(image_files):
        image_path = os.path.join(folder_path, filename)
        
        name = name_mapping.get(filename, extract_name_from_filename(filename))
        description = desc_mapping.get(filename, generate_description(filename, index, total))
        
        print(f"[{index + 1}/{total}] {filename}: {name}")
        
        result = upload_single_image(image_path, name, description)
        
        if result['success']:
            print(f"    ✅ Success!\n")
            success_count += 1
        else:
            print(f"    ❌ Failed: {result['error']}\n")
        
        time.sleep(0.5)
    
    print(f"\n✅ Uploaded {success_count}/{total} images successfully!\n")


def main():
    """Main function với menu lựa chọn"""
    print("""
╔══════════════════════════════════════════════════════════╗
║     BATCH UPLOAD TOOL - Upload Hàng Loạt Khuôn Mặt      ║
╚══════════════════════════════════════════════════════════╝

Chọn phương thức upload:

1. Auto Upload (tự động extract tên từ filename)
2. Upload với CSV file (có sẵn thông tin name, description)
3. Manual input folder path

0. Exit
    """)
    
    choice = input("Nhập lựa chọn (0-3): ").strip()
    
    if choice == '0':
        print("👋 Bye!")
        return
    
    elif choice == '1':
        # Auto upload
        folder = input(f"\nNhập đường dẫn folder chứa ảnh (mặc định: {IMAGES_FOLDER}): ").strip()
        folder = folder if folder else IMAGES_FOLDER
        
        batch_upload(folder)
    
    elif choice == '2':
        # Upload with CSV
        folder = input(f"\nNhập đường dẫn folder chứa ảnh (mặc định: {IMAGES_FOLDER}): ").strip()
        folder = folder if folder else IMAGES_FOLDER
        
        csv_file = input("Nhập đường dẫn CSV file: ").strip()
        
        if csv_file and os.path.exists(csv_file):
            batch_upload_with_csv(folder, csv_file)
        else:
            print("❌ CSV file không tồn tại!")
    
    elif choice == '3':
        # Manual input
        folder = input("\nNhập đường dẫn folder: ").strip()
        
        if folder and os.path.exists(folder):
            # Ask if want to use custom naming
            use_mapping = input("\nBạn có muốn tự đặt tên cho từng ảnh? (y/n): ").strip().lower()
            
            if use_mapping == 'y':
                name_mapping = {}
                image_files = [
                    f for f in os.listdir(folder)
                    if Path(f).suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']
                ]
                
                print(f"\nCó {len(image_files)} ảnh. Nhập tên cho từng ảnh:")
                for filename in image_files:
                    default_name = extract_name_from_filename(filename)
                    name = input(f"  {filename} [{default_name}]: ").strip()
                    name_mapping[filename] = name if name else default_name
                
                batch_upload(folder, name_mapping)
            else:
                batch_upload(folder)
        else:
            print("❌ Folder không tồn tại!")
    
    else:
        print("❌ Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    # Kiểm tra server đang chạy
    try:
        response = requests.get(f"{API_BASE_URL}/stats", timeout=5)
        if response.status_code != 200:
            print("⚠️  Server có thể chưa chạy. Hãy chạy: python main.py")
            sys.exit(1)
    except:
        print("❌ Không thể kết nối server!")
        print("   Hãy chạy server trước: python main.py")
        sys.exit(1)
    
    main()
