# SmartClassroom

## Giới thiệu
Dự án **SmartClassroom** là hệ thống "Lớp học thông minh" sử dụng Django cho backend và Vue.js cho frontend. Hệ thống bao gồm các chức năng quản lý, làm tăng tương tác giữa học sinh, giáo viên và phụ huynh, điểm danh bằng RFID, và nhiều hơn nữa.

## Cấu trúc thư mục dự án
SmartClassroom/ ├── backend/ # Mã nguồn Django ├── frontend/ # Mã nguồn Vue.js ├── .gitignore # File cấu hình để bỏ qua các file không cần thiết ├── requirements.txt # File lưu các package cần thiết cho Django backend └── README.md # Hướng dẫn dự án


## Hướng dẫn thiết lập môi trường phát triển

### 1. Khởi tạo môi trường Python

**Bước 1:** Di chuyển ra khỏi thư mục `SmartClassroom` để tạo môi trường ảo Python bên ngoài dự án:

```bash
cd ..
Bước 2: Khởi tạo môi trường ảo Python với tên venv (hoặc tên khác mà bạn muốn):
python -m venv venv


Dưới đây là file README.md hoàn chỉnh với các yêu cầu về cài đặt module Python và vị trí của file requirements.txt:

markdown
Sao chép mã
# SmartClassroom

## Giới thiệu
Dự án **SmartClassroom** là hệ thống điểm danh học sinh sử dụng Django cho backend và Vue.js cho frontend. Hệ thống bao gồm các chức năng quản lý học sinh, điểm danh bằng RFID, và nhiều hơn nữa.

## Cấu trúc thư mục dự án

SmartClassroom/ ├── backend/ # Mã nguồn Django ├── frontend/ # Mã nguồn Vue.js ├── .gitignore # File cấu hình để bỏ qua các file không cần thiết ├── requirements.txt # File lưu các package cần thiết cho Django backend └── README.md # Hướng dẫn dự án

less
Sao chép mã

## Hướng dẫn thiết lập môi trường phát triển

### 1. Khởi tạo môi trường Python

**Bước 1:** Di chuyển ra khỏi thư mục `SmartClassroom` để tạo môi trường ảo Python bên ngoài dự án:

```bash
cd ..
Bước 2: Khởi tạo môi trường ảo Python với tên venv (hoặc tên khác mà bạn muốn):
Bước 3: Kích hoạt môi trường ảo:
Trên Windows: <venv>\Scripts\activate
Trên macOS/Linux:source venv/bin/activate

###2. Cài đặt các package Python
Bước 1: Sau khi môi trường ảo được kích hoạt, di chuyển vào thư mục backend của dự án:
cd SmartClassroom/backend
Bước 2: Cài đặt các package cần thiết từ file requirements.txt (file này nên đặt trong thư mục gốc SmartClassroom):
pip install -r ../requirements.txt
Bước 3: Nếu bạn cần cài đặt thêm các package riêng lẻ, có thể sử dụng lệnh:
pip install <package-name>
Danh sách các package cần thiết đến thời điểm hiện tại:
pip install pandas
pip install djangorestframework
pip install markdown       
pip install django-filter  
pip install requests
pip install django-cors-headers
Sau khi cài đặt xong các package, bạn nên cập nhật file requirements.txt:
pip freeze > ../requirements.txt
###3. Cấu hình Django
Bước 1: Tạo file .env để lưu các biến môi trường (nếu cần) dựa trên file .env.example có sẵn.
Bước 2: Chạy các lệnh migrate để tạo các bảng cơ sở dữ liệu:
Bước 3: Chạy server phát triển:

###4. Thiết lập frontend
Bước 1: Di chuyển vào thư mục frontend:
cd ../frontend
Bước 2: Cài đặt các package Vue.js:
npm install
Bước 3: Chạy server phát triển cho frontend:
npm run dev

###5. Cấu hình .gitignore
Đảm bảo rằng file .gitignore đã được cấu hình để bỏ qua các thư mục không cần thiết như venv/ và node_modules/ trong cả frontend và backend.

# .gitignore trong thư mục gốc
venv/
frontend/node_modules/
backend/__pycache__/
backend/*.pyc
backend/*.log

###Hướng dẫn sử dụng Git

1. Clone dự án
Để bắt đầu phát triển, hãy clone dự án về máy:
git clone <repository-url>
2. Cấu hình Git
Sau khi clone, đảm bảo rằng môi trường ảo venv/ và các thư mục không cần thiết khác đã được bỏ qua bằng cách kiểm tra file .gitignore.

Ghi chú
Luôn kích hoạt môi trường ảo trước khi làm việc với dự án Django.
Kiểm tra và cập nhật requirements.txt khi cài đặt thêm bất kỳ package nào mới.
Kiểm tra npm install để đảm bảo tất cả các package Vue.js đã được cài đặt đầy đủ.
