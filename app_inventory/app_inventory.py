from fastapi import FastAPI
from database import Base, engine
from routes.inventory_routes import router as inventory_router
from routes.auth_routes import router as auth_router 

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(inventory_router, prefix="/api", tags=["Inventory"])
app.include_router(auth_router, prefix="/auth")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_inventory:app", host="127.0.0.1", port=8001, reload=True)
