from fastapi import FastAPI
from sqlalchemy import text
from app.database import Base, engine
from app.models.user import User
from app.api.user import router as user_router

app = FastAPI(title="Niyati Python Fullstack Template")

Base.metadata.create_all(bind=engine)

app.include_router(user_router)

@app.get("/")
def home():
    return {
        "message": "Clinic API Running"
    }

@app.get('/health')
def health():
    return {'ok': True, 'service': 'api', 'stack': 'python'}


@app.get('/api/version')
def version():
    return {'version': 'starter-v1', 'runtime': 'python', 'deploy_target': 'render'}


@app.get('/api/ping')
def ping():
    return {'ok': True, 'message': 'pong'}


@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT NOW()"))
            return {
                "status": "Connected",
                "database_time": str(result.scalar())
            }
    except Exception as e:
        return {
            "status": "Failed",
            "error": str(e)
        }
