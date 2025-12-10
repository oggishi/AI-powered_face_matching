# 🎭 AI-Powered Face Matching System

Hệ thống nhận diện và so khớp khuôn mặt sử dụng AI
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

- **Backend**: FastAPI + Python 3.11
- **AI/ML**: ArcFace (99.82% accuracy), DeepFace, TensorFlow, RetinaFace, OpenCV
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite
- **Deployment**: Docker & Docker Compose

## 📋 Yêu Cầu Hệ Thống

### Native Python:
- Python 3.11 hoặc cao hơn
- pip
- 2GB+ RAM (4GB+ recommended)

### Docker (Recommended):
- Docker Desktop 4.0+
- Docker Compose 2.0+
- 4GB+ RAM

## 🚀 Cài Đặt

### ⚡ Cách 1: Docker (KHUYẾN NGHỊ - Nhanh & Dễ)

**Windows:**
```bash
# Sử dụng script tự động
scripts\run-docker.bat

# Hoặc thủ công:
docker-compose up -d --build
```

**Linux/Mac:**
```bash
# Cấp quyền thực thi
chmod +x scripts/run-docker.sh

# Chạy script
./scripts/run-docker.sh

# Hoặc thủ công:
docker-compose up -d --build
```

**Truy cập:** http://localhost:8000

📖 **Chi tiết:** Xem [DOCKER.md](DOCKER.md)

---

### 🐍 Cách 2: Native Python

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



## 📖 Hướng Dẫn Sử Dụng

### 1. Phát Hiện Khuôn Mặt (Detect Face)

- Vào tab "Detect Face"
- Upload ảnh
- Xem số lượng khuôn mặt được phát hiện
- ⚠️ Nếu >1 khuôn mặt: cảnh báo hiện ra

### 2. Thêm Khuôn Mặt Vào Database (Add Face)

- Vào tab "Add Face"
- Upload ảnh khuôn mặt
- Nhập thông tin (tên, mô tả)
- Click "Add to Database"

### 3. Thêm Nhiều Người Cùng Lúc (Batch Add) 🔥

- Vào tab "Batch Add"
- Upload ảnh nhóm (nhiều người)
- Nhập tên cách nhau bởi dấu phẩy: `John, Jane, Bob`
- Click "Add All to Database"
- Hệ thống tự động: detect → crop → add từng người

### 4. Tìm Kiếm Khuôn Mặt (Search Face)

- Vào tab "Search Face"
- Upload ảnh cần tìm
- Hệ thống sẽ hiển thị các khuôn mặt tương tự kèm độ chính xác (ArcFace 99.82%)

### 5. Quản Lý Database (Manage Database)

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

