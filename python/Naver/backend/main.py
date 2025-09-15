from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from package.database import SessionLocal, engine, Base
from package.models import Todo
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS để React frontend gọi được
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # production thay bằng domain của bạn
    allow_methods=["*"],
    allow_headers=["*"]
)

# Pydantic schemas
class TodoSchema(BaseModel):
    text: str
    completed: bool = False

class TodoUpdateSchema(BaseModel):
    text: str
    completed: bool

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

@app.post("/todos")
def create_todo(todo: TodoSchema, db: Session = Depends(get_db)):
    db_todo = Todo(text=todo.text, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoUpdateSchema, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.text = todo.text
    db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return {"detail": "Deleted"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",   # "tên_file:instance_app"
        host="0.0.0.0",
        port=8000,
        reload=True,   # tự reload khi thay đổi code
        log_level="info"
    )
