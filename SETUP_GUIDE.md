# 🚀 HƯỚNG DẪN CHẠY ỨNG DỤNG

## Cách 1: Chạy trực tiếp với Python (Khuyến nghị cho Development)

### Bước 1: Cài đặt môi trường

```cmd
REM Tạo virtual environment
python -m venv face_env

REM Kích hoạt virtual environment
face_env\Scripts\activate

REM Cài đặt dependencies
pip install -r requirements.txt
```

### Bước 2: Cấu hình môi trường

```cmd
REM Copy file cấu hình
copy .env.example .env

REM Chỉnh sửa .env nếu cần (dùng notepad hoặc editor yêu thích)
notepad .env
```

### Bước 3: Chạy ứng dụng

```cmd
python main.py
```

### Bước 4: Truy cập ứng dụng

- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

---

## Cách 2: Chạy với Docker (Khuyến nghị cho Production)

### Yêu cầu
- Docker Desktop đã được cài đặt

### Bước 1: Build và chạy

```cmd
REM Build và chạy container
docker-compose up -d

REM Xem logs
docker-compose logs -f
```

### Bước 2: Truy cập ứng dụng

- **Web Interface**: http://localhost:8000

### Các lệnh Docker hữu ích

```cmd
REM Dừng container
docker-compose down

REM Rebuild container
docker-compose up -d --build

REM Xem logs
docker-compose logs -f

REM Vào trong container
docker exec -it ai-face-matching bash
```

---

## 📝 Hướng dẫn sử dụng

### 1. Phát hiện khuôn mặt (Detect Face)
1. Click tab "Detect Face"
2. Upload ảnh
3. Click "Detect Faces"
4. Xem kết quả số lượng khuôn mặt được phát hiện

### 2. Thêm khuôn mặt vào database (Add Face)
1. Click tab "Add Face"
2. Upload ảnh khuôn mặt rõ ràng
3. Nhập tên và mô tả
4. Click "Add to Database"

### 3. Tìm kiếm khuôn mặt (Search Face)
1. Click tab "Search Face"
2. Upload ảnh cần tìm
3. Chọn số lượng kết quả muốn hiển thị
4. Click "Search"
5. Xem kết quả với độ chính xác (confidence score)

### 4. Quản lý database (Manage Database)
1. Click tab "Manage Database"
2. Xem danh sách tất cả khuôn mặt đã lưu
3. Xóa khuôn mặt nếu cần

---

## 🔧 Troubleshooting

### Lỗi: "No module named 'face_recognition'"

```cmd
REM Cài đặt lại dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Lỗi: "CMake not found"

- **Windows**: Download và cài đặt Visual Studio Build Tools
- Hoặc dùng Docker để tránh vấn đề này

### Lỗi: Database locked

```cmd
REM Xóa database cũ và tạo lại
del database\face_matching.db
python main.py
```

### Port 8000 đã được sử dụng

Chỉnh sửa file `.env`:
```
PORT=8001
```

---

## 📊 API Endpoints

### 1. Phát hiện khuôn mặt
```http
POST /api/detect-face
Content-Type: multipart/form-data

file: <image-file>
```

### 2. Thêm khuôn mặt
```http
POST /api/add-face
Content-Type: multipart/form-data

file: <image-file>
name: <person-name>
description: <optional-description>
```

### 3. Tìm kiếm khuôn mặt
```http
POST /api/search-face
Content-Type: multipart/form-data

file: <image-file>
top_k: <number>
```

### 4. Lấy danh sách khuôn mặt
```http
GET /api/faces?skip=0&limit=100
```

### 5. Xóa khuôn mặt
```http
DELETE /api/faces/{face_id}
```

Chi tiết đầy đủ: http://localhost:8000/docs

---

## 💡 Tips

1. **Ảnh tốt nhất cho face recognition:**
   - Ánh sáng tốt
   - Khuôn mặt rõ ràng, nhìn thẳng
   - Không bị che khuất
   - Độ phân giải cao

2. **Tối ưu hiệu suất:**
   - Sử dụng `FACE_DETECTION_MODEL=hog` cho CPU
   - Sử dụng `FACE_DETECTION_MODEL=cnn` cho GPU (chính xác hơn)

3. **Backup database:**
   ```cmd
   copy database\face_matching.db database\backup.db
   ```

---

## 🎓 Sử dụng cho Luận văn/Đồ án

### Các điểm nổi bật để trình bày:

1. **Công nghệ sử dụng:**
   - Deep Learning với dlib
   - Face Recognition library (accuracy ~99.38%)
   - RESTful API với FastAPI
   - Responsive UI với Bootstrap

2. **Kiến trúc hệ thống:**
   - Backend: FastAPI (Python)
   - Face Detection: HOG/CNN algorithms
   - Face Encoding: 128-dimensional embeddings
   - Database: SQLite
   - Frontend: HTML/CSS/JavaScript

3. **Tính năng chính:**
   - Real-time face detection
   - Face matching với confidence score
   - Database management
   - RESTful API
   - Docker deployment

### Cấu trúc demo:
1. Giới thiệu hệ thống (2 phút)
2. Demo phát hiện khuôn mặt (1 phút)
3. Demo thêm vào database (1 phút)
4. Demo tìm kiếm & matching (2 phút)
5. Giải thích thuật toán (2 phút)
6. Q&A

---

## 📞 Support

Nếu gặp vấn đề, hãy:
1. Check logs: `docker-compose logs -f`
2. Kiểm tra file README.md
3. Xem API docs: http://localhost:8000/docs

---

**Good luck with your project! 🎉**
