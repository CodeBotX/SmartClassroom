# SmartClassroom

## Giới thiệu
Dự án **SmartClassroom** là hệ thống "Lớp học thông minh" sử dụng Django cho backend và Vue.js cho frontend. Hệ thống này cung cấp các tính năng quản lý học sinh, điểm danh bằng RFID, tương tác giữa học sinh, giáo viên và phụ huynh.
### Thành Viên
- **Lê Minh Tiến**
- **Nguyễn Tuấn Anh**
- **Nguyễn Minh Hiếu**


## Cấu trúc thư mục dự án
```bash
SmartClassroom/
├── backend/              # Mã nguồn Django
├── frontend/             # Mã nguồn Vue.js
├── .gitignore            # File cấu hình để bỏ qua các file 
├── requirements.txt      # File lưu các package cần thiết 
└── README.md             # Hướng dẫn dự án
```

## Hướng dẫn thiết lập môi trường phát triển
### 1. Khởi tạo môi trường Python.

Bước 1: Di chuyển ra khỏi thư mục SmartClassroom để tạo môi trường ảo Python bên ngoài dự án: 
```bash 
cd.. 
```

Bước 2: Khởi tạo môi trường ảo Python, nếu đã có hoặc không muốn thì có thể bỏ qua bước này:
```bash 
python -m venv venv 
```
Bước 3: Kích hoạt môi trường ảo:
- Trên Windows:
```bash 
venv\Scripts\activate
```
Hoặc
```bash 
.\Scripts\Activate.ps1   
```
- Trên macOS/Linux:

```bash 
source venv/bin/activate
```

### 2. Cài đặt các package Python
Bước 1: Sau khi môi trường ảo được kích hoạt, di chuyển vào thư mục backend:
```bash 
cd SmartClassroom/backend
```
Bước 2: Cài đặt các package cần thiết từ file requirements.txt:
```bash 
pip install -r ../requirements.txt
```
Bước 3: Nếu cần cài đặt thêm các package riêng lẻ, sử dụng lệnh:
```bash 
pip install <package-name>
```
Sau khi cài đặt xong, cập nhật file requirements.txt:
```bash 
pip freeze > ../requirements.txt
```
#### Danh sách các package trong requirements hiện tại:
- pandas
- djangorestframework
- markdown
- django-filter
- requests
- django-cors-headers

### 3. Cấu hình Django
Bước 1: Chạy các lệnh migrate để tạo cơ sở dữ liệu:
```bash 
python manage.py migrate
```
Bước 2: Chạy server phát triển Django:
```bash 
python manage.py runserver
```
### 4. Thiết lập môi trường frontend
Bước 1: Di chuyển vào thư mục frontend:
```bash 
cd ../frontend
```

Bước 2: Cài đặt các package Vue.js:
```bash 
npm install
```

Bước 3: Chạy server phát triển Vue.js:
```bash 
npm run dev
```
- front end chạy trên port 127.0.0.1:8080

### 5. Cấu hình .gitignore
Đảm bảo rằng file .gitignore đã được cấu hình để bỏ qua các thư mục và file không cần thiết.


## Hướng dẫn sử dụng Git

### 1. Clone dự án
Để bắt đầu phát triển, bạn cần clone dự án về máy của mình:
```bash
git clone <repository-url>
```
Dự án sẽ được clone với cấu trúc như sau:
```bash
SmartClassroom/
├── backend/              # Mã nguồn Django
├── frontend/             # Mã nguồn Vue.js
├── .gitignore            # Git ignore file
├── requirements.txt      # Backend dependencies
└── README.md             # Project documentation
```

### 2. Quản lý backend (Django)
Di chuyển vào thư mục `backend` để quản lý phần mã nguồn của **backend**:
```bash
cd backend
```

#### Thao tác Git cho backend:
- **Kiểm tra trạng thái thay đổi:**
    ```bash
    git status
    ```

- **Thêm các thay đổi vào staged:**
    ```bash
    git add .
    ```

- **Commit các thay đổi:**
    ```bash
    git commit -m "Mô tả thay đổi cho backend"
    ```

- **Đẩy thay đổi lên remote repository:**
    ```bash
    git push origin <branch-name>
    ```

### 3. Quản lý frontend (Vue.js)
Di chuyển vào thư mục `frontend` để quản lý phần mã nguồn của **frontend**:
```bash
cd frontend
```

#### Thao tác Git cho frontend:
- **Kiểm tra trạng thái thay đổi:**
    ```bash
    git status
    ```

- **Thêm các thay đổi vào staged:**
    ```bash
    git add .
    ```

- **Commit các thay đổi:**
    ```bash
    git commit -m "Mô tả thay đổi cho frontend"
    ```

- **Đẩy thay đổi lên remote repository:**
    ```bash
    git push origin <branch-name>
    ```

### 4. Làm việc với các branch
Nếu bạn làm việc với nhiều branch, bạn có thể sử dụng các lệnh sau để quản lý:
- **Tạo branch mới:**
    ```bash
    git checkout -b <new-branch-name>
    ```

- **Chuyển đổi giữa các branch:**
    ```bash
    git checkout <branch-name>
    ```

- **Xem danh sách các branch:**
    ```bash
    git branch
    ```

### 5. Pull thay đổi từ remote repository
Trước khi thực hiện thêm các thay đổi, bạn nên **pull** các thay đổi mới nhất từ remote repository để tránh xung đột:
```bash
git pull origin <branch-name>
```

### 6. Đẩy cả frontend và backend lên repository
Sau khi bạn hoàn thành công việc trong cả hai thư mục `frontend` và `backend`, bạn có thể đẩy tất cả thay đổi lên remote repository:
```bash
# Trong thư mục gốc của dự án
git add .
git commit -m "Cập nhật cả frontend và backend"
git push origin <branch-name>
```

## Lưu ý
- **Sử dụng môi trường ảo** khi làm việc với backend (Django).
- **Cập nhật** file `requirements.txt` khi cài đặt thêm các package cho backend.
- **Sử dụng `npm install`** trong thư mục `frontend` để đảm bảo tất cả package cho Vue.js được cài đặt đầy đủ.
