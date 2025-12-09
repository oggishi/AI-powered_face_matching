# ⚠️ LỖI: MediaPipe không hỗ trợ Python 3.13

## Vấn đề
Bạn đang dùng **Python 3.13**, nhưng MediaPipe chỉ hỗ trợ đến **Python 3.11**

## ✅ Giải pháp: Dùng Python 3.11

### **Option 1: Cài Python 3.11 (Khuyến nghị)**

1. **Download Python 3.11:**
   - Truy cập: https://www.python.org/downloads/
   - Download: **Python 3.11.x** (bản mới nhất của 3.11)

2. **Cài đặt:**
   - ✅ Check: "Add Python to PATH"
   - Install

3. **Tạo lại project:**
```cmd
REM Xóa venv cũ
rmdir /s /q face_env

REM Tạo venv với Python 3.11
py -3.11 -m venv face_env

REM Kích hoạt
face_env\Scripts\activate

REM Cài đặt packages
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

REM Chạy
python main.py
```

### **Option 2: Dùng Anaconda/Miniconda (Nếu đã cài)**

```cmd
REM Tạo environment với Python 3.11
conda create -n face_env python=3.11 -y

REM Kích hoạt
conda activate face_env

REM Di chuyển vào thư mục project
cd "d:\University\Computer Vision\AI-powered_face_matching"

REM Cài đặt packages
pip install -r requirements.txt

REM Chạy
python main.py
```

### **Option 3: Dùng face-recognition thay MediaPipe (Khó hơn)**

Nếu vẫn muốn dùng Python 3.13:

```cmd
REM Cài Visual Studio Build Tools (3GB+)
REM Download: https://visualstudio.microsoft.com/downloads/
REM Chọn: Desktop development with C++

REM Cài CMake
REM Download: https://cmake.org/download/

REM Cài face-recognition
pip install cmake
pip install dlib
pip install face-recognition
```

Sau đó sửa code để dùng `face-recognition` thay vì `mediapipe`.

## 🎯 Khuyến nghị

**→ Dùng Python 3.11** là cách đơn giản và nhanh nhất!

### Tại sao?
- ✅ MediaPipe hỗ trợ đầy đủ
- ✅ Không cần compile
- ✅ Cài đặt nhanh (2-3 phút)
- ✅ Stable, ít lỗi

### Kiểm tra Python version:

```cmd
python --version
py -3.11 --version
```

## 📝 Sau khi cài Python 3.11

```cmd
REM 1. Xóa venv cũ
rmdir /s /q face_env

REM 2. Tạo venv mới với Python 3.11
py -3.11 -m venv face_env

REM 3. Kích hoạt
face_env\Scripts\activate

REM 4. Check version (phải là 3.11.x)
python --version

REM 5. Cài đặt
pip install --upgrade pip
pip install -r requirements.txt

REM 6. Chạy
python main.py
```

## ✨ Kết quả

Sau khi dùng Python 3.11, mọi thứ sẽ chạy smooth! 🎉

---

**Lưu ý:** MediaPipe thường hỗ trợ Python versions 3.8 - 3.11. Version 3.13 quá mới nên chưa được hỗ trợ.
