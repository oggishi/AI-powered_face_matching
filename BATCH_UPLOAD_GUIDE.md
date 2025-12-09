# 📤 BATCH UPLOAD - Hướng Dẫn Upload Hàng Loạt

Script tự động upload hàng loạt ảnh khuôn mặt vào database.

## 🚀 Cách sử dụng

### **Bước 1: Chuẩn bị ảnh**

Tạo folder chứa ảnh (ví dụ: `batch_images/`)
```
batch_images/
├── nguyen_van_a.jpg
├── tran_thi_b.jpg
├── john_doe.png
├── jane_smith_01.jpg
└── ...
```

### **Bước 2: Chạy server**

```cmd
python main.py
```

### **Bước 3: Chạy batch upload** (Terminal mới)

```cmd
python batch_upload.py
```

## 📋 3 Phương thức upload

### **1. Auto Upload (Khuyến nghị)**

Tự động trích xuất tên từ filename:

```
nguyen_van_a.jpg → "Nguyen Van A"
john_doe_01.jpg → "John Doe"
IMG_001_tran_thi_b.png → "Tran Thi B"
```

**Cách dùng:**
```cmd
python batch_upload.py
# Chọn: 1
# Nhập folder: batch_images
```

### **2. Upload với CSV file**

Tạo file CSV với thông tin chi tiết:

**`faces_info.csv`:**
```csv
filename,name,description
person1.jpg,Nguyen Van A,Employee - IT Dept
person2.jpg,Tran Thi B,Manager - HR Dept
john_doe.png,John Doe,Intern
```

**Cách dùng:**
```cmd
python batch_upload.py
# Chọn: 2
# Nhập folder: batch_images
# Nhập CSV: faces_info.csv
```

### **3. Manual Input**

Tự nhập tên cho từng ảnh:

```cmd
python batch_upload.py
# Chọn: 3
# Nhập folder path
# Nhập tên cho từng ảnh
```

## 💡 Ví dụ thực tế

### Ví dụ 1: Upload ảnh nhân viên

```
employees/
├── emp_001_nguyen_van_a.jpg
├── emp_002_tran_thi_b.jpg
├── emp_003_le_van_c.jpg
```

```cmd
python batch_upload.py
# Chọn 1
# Folder: employees
```

Kết quả:
- emp_001_nguyen_van_a.jpg → "Nguyen Van A"
- emp_002_tran_thi_b.jpg → "Tran Thi B"
- emp_003_le_van_c.jpg → "Le Van C"

### Ví dụ 2: Upload với thông tin đầy đủ

**employees.csv:**
```csv
filename,name,description
emp_001.jpg,Nguyen Van A,Software Engineer - Backend Team
emp_002.jpg,Tran Thi B,Product Manager
emp_003.jpg,Le Van C,UI/UX Designer
```

```cmd
python batch_upload.py
# Chọn 2
# Folder: employees
# CSV: employees.csv
```

## 🎨 Format tên file được hỗ trợ

Script tự động xử lý các format:

| Filename | → | Name |
|----------|---|------|
| `nguyen_van_a.jpg` | → | Nguyen Van A |
| `john-doe.png` | → | John Doe |
| `IMG_001_tran_thi_b.jpg` | → | Tran Thi B |
| `person_001.jpg` | → | Person |
| `john_doe_01.jpg` | → | John Doe |
| `DSC_1234_jane.jpg` | → | Jane |

## 📊 Output mẫu

```
╔══════════════════════════════════════════════════════════╗
║     BATCH UPLOAD TOOL - Upload Hàng Loạt Khuôn Mặt      ║
╚══════════════════════════════════════════════════════════╝

============================================================
🚀 Bắt đầu upload 5 ảnh từ folder: batch_images
============================================================

[1/5] Uploading: nguyen_van_a.jpg
    Name: Nguyen Van A
    Description: Nguyen Van A - Auto imported from nguyen_van_a.jpg
    ✅ Success!

[2/5] Uploading: tran_thi_b.jpg
    Name: Tran Thi B
    Description: Tran Thi B - Auto imported from tran_thi_b.jpg
    ✅ Success!

...

============================================================
📊 KẾT QUẢ UPLOAD
============================================================
✅ Thành công: 5/5
❌ Thất bại: 0/5
============================================================
```

## ⚙️ Tùy chỉnh

### Thay đổi API URL

Edit trong `batch_upload.py`:

```python
API_BASE_URL = "http://your-server:8000/api"
```

### Thay đổi folder mặc định

```python
IMAGES_FOLDER = "your_folder_name"
```

### Thêm custom logic extract name

Sửa function `extract_name_from_filename()`:

```python
def extract_name_from_filename(filename: str) -> str:
    # Your custom logic here
    # Ví dụ: extract từ database, API, etc.
    pass
```

## 🔧 Xử lý lỗi

### Lỗi: "Folder không tồn tại"

```cmd
# Tạo folder
mkdir batch_images

# Copy ảnh vào folder
copy your_images\*.jpg batch_images\
```

### Lỗi: "Không thể kết nối server"

```cmd
# Chạy server trước
python main.py

# Sau đó mới chạy batch upload (terminal mới)
python batch_upload.py
```

### Lỗi: "No face detected"

- Kiểm tra ảnh có khuôn mặt rõ ràng
- Ánh sáng tốt
- Khuôn mặt không bị che khuất

## 📝 Tips

1. **Đặt tên file có ý nghĩa:**
   ```
   ✅ nguyen_van_a.jpg
   ✅ john_doe.jpg
   ❌ IMG_1234.jpg
   ❌ DSC_5678.jpg
   ```

2. **Sử dụng CSV cho dự án lớn:**
   - Dễ quản lý
   - Có thể export từ Excel
   - Thông tin đầy đủ

3. **Test với vài ảnh trước:**
   ```cmd
   # Upload 2-3 ảnh test trước
   # Sau đó mới upload hàng loạt
   ```

4. **Backup database:**
   ```cmd
   copy database\face_matching.db database\backup.db
   ```

## 🎓 Sử dụng cho đồ án

**Demo batch upload trong presentation:**

1. Chuẩn bị 10-20 ảnh mẫu
2. Show CSV file với thông tin
3. Chạy batch upload
4. Show kết quả trong web interface

**Trong báo cáo viết:**
> "Hệ thống hỗ trợ batch upload thông qua script Python, cho phép import hàng loạt dữ liệu khuôn mặt từ folder hoặc CSV file. Script tự động trích xuất thông tin từ filename hoặc sử dụng metadata từ CSV, tối ưu hóa quy trình nhập liệu cho các tổ chức có số lượng nhân viên lớn."

---

**Happy batch uploading! 🚀**
