from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, credentials, fanfix
from app.models.base import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FanFix Login Tool API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://*", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(credentials.router, prefix="/credentials", tags=["credentials"])
app.include_router(fanfix.router, prefix="/fanfix", tags=["fanfix"])


@app.get("/")
async def root():
    return {"message": "FanFix Login Tool API"}