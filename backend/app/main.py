from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="LifeOS API",
    description="Autonomous Personal Operations Agent",
    version="0.1.0",
)


# Allow our Next.js frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "name": "LifeOS",
        "description": "Autonomous Personal Operations Agent",
        "status": "running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }