# heart_failure
## Cài đặt MongoDB để làm Database
- Truy cập MongoDB Atlas để tạo tài khoản và đăng nhập
- Tải MongoDB Compass để truy cập từ local. Nhấn "Add new connection", nhập vào ô URI chuỗi: "mongodb+srv://<<user_name>>:m7lNjMGLn3mzAAAx@heartprediction.ursbr.mongodb.net/" (thay <<username>> bằng tên đăng nhập đã tạo từ trước) <br>
## Đảm bảo máy đã cài đặt Python 3.8+ và Node
## Cài đặt FastAPI
- Clone dự án về
- Tạo file .env cùng cấp với folder "app", nội dung: <br>
MONGO_URL = "mongodb+srv://<<user_name>>:m7lNjMGLn3mzAAAx@heartprediction.ursbr.mongodb.net/" <br>
DATABASE_NAME=heart_prediction
- Mở terminal và chạy các lệnh sau: <br>
  cd backend <br>
  pip install fastapi uvicorn motor python-dotenv passlib[bcrypt] jose pydantic[email] <br>
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8080 (Nếu bị lỗi thì thử đổi port khác) <br>
Truy cập vào Swagger để xem API:[ http://21.64.1.254:8080/docs](http://127.0.0.1:8000/docs
)
