import sqlite3
import pandas as pd
import os

# Kết nối đến cơ sở dữ liệu
conn = sqlite3.connect('db.sqlite3')

# Lấy danh sách các bảng
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)

# Tạo thư mục backup nếu chưa tồn tại
backup_folder = 'backup'
os.makedirs(backup_folder, exist_ok=True)

# Xuất dữ liệu từ từng bảng vào thư mục backup
for table_name in tables['name']:
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    df.to_csv(os.path.join(backup_folder, f"{table_name}.csv"), index=False)

# Đóng kết nối
conn.close()
