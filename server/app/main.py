from fastapi import FastAPI
from app.routes import router
from app.database import create_database
from app.config import settings

app = FastAPI()

# Ensure the database and tables are created on startup
create_database()

# Include routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)

