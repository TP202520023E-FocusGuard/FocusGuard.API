from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.modules.categories.services.category_service import CategoryService
from app.modules.categories.schemas.category_schema import (
    CategoriaBase, 
    CategoriaUsuarioCreate, 
    CategoriaUsuarioUpdate, 
    CategoriaConSeleccion
)

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[CategoriaBase])
async def get_categories(
    db: AsyncSession = Depends(get_db)
):
    """Get all base categories in the system"""
    try:
        service = CategoryService(db)
        return await service.get_all_categories()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting categories: {str(e)}"
        )

@router.get("/selected/{user_id}", response_model=List[CategoriaConSeleccion])
async def get_user_categories(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get categories selected by user"""
    try:
        service = CategoryService(db)
        return await service.get_categories_with_selection(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting user categories: {str(e)}"
        )

@router.post("/selected/{user_id}", response_model=List[CategoriaConSeleccion])
async def save_category_selection(
    user_id: int,
    request: CategoriaUsuarioUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Save user category selection"""
    try:
        service = CategoryService(db)
        return await service.save_user_selection(user_id, request.categorias)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving selection: {str(e)}"
        )