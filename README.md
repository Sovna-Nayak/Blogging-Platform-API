Blogging Platform API (Microservices Architecture)

Objective:
Build a scalable blogging API with separate microservices for authentication, posts, and comments.

Features:
1.Users can create accounts and log in
2.Users can create, edit, delete blog posts
3.Users can comment on posts

Follows microservices architecture
Implementation Steps:
1. Create 3 microservices:
auth-service: Handles user authentication
post-service: Manages blog posts
comment-service: Manages comments

2. Use PostgreSQL for each service with separate databases.
3. Implement service-to-service communication using REST or RabbitMQ.
4. Use an API Gateway (FastAPI or Kong) to unify API requests.
📌 Deliverable: A microservices-based blogging API with authentication, posts, and comments.

This is the project Structure-blogging-platform-api/
│
│ 
├── auth-service/
│   ├── main.py                     # FastAPI app for signup/login/token
│   ├── models.py                   # SQLAlchemy User model
│   ├── schemas.py                  # Pydantic models for request/response
│   ├── crud.py                     # DB CRUD helpers
│   ├── deps.py                     # DB Session setup also connection
│   └── .env                        # DB credentials, JWT_SECRET, etc.
│
├── post-service/
│   ├── main.py                     # FastAPI app for CRUD on posts
│   ├── models.py                   # SQLAlchemy Post model
│   ├── schemas.py                  # Pydantic schemas
│   ├── requirements.txt
├── comment-service/
│   ├── main.py                     # FastAPI app for managing comments
│   ├── models.py                   # Comment model (with post_id, author)
│   ├── schemas.py                  # CommentCreate, CommentOut, etc.
│  
│
└── README.md                       # Documentation on how to run everything
├── main.py                         # auth-service + post-service + comment-service in 1 file

