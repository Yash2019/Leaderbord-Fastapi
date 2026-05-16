from sqlalchemy.ext.asyncio import AsyncSession
from app.models.pg_leaderbord import LeaderBord
from app.pydantic_schema.schema import InputScore
from app.database.redis_client import redis
from sqlalchemy import select

async def GetScore(data: InputScore, db: AsyncSession):
    scores = LeaderBord(
        game_name = data.game_name,
        player=data.player,
        score = data.score
    )

    db.add(scores)
    await db.commit()

    await redis.zadd(f'leaderbord:{data.game_name}', {data.player: data.score})
    await db.refresh(scores)

    return scores

async def getScorepg(game_name: str, db: AsyncSession):
    stmt = select(LeaderBord).where(LeaderBord.game_name == game_name)
    result = await db.execute(stmt)
    lead = result.scalars().all()

    return lead

async def getScoreRedis(game_name: str):
    return await redis.zrevrange(f'leaderbord:{game_name}', 0, -1, withscores=True)



