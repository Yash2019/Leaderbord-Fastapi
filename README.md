# Realtime Leaderboard API

A FastAPI leaderboard system backed by PostgreSQL for persistent score history, Redis sorted sets for fast leaderboard reads, and WebSockets for realtime leaderboard updates.

## Features

- Submit player scores through a REST API
- Store submitted scores in PostgreSQL
- Maintain fast per-game leaderboards in Redis
- Fetch leaderboard data from PostgreSQL or Redis
- Subscribe to realtime leaderboard updates over WebSockets
- Send an initial leaderboard snapshot when a client connects
- Broadcast score updates only to clients watching the same game

## Tech Stack

- Python
- FastAPI
- SQLAlchemy async ORM
- PostgreSQL
- Redis
- WebSockets
- Pydantic
- Uvicorn

## Project Structure

```text
app/
  crud/
    routes.py              # REST and WebSocket routes
  database/
    db.py                  # Async SQLAlchemy engine/session setup
    redis_client.py        # Async Redis client
  models/
    pg_leaderbord.py       # Leaderboard database model
  pydantic_schema/
    schema.py              # Request/response schemas
  services/
    game.py                # Score write/read logic
    websocket_manager.py   # WebSocket connection manager
  configure.py             # Environment configuration
  main.py                  # FastAPI app entrypoint
requirements.txt
```

## How It Works

When a score is submitted:

```text
POST /LeaderBord
      |
      v
PostgreSQL stores the score history
      |
      v
Redis updates the sorted leaderboard
      |
      v
WebSocket clients watching that game receive an update
```

Redis stores leaderboards using keys like:

```text
leaderbord:{game_name}
```

For example:

```text
leaderbord:pubg
leaderbord:chess
leaderbord:valorant
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create an environment file at:

```text
app/.env
```

Example:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/leaderboard_db
REDIS_URL=redis://localhost:6379
```

Make sure PostgreSQL and Redis are running before starting the API.

## Run The App

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Swagger docs:

```text
http://localhost:8000/docs
```

Note: WebSocket routes do not appear in Swagger/OpenAPI docs. This is expected.

## REST Endpoints

### Submit Score

```http
POST /LeaderBord
```

Request body:

```json
{
  "game_name": "pubg",
  "player": "roger",
  "score": 1200
}
```

Example response:

```json
{
  "game_name": "pubg",
  "player": "roger",
  "score": 1200
}
```

This endpoint:

- saves the score in PostgreSQL
- updates the Redis sorted set
- broadcasts a realtime update to WebSocket clients watching the same game

### Get Scores From PostgreSQL

```http
GET /Scorepg?game_name=pubg
```

Returns score records stored in PostgreSQL for the given game.

### Get Leaderboard From Redis

```http
GET /ScoreRedis?game_name=pubg
```

Returns the Redis sorted-set leaderboard for the given game.

## WebSocket Endpoint

```text
ws://localhost:8000/ws/leaderbord/{game_name}
```

Example:

```text
ws://localhost:8000/ws/leaderbord/pubg
```

When a client connects, the server sends an initial leaderboard snapshot:

```json
{
  "type": "leaderboard_snapshot",
  "game_name": "pubg",
  "data": [
    {
      "player": "roger",
      "score": 1200
    }
  ]
}
```

When a new score is submitted for the same game, connected clients receive:

```json
{
  "type": "leaderboard_updated",
  "game_name": "pubg",
  "player": "roger",
  "score": 1200
}
```

## Testing With Postman

### Test The WebSocket

Create a new WebSocket request in Postman and connect to:

```text
ws://localhost:8000/ws/leaderbord/pubg
```

After connecting, you should receive the current leaderboard snapshot.

### Trigger A Realtime Update

In another Postman tab, send:

```http
POST http://localhost:8000/LeaderBord
```

Body:

```json
{
  "game_name": "pubg",
  "player": "roger",
  "score": 1200
}
```

The WebSocket tab connected to `pubg` should receive a `leaderboard_updated` event.

## Important Notes

- WebSocket endpoints do not show in Swagger.
- The REST endpoint uses `/LeaderBord` because that is the current route name in the code.
- The WebSocket endpoint uses `/ws/leaderbord/{game_name}` because that is the current route name in the code.
- Redis sorted sets keep one score per player per game. Submitting another score for the same player updates that player's Redis score.
- PostgreSQL stores each submitted score as a separate record.
- The current WebSocket manager is in-memory. It works for a single FastAPI process. For multiple workers or multiple servers, use Redis Pub/Sub to broadcast events across processes.

## Example Flow

1. Start PostgreSQL.
2. Start Redis.
3. Run the FastAPI app.
4. Open a WebSocket connection to `ws://localhost:8000/ws/leaderbord/pubg`.
5. Submit a score to `POST /LeaderBord`.
6. Watch the WebSocket client receive the realtime update.
