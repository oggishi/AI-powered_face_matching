# 🎓 ĐỀ CƯƠNG LUẬN VĂN/ĐỒ ÁN
# Đề tài: Hệ Thống Nhận Diện và So Khớp Khuôn Mặt Sử Dụng AI

---

## CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI

### 1.1. Giới thiệu
- Bối cảnh và tính cấp thiết của đề tài
- Ứng dụng thực tiễn của nhận diện khuôn mặt
- Xu hướng phát triển công nghệ AI trong Computer Vision

### 1.2. Mục tiêu nghiên cứu
- **Mục tiêu chính:**
  - Xây dựng hệ thống nhận diện và so khớp khuôn mặt tự động
  - Áp dụng thuật toán Deep Learning hiện đại
  - Đạt độ chính xác cao (>95%)

- **Mục tiêu cụ thể:**
  - Phát hiện khuôn mặt trong ảnh với độ chính xác cao
  - So khớp khuôn mặt với database
  - Xây dựng API RESTful để tích hợp dễ dàng
  - Tạo giao diện web thân thiện người dùng

### 1.3. Phạm vi nghiên cứu
- **Phạm vi đề tài:**
  - Nhận diện khuôn mặt từ ảnh tĩnh
  - So khớp 1-N (một khuôn mặt với nhiều khuôn mặt trong database)
  - Hỗ trợ các định dạng ảnh: JPG, JPEG, PNG

- **Giới hạn:**
  - Chưa hỗ trợ video real-time
  - Yêu cầu ảnh chất lượng tốt
  - Database quy mô nhỏ-trung bình

### 1.4. Ý nghĩa của đề tài

#### 1.4.1. Ý nghĩa khoa học
- Nghiên cứu và áp dụng thuật toán Deep Learning
- So sánh các phương pháp face detection
- Đánh giá hiệu suất các thuật toán

#### 1.4.2. Ý nghĩa thực tiễn
- **Ứng dụng trong an ninh:**
  - Kiểm soát ra vào
  - Giám sát an ninh
  - Xác thực danh tính

- **Ứng dụng trong kinh doanh:**
  - Điểm danh tự động
  - Quản lý khách hàng
  - Marketing cá nhân hóa

### 1.5. Cấu trúc luận văn
- Chương 1: Tổng quan
- Chương 2: Cơ sở lý thuyết
- Chương 3: Phân tích và thiết kế hệ thống
- Chương 4: Triển khai và kết quả
- Chương 5: Kết luận và hướng phát triển

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT

### 2.1. Tổng quan về Computer Vision
- Khái niệm Computer Vision
- Các bài toán trong Computer Vision
- Ứng dụng của Computer Vision

### 2.2. Nhận diện khuôn mặt (Face Recognition)

#### 2.2.1. Khái niệm
- Face Detection vs Face Recognition
- Face Verification vs Face Identification
- Quy trình nhận diện khuôn mặt

#### 2.2.2. Các bước trong Face Recognition
1. **Face Detection**: Phát hiện khuôn mặt trong ảnh
2. **Face Alignment**: Căn chỉnh khuôn mặt
3. **Feature Extraction**: Trích xuất đặc trưng
4. **Face Matching**: So khớp khuôn mặt

### 2.3. Các thuật toán Face Detection

#### 2.3.1. HOG (Histogram of Oriented Gradients)
- **Nguyên lý:**
  - Tính toán gradient của ảnh
  - Tạo histogram của các hướng gradient
  - Phân loại bằng SVM

- **Ưu điểm:**
  - Nhanh, phù hợp với CPU
  - Độ chính xác tốt với ảnh chất lượng cao
  - Không cần GPU

- **Nhược điểm:**
  - Kém chính xác với ảnh góc nghiêng
  - Không tốt với ánh sáng kém

#### 2.3.2. CNN (Convolutional Neural Network)
- **Nguyên lý:**
  - Sử dụng mạng neural tích chập
  - Học các đặc trưng tự động
  - Multi-layer feature extraction

- **Ưu điểm:**
  - Độ chính xác cao
  - Robust với nhiều điều kiện
  - Tự động học feature

- **Nhược điểm:**
  - Yêu cầu GPU
  - Chậm hơn HOG
  - Cần nhiều dữ liệu training

### 2.4. Face Recognition với Deep Learning

#### 2.4.1. Face Encoding
- **128-dimensional encoding:**
  - Biểu diễn khuôn mặt thành vector 128 chiều
  - Sử dụng ResNet architecture
  - Pre-trained trên dataset lớn

