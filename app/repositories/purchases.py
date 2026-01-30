from sqlalchemy import Float, cast, func, select
from sqlalchemy.orm import aliased

from app.models import Item
from app.models.purchases import Purchase, PurchaseUnit
from app.repositories.base_repository import Repository


class PurchaseRepository(Repository):
    model = Purchase

    async def get_purchases(self, **filter_by):
        """
        Получить покупки пользователя.
        :param filter_by:
        :return:
        """
        current_user_id = filter_by["current_user_id"]
        page = filter_by["page"]
        page_size = filter_by["page_size"]

        stmt = (
            select(self.model)
            .where(self.model.user_id == current_user_id)
            .order_by(self.model.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        purchases = await self.session.execute(stmt)
        return purchases.scalars().all()

    async def get_count_purchases(self):
        """
        Получить общее количество покупок.
        :return:
        """
        total_tx_stmt = select(func.count(Purchase.id))
        total_transactions = (await self.session.execute(total_tx_stmt)).scalar() or 1
        return total_transactions

    async def get_count_user_purchases(self, current_user_id: int):
        """
        Получить все записи из таблицы в БД, списком
        :return:
        """
        stmt = select(func.count(self.model.id)).where(
            self.model.user_id == current_user_id
        )
        count = await self.session.execute(stmt)
        return count.first()


class PurchaseUnitRepository(Repository):
    model = PurchaseUnit

    async def generate_recommendations(self, filter_by):
        """

        :param filter_by:
        :return:
        """
        user_id = filter_by["user_id"]
        total_transactions = filter_by["total_transactions"]
        min_pair_count = filter_by["min_pair_count"]

        # 1. Получаем историю покупок пользователя
        user_history_stmt = (
            select(self.model.item_id)
            .join(Purchase, Purchase.id == self.model.purchase_id)
            .where(Purchase.user_id == user_id)
        )
        history_res = await self.session.execute(user_history_stmt)
        user_bought_ids = list(set(history_res.scalars().all()))

        if not user_bought_ids:
            return []

        # 2. CTE для частоты товаров
        item_counts_cte = (
            select(
                self.model.item_id.label("item_id"),
                func.count(self.model.id).label("total_cnt"),
            )
            .group_by(self.model.item_id)
            .cte("item_counts")
        )

        # 3. CTE для расчета матрицы Lift (база знаний)
        # Это решает проблему "misuse of aggregate function"
        pu1, pu2 = aliased(self.model), aliased(self.model)
        ic1, ic2 = aliased(item_counts_cte), aliased(item_counts_cte)

        knowledge_base_cte = (
            select(
                pu1.item_id.label("id_a"),
                pu2.item_id.label("id_b"),
                (
                        cast(func.count(pu1.id) * total_transactions, Float)
                        / (ic1.c.total_cnt * ic2.c.total_cnt)
                ).label("lift_value"),
            )
            .join(pu2, pu1.purchase_id == pu2.purchase_id)
            .join(ic1, ic1.c.item_id == pu1.item_id)
            .join(ic2, ic2.c.item_id == pu2.item_id)
            .where(
                pu1.item_id != pu2.item_id
            )  # Нам нужны оба направления (A->B и B->A)  # noqa: E501
            .group_by(pu1.item_id, pu2.item_id, ic1.c.total_cnt, ic2.c.total_cnt)
            .having(func.count(pu1.id) >= min_pair_count)
            .cte("knowledge_base")
        )

        # 4. Финальный выбор: сопоставляем историю пользователя с базой знаний
        kb = aliased(knowledge_base_cte)
        item_info = aliased(Item)

        final_stmt = (
            select(
                item_info.id.label("recommended_item_id"),
                item_info.name.label("recommended_item_name"),
                func.max(kb.c.lift_value).label("lift"),
            )
            .join(item_info, item_info.id == kb.c.id_b)
            # Условие: товар А из пары уже куплен пользователем
            .where(kb.c.id_a.in_(user_bought_ids))
            # Условие: товара Б еще нет в истории пользователя
            .where(kb.c.id_b.not_in(user_bought_ids))
            .group_by(item_info.id, item_info.name)
            .order_by(func.max(kb.c.lift_value).desc())
            .limit(10)
        )

        result = await self.session.execute(final_stmt)
        return result.mappings().all()
