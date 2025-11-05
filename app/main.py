from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.modules.categories.controllers.category_controller import router as categories_router
# from app.modules.configuration.controllers.configuration_controller import router as configuration_router
from app.modules.websites.controllers.website_controller import router as website_router
from app.modules.websites.controllers.website_user_controller import router as website_user_router
from app.modules.websites.controllers.website_visited_controller import router as website_visited_router
app = FastAPI(
    title="FocusGuard API",
    description="Sistema para detectar y reducir procrastinación digital",
    version="1.0.0"
)

# Configurar CORS

#EXTENSION_ORIGIN = "chrome-extension://jmnlmmgpeadljmioaojnmihpoddebcml"

#origins = [
#    "http://localhost",
#    "http://localhost:8000",
#    EXTENSION_ORIGIN,  # ID de la extensión
#]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# app.include_router(categories_router, prefix="/api/v1")
# app.include_router(configuration_router, prefix="/api/v1")
app.include_router(website_router, prefix="/api/v1")
app.include_router(website_user_router, prefix="/api/v1")
app.include_router(website_visited_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "FocusGuard API is running!", "mode": "development"}

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy", "modules": ["categories", "configuration"]}
