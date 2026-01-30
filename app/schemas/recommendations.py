from pydantic import BaseModel, Field, ConfigDict


class Recommendation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID рекомендации")
    user_id: int = Field(..., description="ID пользователя")
    item_id: int = Field(..., description="ID товара")

class RecommendationCreate(BaseModel):
    user_id: int = Field(..., gt=0, description="ID пользователя")
    min_pair_count: int = Field(default=5, gt=0, description="Минимальное количество совместных покупок")
