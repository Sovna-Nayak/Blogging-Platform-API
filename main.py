from fastapi import FastAPI

# Import routers from each service
from Auth.main import router as auth_router
from comment_service.main import router as comment_router
from Post_Service.main import router as post_router

app = FastAPI(title="Blogging Platform API")

# Include routers from each microservice
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(post_router, prefix="/posts", tags=["Posts"])
app.include_router(comment_router, prefix="/comments", tags=["Comments"])

# Optional root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Blogging Platform API"}
