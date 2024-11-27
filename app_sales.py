from fastapi import FastAPI
from routes.sales_routes import router as sales_router
from database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(sales_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_services:app", host="127.0.0.1", port=8002, reload=True)
