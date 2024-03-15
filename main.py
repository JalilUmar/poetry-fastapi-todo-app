from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from user.users import router as UserRouter
from todo.todos import router as TodoRouter
from user import models as user_models
from todo import models as todo_models
from database import engine

app = FastAPI()


# added CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# binded Models
user_models.Base.metadata.create_all(bind=engine)
todo_models.Base.metadata.create_all(bind=engine)


@app.get("/api/health", status_code=status.HTTP_200_OK)
def hello_world():
    return {"message": "Hello World! I am healthy."}


app.include_router(UserRouter)
app.include_router(TodoRouter)