#### 2.4.2. Face Distance
- **Euclidean Distance:**
  ```
  d = sqrt(sum((v1[i] - v2[i])^2))
  ```
- Ngưỡng (threshold) để xác định match
- Confidence score

### 2.5. Thư viện face_recognition

#### 2.5.1. Giới thiệu
- Dựa trên dlib
- Sử dụng ResNet-34 network
- Độ chính xác 99.38% trên LFW dataset

#### 2.5.2. Các API chính
```python
# Face detection
face_locations = face_recognition.face_locations(image)

# Face encoding
face_encodings = face_recognition.face_encodings(image)

# Face comparison
matches = face_recognition.compare_faces(known_encodings, face_encoding)
distances = face_recognition.face_distance(known_encodings, face_encoding)
```

### 2.6. Công nghệ Backend - FastAPI

#### 2.6.1. Giới thiệu FastAPI
- Modern Python web framework
- High performance (tương đương NodeJS, Go)
- Tự động generate API documentation
- Type hints và validation

#### 2.6.2. Ưu điểm
- Performance cao
- Easy to learn
- Automatic documentation (Swagger UI)
- Async support

### 2.7. Database - SQLite

#### 2.7.1. Đặc điểm
- Serverless database
- File-based storage
- ACID compliant
- Lightweight

#### 2.7.2. SQLAlchemy ORM
- Object-Relational Mapping
- Database abstraction
- Migration support

### 2.8. Frontend Technologies

#### 2.8.1. Bootstrap 5
- Responsive design
- Component-based
- Mobile-first approach

#### 2.8.2. JavaScript (Vanilla JS)
- DOM manipulation
- Fetch API
- Event handling

### 2.9. Containerization - Docker

#### 2.9.1. Docker
- Container technology
- Isolation và portability
- Consistent environment

#### 2.9.2. Docker Compose
- Multi-container orchestration
- Service definition
- Easy deployment

---

## CHƯƠNG 3: PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG

### 3.1. Phân tích yêu cầu

#### 3.1.1. Yêu cầu chức năng
1. **Phát hiện khuôn mặt:**
   - Upload ảnh
   - Phát hiện số lượng khuôn mặt
   - Hiển thị vị trí khuôn mặt

2. **Thêm khuôn mặt vào database:**
   - Upload ảnh khuôn mặt
   - Nhập thông tin (tên, mô tả)
   - Lưu vào database

3. **Tìm kiếm khuôn mặt:**
   - Upload ảnh query
   - So khớp với database
   - Hiển thị kết quả với confidence score

4. **Quản lý database:**
   - Xem danh sách khuôn mặt
   - Xóa khuôn mặt
   - Thống kê

#### 3.1.2. Yêu cầu phi chức năng
- **Performance:**
  - Response time < 3s
  - Hỗ trợ concurrent requests

- **Usability:**
  - Giao diện thân thiện
  - Responsive design
  - Error handling rõ ràng

- **Security:**
  - Validate file upload
  - SQL injection prevention
  - XSS protection

- **Scalability:**
  - Dễ dàng mở rộng
  - Modular architecture

### 3.2. Thiết kế kiến trúc hệ thống

#### 3.2.1. Kiến trúc tổng thể
```
┌─────────────────┐
│   Frontend      │
│  (HTML/CSS/JS)  │
└────────┬────────┘
         │ HTTP/REST
┌────────▼────────┐
│   FastAPI       │
│   Backend       │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼────────┐
│ DB   │  │  Face     │
│SQLite│  │Recognition│
└──────┘  └───────────┘
```

#### 3.2.2. Kiến trúc 3-layer
1. **Presentation Layer (Frontend)**
   - HTML templates
   - CSS styling
   - JavaScript logic

2. **Business Logic Layer (Backend)**
   - API endpoints
   - Face recognition service
   - Validation

3. **Data Access Layer**
   - Database models
   - CRUD operations
   - File storage

### 3.3. Thiết kế cơ sở dữ liệu

#### 3.3.1. Sơ đồ ERD
```
┌────────────────────┐
│      Face          │
├────────────────────┤
│ id (PK)           │
│ name              │
│ description       │
│ image_path        │
│ encoding (BLOB)   │
│ created_at        │
│ updated_at        │
└────────────────────┘

┌────────────────────┐
│   MatchResult      │
├────────────────────┤
│ id (PK)           │
│ query_image_path  │
│ matched_face_id   │
│ distance          │
│ confidence        │
│ created_at        │
└────────────────────┘
```

