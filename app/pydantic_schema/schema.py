from pydantic import BaseModel

class InputScore(BaseModel):
    game_name: str
    player: str
    score: int

class InputResponse(BaseModel):
    game_name: str
    player: str
    score: int