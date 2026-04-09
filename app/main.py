from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.modules.categories.controllers.category_controller import router as categories_router
# from app.modules.configuration.controllers.configuration_controller import router as configuration_router
from app.modules.websites.controllers.website_controller import router as website_router
from app.modules.websites.controllers.website_user_controller import router as website_user_router
from app.modules.websites.controllers.website_visited_controller import router as website_visited_router
from app.modules.categories.controllers.category_website_controller import router as category_website_router
from app.modules.categories.controllers.category_content_controller import router as category_content_router
from app.modules.categories.controllers.category_controller import router as change_category_router
from app.modules.users.controllers.user_controller import router as user_router
from app.modules.contents.controllers.content_controller import router as content_router
from app.modules.contents.controllers.content_user_controller import router as content_user_router
from app.modules.contents.controllers.content_visited_controller import router as content_visited_router
from app.modules.ml_clasification.controllers.ml_prediction_controller import router as ml_prediction_controller
from app.modules.goals.controllers.goal_controller import router as goal_router
from app.modules.objectives.controllers.weekly_goal_controller import router as weekly_goal_router
from app.modules.objectives.controllers.daily_progress_controller import router as daily_progress_router
from app.modules.configuration.controllers.rest_time_controller import router as rest_time_router
from app.modules.reports.controllers.top_site_controller import router as top_site_router

app = FastAPI(
    title="FocusGuard API",
    description="Sistema para detectar y reducir procrastinación digital",
    version="1.0.0"
)

# Configurar CORS

#EXTENSION_ORIGIN = "chrome-extension://jmnlmmgpeadljmioaojnmihpoddebcml"

#origins = [
#    "http://localhost",
#    "http://localhost:8000"
#   #EXTENSION_ORIGIN,  # ID de la extensión
#]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# app.include_router(categories_router, prefix="/api/v1")
# app.include_router(configuration_router, prefix="/api/v1")

app.include_router(rest_time_router, prefix="/api/v1")

app.include_router(top_site_router, prefix="/api/v1")
app.include_router(goal_router, prefix="/api/v1")
app.include_router(weekly_goal_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(category_website_router, prefix="/api/v1")
app.include_router(change_category_router, prefix="/api/v1")
app.include_router(category_content_router, prefix="/api/v1")
app.include_router(website_router, prefix="/api/v1")
app.include_router(website_user_router, prefix="/api/v1")
app.include_router(website_visited_router, prefix="/api/v1")
app.include_router(content_router, prefix="/api/v1")
app.include_router(content_user_router, prefix="/api/v1")
app.include_router(content_visited_router, prefix="/api/v1")
app.include_router(ml_prediction_controller, prefix="/api/v1")

app.include_router(weekly_goal_router, prefix="/api/v1")
app.include_router(daily_progress_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "FocusGuard API is running!", "mode": "development"}

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy", "modules": ["categories", "configuration"]}
