    # BE
    ├── migrations/                  # Script quản lý schema database 
    ├── scripts/                     # Các script tiện ích
    │   └── run_postgres.sh          # Script khởi chạy Postgres
    ├── src/
    │   ├── api/                     # API Layer
    │   │   ├── controllers/         # Controllers (RESTful endpoints)
    │   │   ├── schemas/             # Marshmallow schemas (validate request/response)
    │   │   ├── middleware.py        # Middleware (auth, logging, etc.)
    │   │   ├── responses.py         # Chuẩn hoá response format
    │   │   └── requests.py          # Xử lý request đầu vào
    │   │
    │   ├── infrastructure/          # Infrastructure Layer
    │   │   ├── services/            # Tích hợp service bên ngoài (email, payment,…)
    │   │   ├── databases/           # Kết nối & khởi tạo database
    │   │   ├── repositories/        # Repository pattern 
    │   │   └── models/              # ORM models 
    │   │
    │   ├── domain/                  # Domain Layer
    │   │   ├── constants.py         # Các hằng số của domain
    │   │   ├── exceptions.py        # Custom exception
    │   │   ├── models/              # Domain models (business logic)
    │   │
    │   ├── services/                # Application services 
    │   │
    │   ├── app.py                   
    │   ├── config.py                
    │   ├── cors.py                  
    │   ├── create_app.py            
    │   ├── dependency_container.py  
    │   ├── error_handler.py         
    │   └── logging.py               
