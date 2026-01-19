from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    id: int = Field(..., description="ID рекомендации")
    user_id: int = Field(..., description="ID пользователя")
    item_id: int = Field(..., description="ID товара")
