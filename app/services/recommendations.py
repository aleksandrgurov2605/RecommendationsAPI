from app.schemas.recommendations import Recommendation
from app.utils.logger import logger
from app.utils.unitofwork import IUnitOfWork


class RecommendationService:
    @staticmethod
    async def generate_recommendations(
        uow: IUnitOfWork, user_id: int, min_pair_count: int
    ):
        total_transactions = await uow.purchase.get_count_purchases()
        recommendations = await uow.purchase_unit.generate_recommendations(
            {
                "user_id": user_id,
                "total_transactions": total_transactions,
                "min_pair_count": min_pair_count,
            }
        )
        logger.debug(f"RecommendationService: {recommendations=}")
        if recommendations:
            rec_dict = {
                "user_id": user_id,
                "item_id": recommendations[0].get("recommended_item_id"),
            }
            recommendations_from_db = await uow.recommendation.fetch_one(
                user_id=user_id
            )
            logger.debug(f"RecommendationService: {recommendations_from_db=}")
            if recommendations_from_db:
                await uow.recommendation.update(rec_dict, recommendations_from_db.id)
            else:
                await uow.recommendation.add_one(rec_dict)
            logger.debug(f"RecommendationService: {rec_dict=}")
            await uow.commit()

    @staticmethod
    async def get_recommendations(uow: IUnitOfWork, user_id: int):
        async with uow:
            recs = await uow.recommendation.fetch_one(user_id=user_id)
            logger.debug(f"RecommendationService: {recs=}")
            return Recommendation.model_validate(recs) if recs else None
