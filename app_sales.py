from fastapi import FastAPI
from routes.sales_routes import router as sales_router
from database import Base, engine
from routes.auth_routes import router as auth_router 

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(sales_router, prefix="/api", tags=["Sales"])
app.include_router(auth_router, prefix="/auth")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_sales:app", host="127.0.0.1", port=8002, reload=True)