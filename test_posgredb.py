import psycopg2
import os

# Lấy URL từ biến môi trường hoặc dùng mặc định
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:12345@localhost:5432/chatbot")

try:
    # Kết nối với PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Test query
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print("✅ Kết nối thành công! Phiên bản PostgreSQL:", db_version[0])

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Lỗi kết nối:", e)
