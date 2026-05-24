from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db
from app.services.game import GetScore, getScorepg, getScoreRedis
from app.services.websocket_manager import manager
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

@router.websocket('/ws/leaderbord/{game_name}')
async def leaderbord_websocket(websocket: WebSocket, game_name: str):
    await manager.connect(game_name, websocket)

    try:
        leaderbord = await getScoreRedis(game_name)

        data = []
        for player, score in leaderbord:
            data.append({
                'player': player,
                'score': score
            })

        await websocket.send_json(
            {
                "type": "leaderboard_snapshot",
                'game_name': game_name,
                'data': data
            }
        )

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(game_name, websocket)
