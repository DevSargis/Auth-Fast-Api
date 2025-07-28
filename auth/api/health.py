from fastapi import APIRouter
from auth.models.dto.api_dto import HealthCheckResponseDTO

router = APIRouter()

@router.get("/health", response_model=HealthCheckResponseDTO)
async def health_check():
    return HealthCheckResponseDTO(status="healthy") 