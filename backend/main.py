from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.admin import router as admin_router
from routes.menu import router as menu_router

app = FastAPI(title="Cafeteria App")

# 🔥 ADD THIS (CORS MIDDLEWARE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # DEV only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(admin_router)
app.include_router(menu_router)

@app.get("/")
def health_check():
    return {"status": "Backend running"}
