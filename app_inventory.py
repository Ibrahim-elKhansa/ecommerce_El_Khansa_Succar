from fastapi import FastAPI
from database import Base, engine
from routes.inventory_routes import router as inventory_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(inventory_router, prefix="/api", tags=["Inventory"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_inventory:app", host="127.0.0.1", port=8001, reload=True)
