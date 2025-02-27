"""This is the entry point of the FastAPI application."""
from fastapi import FastAPI

from routes import router

app = FastAPI(
    title="Test task",
    description="A test task with Signup, Login, AddPost, GetPosts, and DeletePost endpoints.",
    version="1.0.0",
)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
