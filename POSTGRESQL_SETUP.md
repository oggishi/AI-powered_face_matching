# PostgreSQL Setup Guide - Supabase (Free)

Hướng dẫn chuyển từ SQLite sang PostgreSQL với Supabase (miễn phí, không cần thẻ tín dụng).

## Bước 1: Tạo tài khoản Supabase

1. Truy cập: https://supabase.com
2. Click **"Start your project"** → Sign up với GitHub/Google
3. Xác nhận email

## Bước 2: Tạo Project mới

1. Click **"New Project"**
2. Điền thông tin:
   - **Name**: `face-matching-system` (hoặc tên bạn thích)
   - **Database Password**: Tạo password mạnh (LƯU LẠI PASSWORD NÀY!)
   - **Region**: Chọn `Southeast Asia (Singapore)` (gần Việt Nam nhất)
   - **Pricing Plan**: **Free** (0$/month)
3. Click **"Create new project"**
4. Đợi 2-3 phút để Supabase khởi tạo database

## Bước 3: Lấy Connection String

1. Trong project, click **Settings** (icon bánh răng) ở sidebar trái
2. Click **Database** trong menu Settings
3. Scroll xuống phần **Connection string**
4. Chọn tab **URI** (không phải Pooler)
5. Copy chuỗi có dạng:
   ```
   postgresql://postgres.[PROJECT_REF]:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
   ```
6. **QUAN TRỌNG**: Thay `[YOUR-PASSWORD]` bằng password bạn đã tạo ở bước 2

## Bước 4: Cấu hình .env

1. Tạo file `.env` (nếu chưa có):
   ```bash
   copy .env.example .env
   ```

2. Mở file `.env` và sửa dòng `DATABASE_URL`:
   ```env
   DATABASE_URL=postgresql://postgres.xxxxx:YOUR_PASSWORD@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
   ```

**Ví dụ thực tế:**
```env
DATABASE_URL=postgresql://postgres.abcdefghijk:MyStr0ngP@ss@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
```

## Bước 5: Test kết nối

1. **Khởi động server:**
   ```bash
   python main.py
   ```

2. **Kiểm tra log:**
   ```
   ✅ Database initialized
   ✅ AI-Powered Face Matching System v1.0.0 started
   ```

3. **Mở trình duyệt:** http://localhost:8000

4. **Upload 1 khuôn mặt** để test

## Bước 6: Kiểm tra dữ liệu trên Supabase

1. Quay lại Supabase Dashboard
2. Click **Table Editor** ở sidebar
3. Bạn sẽ thấy 2 tables:
   - **faces** - Chứa thông tin khuôn mặt
   - **match_results** - Lịch sử tìm kiếm
4. Click vào table để xem dữ liệu

## Lợi ích của PostgreSQL

✅ **Shared Database**: Máy khác truy cập cùng URL → cùng dữ liệu
✅ **Cloud Backup**: Dữ liệu lưu trên cloud, không mất khi format máy
✅ **Scalable**: Hỗ trợ nhiều người dùng cùng lúc
✅ **Production Ready**: Phù hợp deploy thật

## So sánh SQLite vs PostgreSQL

| Feature | SQLite (Local) | PostgreSQL (Cloud) |
|---------|---------------|-------------------|
| Lưu trữ | File local | Cloud server |
| Chia sẻ | ❌ Không | ✅ Có |
| Multi-user | ❌ Khó | ✅ Tốt |
| Backup | Thủ công | Tự động |
| Tốc độ | Nhanh (local) | Phụ thuộc mạng |
| Giá | Miễn phí | Miễn phí (Supabase Free) |

## Quay lại SQLite

Nếu muốn quay lại SQLite:

1. Mở `.env`
2. Đổi lại:
   ```env
   DATABASE_URL=sqlite:///./database/face_matching.db
   ```
3. Restart server

## Troubleshooting

### Lỗi: "connection failed"
- Kiểm tra password có đúng không
- Kiểm tra internet connection
- Thử copy lại connection string từ Supabase

### Lỗi: "SSL required"
Nếu gặp lỗi SSL, thêm `?sslmode=require` vào cuối URL:
```env
DATABASE_URL=postgresql://...postgres?sslmode=require
```

### Lỗi: "password authentication failed"
- Password sai → Lấy lại password từ Supabase Settings
- Hoặc reset database password trong Supabase Settings

## Supabase Free Tier Limits

- **Database Size**: 500 MB
- **Bandwidth**: 5 GB/month
- **Active connections**: 60 simultaneous
- **Backups**: 7 days

→ **Đủ cho project học tập và demo!** 🎓

## Giải pháp khác (Nếu không dùng Supabase)

### 1. Railway.app
- Link: https://railway.app
- Free tier: $5 credit/month
- Setup: Tương tự Supabase

### 2. Neon.tech
- Link: https://neon.tech
- Free tier: 10 GB storage
- Tốc độ nhanh hơn Supabase

### 3. ElephantSQL
- Link: https://www.elephantsql.com
- Free tier: 20 MB (nhỏ)
- Phù hợp test nhỏ

## Kết luận

✅ **Code đã sẵn sàng cho PostgreSQL**
✅ **Chỉ cần tạo Supabase account và copy connection string**
✅ **Không cần thay đổi code gì thêm**

**Thời gian setup**: ~10 phút
**Chi phí**: Miễn phí 100%

Good luck! 🚀
