from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db
from app.services.game import GetScore, getScorepg, getScoreRedis
from app.pydantic_schema.schema import InputResponse, InputScore

router = APIRouter()

@router.post('/LeaderBord', response_model=InputResponse)
async def LeaderBord_endpoint(data: InputScore, db: AsyncSession = Depends(get_db)):
    return await GetScore(data, db)

@router.get('/Scorepg')
async def get_scorepg_endpoint(game_name: str, db: AsyncSession = Depends(get_db)):
    return await getScorepg(game_name, db)

@router.get('/ScoreRedis')
async def get_scoreRedis_endpoint(game_name: str):
    return await getScoreRedis(game_name)
