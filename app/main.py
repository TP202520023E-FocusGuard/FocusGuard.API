from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.categories.controllers.category_controller import router as categories_router
from app.modules.configuration.controllers.configuration_controller import router as configuration_router
from app.modules.sites.controllers.site_controller import router as sites_router

app = FastAPI(
    title="FocusGuard API",
    description="Sistema para detectar y reducir procrastinación digital",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(categories_router, prefix="/api/v1")
app.include_router(configuration_router, prefix="/api/v1")
app.include_router(sites_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "FocusGuard API is running!", "mode": "development"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "modules": ["categories", "configuration", "sites"]}