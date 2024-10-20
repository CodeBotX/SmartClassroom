import sqlite3
import pandas as pd
import os

# Kết nối đến cơ sở dữ liệu SQLite
conn = sqlite3.connect('db.sqlite3')

# Đường dẫn đến thư mục backup
backup_folder = 'backup'

# Lặp qua từng file CSV trong thư mục backup
for filename in os.listdir(backup_folder):
    if filename.endswith('.csv'):
        table_name = filename[:-4]  # Lấy tên bảng từ tên file
        df = pd.read_csv(os.path.join(backup_folder, filename))

        for index, row in df.iterrows():
            try:
                # Thêm từng bản ghi
                row.to_frame().T.to_sql(table_name, conn, if_exists='append', index=False)
            except sqlite3.IntegrityError:
                # Bỏ qua bản ghi nếu có lỗi
                print(f"Skipped duplicate entry for {row}")

# Đóng kết nối
conn.close()
print("Data restoration completed.")
