from app.schemas.recommendations import Recommendation
from app.schemas.users import UserRead
from app.utils.logger import logger
from app.utils.unitofwork import IUnitOfWork


class RecommendationService:
    @staticmethod
    async def generate_recommendations(
            uow: IUnitOfWork,
            user_id: int,
            min_pair_count: int
    ):
        total_transactions = await uow.purchase.get_count_purchases()
        recommendations = await uow.purchase_unit.generate_recommendations(
            {
                "user_id":user_id,
                "total_transactions":total_transactions,
                "min_pair_count":min_pair_count
            }
        )
        logger.debug(f"RecommendationService: {recommendations=}")
        if recommendations:
            recommendation_dict = {"user_id": user_id, "item_id": recommendations[0].get("recommended_item_id")}
            recommendations_from_db = await uow.recommendation.fetch_one(user_id)
            logger.debug(f"RecommendationService: {recommendations_from_db=}")
            if recommendations_from_db:
                await uow.recommendation.update(recommendation_dict, recommendations_from_db.id)
            else:
                await uow.recommendation.add_one(recommendation_dict)
            logger.debug(f"RecommendationService: {recommendation_dict=}")
            await uow.commit()

    @staticmethod
    async def get_recommendations(
            uow: IUnitOfWork,
            user_id: int
    ):
        async with uow as uow:
            recommendations = await uow.recommendation.fetch_one(user_id)
            logger.debug(f"RecommendationService: {recommendations=}")
            return Recommendation.model_validate(recommendations) if recommendations else None
            # return recommendations