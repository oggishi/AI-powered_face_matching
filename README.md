# 🎭 AI-Powered Face Matching System

Hệ thống nhận diện và so khớp khuôn mặt sử dụng AI, được xây dựng với FastAPI và face_recognition library.
## 📊 Cấu Trúc Dự Án

```
AI-powered_face_matching/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── face.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── face_recognition_service.py
│   └── __init__.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── images/
├── templates/
│   └── index.html
├── database/
├── uploads/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── main.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## ✨ Tính Năng

- 📸 **Upload và phát hiện khuôn mặt**: Upload ảnh và tự động phát hiện khuôn mặt
- 🔍 **Tìm kiếm khuôn mặt tương tự**: So khớp khuôn mặt với database
- 💾 **Quản lý database**: Thêm, xóa, cập nhật thông tin khuôn mặt
- 📊 **Báo cáo chi tiết**: Hiển thị độ chính xác và thông tin matching
- 🎨 **Giao diện web đẹp mắt**: Bootstrap responsive design
- 🐳 **Docker ready**: Dễ dàng deploy

## 🛠️ Công Nghệ

- **Backend**: FastAPI + Python 3.8+
- **AI/ML**: face_recognition, dlib, OpenCV
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite
- **Deployment**: Docker & Docker Compose

## 📋 Yêu Cầu Hệ Thống

- Python 3.8 hoặc cao hơn
- pip
- (Tùy chọn) Docker & Docker Compose

## 🚀 Cài Đặt

### Cách 1: Chạy trực tiếp với Python

1. **Clone repository**
```bash
git clone <your-repo-url>
cd AI-powered_face_matching
```

2. **Tạo virtual environment**
```bash
python -m venv face_env
# Windows
face_env\Scripts\activate
# Linux/Mac
source face_env/bin/activate
```

3. **Cài đặt dependencies**
```bash
pip install -r requirements.txt
```

4. **Cấu hình environment**
```bash
copy .env.example .env
# Chỉnh sửa .env theo nhu cầu
```

5. **Chạy ứng dụng**
```bash
python main.py
```

6. **Truy cập ứng dụng**
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative API Docs: http://localhost:8000/redoc

### Cách 2: Chạy với Docker

1. **Build và chạy**
```bash
docker-compose up -d
```

2. **Truy cập ứng dụng**
- Web Interface: http://localhost:8000

## 📖 Hướng Dẫn Sử Dụng

### 1. Thêm Khuôn Mặt Vào Database

- Vào tab "Add Face"
- Upload ảnh khuôn mặt
- Nhập thông tin (tên, mô tả)
- Click "Add to Database"

### 2. Tìm Kiếm Khuôn Mặt

- Vào tab "Search Face"
- Upload ảnh cần tìm
- Hệ thống sẽ hiển thị các khuôn mặt tương tự kèm độ chính xác

### 3. Quản Lý Database

- Vào tab "Manage Database"
- Xem danh sách khuôn mặt đã lưu
- Xóa hoặc cập nhật thông tin

## 🔧 API Endpoints

### Upload và phát hiện khuôn mặt
```
POST /api/detect-face
```

### Thêm khuôn mặt vào database
```
POST /api/add-face
```

### Tìm kiếm khuôn mặt
```
POST /api/search-face
```

### Lấy danh sách khuôn mặt
```
GET /api/faces
```

### Xóa khuôn mặt
```
DELETE /api/faces/{face_id}
```

Chi tiết API: http://localhost:8000/docs

