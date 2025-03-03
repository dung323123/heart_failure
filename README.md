# heart_failure
## Cài đặt MongoDB để làm Database
- Truy cập MongoDB Atlas để tạo tài khoản và đăng nhập
- Tải MongoDB Compass để truy cập từ local. Nhấn "Add new connection", nhập vào ô URI chuỗi: mongodb+srv://<username>:m7lNjMGLn3mzAAAx@heartprediction.ursbr.mongodb.net/ (thay username bằng tên đăng nhập đã tạo từ trước)
## Đảm bảo máy đã cài đặt Python 3.8+ và Node
## Cài đặt FastAPI
- Clone dự án về
- Tạo file .env cùng cấp với folder "app", nội dung: 
MONGO_URL = mongodb+srv://<username>:m7lNjMGLn3mzAAAx@heartprediction.ursbr.mongodb.net/
DATABASE_NAME=heart_prediction
- Mở terminal và chạy các lệnh sau:
  cd backend
  pip install fastapi uvicorn motor python-dotenv passlib[bcrypt] jose pydantic[email]
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8080 (Nếu bị lỗi thì thử đổi port khác)
Truy cập vào Swagger để xem API: http://21.64.1.254:8080/docs
