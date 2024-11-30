from fastapi import FastAPI
from database import Base, engine
from routes.review_routes import router as review_router
from routes.auth_routes import router as auth_router 

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(review_router, prefix="/api", tags=["Reviews"])
app.include_router(auth_router, prefix="/auth")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_review:app", host="127.0.0.1", port=8003, reload=True)
