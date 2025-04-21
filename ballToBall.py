from fastapi import FastAPI, Request, HTTPException, Query
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, auth, firestore
import os, json

firebase_key_json = os.getenv("FIREBASE_KEY")
cred = credentials.Certificate(json.loads(firebase_key_json))
firebase_admin.initialize_app(cred)

db = firestore.client()
app = FastAPI()

@app.get("/balls")
def get_all_balls(
    batterName: str = Query(None),
    ballLine: str = Query(None),
    footwork: str = Query(None),
    ballLength: str = Query(None)
):
    docs = db.collection("ball_ID").stream()

    all_balls = []
    player_data = {}
    total_middled = 0
    total_not_middled = 0

    # Normalize filters
    batterName = batterName.strip().lower() if batterName else None
    ballLine = ballLine.strip().lower() if ballLine else None
    footwork = footwork.strip().lower() if footwork else None
    ballLength = ballLength.strip().lower() if ballLength else None

    for doc in docs:
        ball = doc.to_dict()

        # Extract and normalize fields
        ball_batter = ball.get("batterName", "").strip().lower()
        ball_line = ball.get("ballLine", "").strip().lower()
        footwork_val = ball.get("footwork", "").strip().lower()
        ball_len = ball.get("ballLength", "").strip().lower()
        bat_len = ball.get("batLength", "").strip().lower()
        bat_line = ball.get("batLine", "").strip().lower()

        # Apply filters
        if batterName and batterName != ball_batter:
            continue
        if ballLine and ballLine != ball_line:
            continue
        if footwork and footwork != footwork_val:
            continue
        if ballLength and ballLength != ball_len:
            continue

        # Store ball
        all_balls.append(ball)

        if ball_batter not in player_data:
            player_data[ball_batter] = {
                "total": 0,
                "middled": 0,
                "notMiddled": 0,
                "timeline": []
            }

        is_middled = bat_len == "middle" and bat_line == "middle"

        player_data[ball_batter]["total"] += 1
        player_data[ball_batter]["timeline"].append(1 if is_middled else 0)

        if is_middled:
            player_data[ball_batter]["middled"] += 1
            total_middled += 1
        else:
            player_data[ball_batter]["notMiddled"] += 1
            total_not_middled += 1

    return {
        "balls": all_balls,
        "playerSpecificData": player_data,
        "totalMiddled": total_middled,
        "totalNotMiddled": total_not_middled
    }