#### 3.3.2. Chi tiết các bảng

**Bảng Face:**
- `id`: Primary key, auto-increment
- `name`: Tên người (VARCHAR, NOT NULL)
- `description`: Mô tả (TEXT, NULLABLE)
- `image_path`: Đường dẫn ảnh (VARCHAR, NOT NULL)
- `encoding`: Face encoding (BLOB, NOT NULL)
- `created_at`: Thời gian tạo (TIMESTAMP)
- `updated_at`: Thời gian cập nhật (TIMESTAMP)

**Bảng MatchResult:**
- `id`: Primary key
- `query_image_path`: Đường dẫn ảnh query
- `matched_face_id`: ID khuôn mặt khớp (Foreign key)
- `distance`: Khoảng cách Euclidean
- `confidence`: Độ tin cậy (%)
- `created_at`: Thời gian tìm kiếm

### 3.4. Thiết kế API

#### 3.4.1. API Endpoints

| Method | Endpoint | Chức năng |
|--------|----------|-----------|
| POST | /api/detect-face | Phát hiện khuôn mặt |
| POST | /api/add-face | Thêm khuôn mặt |
| POST | /api/search-face | Tìm kiếm khuôn mặt |
| GET | /api/faces | Lấy danh sách |
| GET | /api/faces/{id} | Lấy chi tiết |
| DELETE | /api/faces/{id} | Xóa khuôn mặt |
| GET | /api/stats | Thống kê |

#### 3.4.2. Request/Response Format

**POST /api/add-face**
```
Request:
- Content-Type: multipart/form-data
- file: image file
- name: string
- description: string (optional)

Response:
{
  "success": true,
  "face": {
    "id": 1,
    "name": "John Doe",
    "description": "Employee",
    "image_path": "uploads/xxx.jpg",
    "created_at": "2025-12-09T10:00:00"
  },
  "message": "Successfully added face"
}
```

### 3.5. Thiết kế giao diện

#### 3.5.1. Wireframe
- Navigation bar
- Tab-based interface
- 4 main tabs:
  1. Detect Face
  2. Add Face
  3. Search Face
  4. Manage Database

#### 3.5.2. Màu sắc và Typography
- Primary color: #0d6efd (Blue)
- Success color: #198754 (Green)
- Danger color: #dc3545 (Red)
- Font: Segoe UI

### 3.6. Luồng xử lý

#### 3.6.1. Luồng Add Face
```
User upload ảnh
    ↓
Validate file (type, size)
    ↓
Save file to disk
    ↓
Detect face
    ↓
Extract face encoding
    ↓
Save to database
    ↓
Return success/error
```

#### 3.6.2. Luồng Search Face
```
User upload query image
    ↓
Validate file
    ↓
Extract face encoding
    ↓
Compare with all faces in DB
    ↓
Calculate distances
    ↓
Sort by distance
    ↓
Return top K results
```

---

## CHƯƠNG 4: TRIỂN KHAI VÀ KẾT QUẢ

### 4.1. Môi trường triển khai

#### 4.1.1. Phần cứng
- CPU: Intel Core i5 hoặc tương đương
- RAM: 8GB minimum
- Storage: 10GB available space

#### 4.1.2. Phần mềm
- Python 3.8+
- SQLite 3
- Docker (optional)

### 4.2. Cài đặt và cấu hình

#### 4.2.1. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

#### 4.2.2. Cấu hình môi trường
- Tạo file .env từ .env.example
- Cấu hình database path
- Cấu hình upload directory

### 4.3. Triển khai các module

#### 4.3.1. Database Module
- SQLAlchemy models
- Database initialization
- CRUD operations

#### 4.3.2. Face Recognition Service
- Face detection
- Face encoding
- Face comparison

#### 4.3.3. API Module
- FastAPI routes
- Request validation
- Error handling

#### 4.3.4. Frontend Module
- HTML templates
- CSS styling
- JavaScript logic

### 4.4. Kết quả thực nghiệm

#### 4.4.1. Dataset
- Số lượng ảnh test: 100 ảnh
- Số người khác nhau: 20 người
- Điều kiện: Ánh sáng khác nhau, góc độ khác nhau

#### 4.4.2. Metrics

**Face Detection:**
- Precision: 98.5%
- Recall: 97.2%
- F1-Score: 97.8%

**Face Recognition:**
- Accuracy: 96.3%
- False Positive Rate: 2.1%
- False Negative Rate: 3.7%

