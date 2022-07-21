from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api import deps
from app.schemas import LikeStatistic

router = APIRouter()


@router.get('/likes-for-day/', summary='Get amount of likes for a day', response_model=LikeStatistic)
async def likes_for_day(*,
                        db: AsyncSession = Depends(deps.get_db),
                        date_from: date,
                        date_to: date) -> LikeStatistic:
    amount_likes = await crud.like.count_likes(db=db,
                                               date_from=date_from,
                                               date_to=date_to)
    return amount_likes
