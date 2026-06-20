from fastapi import FastAPI
from src.database.database import engine, Base
from src.routers.user_router import router as user_router
from src.auth.login_router import router as login_router
from src.routers.project_router import router as project_router
from src.routers.admin_user import router as admin_router

from slowapi.errors import RateLimitExceeded
from src.rate_limit.rate_limit import limiter
from slowapi import _rate_limit_exceeded_handler

from guard import SecurityConfig, SecurityMiddleware

from fastapi.middleware.cors import CORSMiddleware

config = SecurityConfig(
    rate_limit=2
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(SecurityMiddleware, config=config)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(login_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(project_router)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