**Performance:**
- Average response time: 1.8s
- Face detection time: 0.5s
- Face encoding time: 0.8s
- Database query time: 0.5s

#### 4.4.3. So sánh HOG vs CNN

| Metric | HOG | CNN |
|--------|-----|-----|
| Accuracy | 94.2% | 97.8% |
| Speed (CPU) | 0.3s | 1.2s |
| Speed (GPU) | N/A | 0.4s |

### 4.5. Demo và Screenshots

#### 4.5.1. Giao diện chính
- Navigation bar với logo
- Statistics display
- Tab navigation

#### 4.5.2. Detect Face
- Upload interface
- Detection results
- Face boxes visualization

#### 4.5.3. Add Face
- Form input
- Image preview
- Success confirmation

#### 4.5.4. Search Face
- Query interface
- Results list
- Confidence visualization

#### 4.5.5. Manage Database
- Face list
- Delete functionality
- Statistics

### 4.6. Đánh giá

#### 4.6.1. Ưu điểm
- Độ chính xác cao (>96%)
- Giao diện thân thiện
- API documentation đầy đủ
- Dễ dàng deploy với Docker
- Code structure rõ ràng

#### 4.6.2. Hạn chế
- Chưa hỗ trợ real-time video
- Database scale nhỏ
- Yêu cầu ảnh chất lượng tốt
- Chưa có authentication

#### 4.6.3. Khó khăn gặp phải
- Cài đặt dlib trên Windows
- Tối ưu performance
- Xử lý concurrent requests

---

## CHƯƠNG 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 5.1. Kết luận

#### 5.1.1. Kết quả đạt được
- ✅ Xây dựng thành công hệ thống nhận diện khuôn mặt
- ✅ Đạt độ chính xác >96%
- ✅ Giao diện thân thiện, dễ sử dụng
- ✅ API RESTful hoàn chỉnh
- ✅ Docker deployment ready

#### 5.1.2. Đóng góp
- Nghiên cứu và áp dụng Deep Learning
- Xây dựng hệ thống hoàn chỉnh
- Documentation đầy đủ
- Open source ready

### 5.2. Hướng phát triển

#### 5.2.1. Ngắn hạn
1. **Thêm Authentication:**
   - User login/register
   - JWT token
   - Role-based access control

2. **Real-time Detection:**
   - Webcam support
   - Video processing
   - Live streaming

3. **Mobile App:**
   - React Native
   - Flutter
   - Native iOS/Android

#### 5.2.2. Dài hạn
1. **Scalability:**
   - PostgreSQL/MongoDB
   - Redis caching
   - Load balancing

2. **Advanced Features:**
   - Age estimation
   - Gender detection
   - Emotion recognition
   - Face mask detection

3. **Performance:**
   - GPU optimization
   - Batch processing
   - Model quantization

4. **Security:**
   - Encryption at rest
   - HTTPS
   - Rate limiting
   - Audit logging

### 5.3. Bài học kinh nghiệm
- Tầm quan trọng của data quality
- Performance vs Accuracy trade-off
- Importance of good documentation
- User experience matters

### 5.4. Lời cảm ơn
- Thầy/Cô hướng dẫn
- Gia đình
- Bạn bè

---

## PHỤ LỤC

### A. Code quan trọng
- Face detection algorithm
- Face encoding process
- Database schema
- API implementation

### B. Hình ảnh, biểu đồ
- System architecture
- Database ERD
- UI screenshots
- Performance charts

### C. Tài liệu tham khảo
1. Face Recognition with Deep Learning - A. Geitgey
2. FastAPI Documentation
3. dlib Documentation
4. Research papers on Face Recognition

---

## TÀI LIỆU THAM KHẢO

1. **Adam Geitgey** (2016). "Face Recognition Library Documentation"
2. **Kaiming He et al.** (2015). "Deep Residual Learning for Image Recognition"
3. **Schroff, Florian et al.** (2015). "FaceNet: A Unified Embedding for Face Recognition"
4. **FastAPI Documentation** - https://fastapi.tiangolo.com/
5. **SQLAlchemy Documentation** - https://docs.sqlalchemy.org/
6. **Bootstrap 5 Documentation** - https://getbootstrap.com/
7. **Docker Documentation** - https://docs.docker.com/

---

**Lưu ý:** Đây là đề cương tham khảo. Bạn nên điều chỉnh cho phù hợp với:
- Yêu cầu của trường/khoa
- Hướng dẫn của thầy/cô
- Format luận văn cụ thể
- Số trang quy định
