from fastapi import FastAPI
from database import Base, engine
from routes.inventory_routes import router as inventory_router

# Initialize database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Register routes
app.include_router(inventory_router, prefix="/api/inventory", tags=["Inventory"])
