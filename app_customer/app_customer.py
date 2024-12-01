from fastapi import FastAPI
from routes.customer_routes import router as customer_router
from routes.auth_routes import router as auth_router 
from database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(customer_router, prefix="/api")
app.include_router(auth_router, prefix="/auth")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_customer:app", host="127.0.0.1", port=8000, reload=True)

