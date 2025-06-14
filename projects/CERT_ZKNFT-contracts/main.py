from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import university, student, employer

app = FastAPI(
    title="CERT-ZKNFT Backend",
    description="ZK NFT Certificate Backend System",
    version="1.0.0"
)

# ✅ CORS Middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:5173"] for stricter policy
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include your routers
app.include_router(university.router)
app.include_router(student.router)
app.include_router(employer.router)
