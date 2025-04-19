# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 14:12:21 2025

@author: Rushi
"""

from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, auth, firestore

import os, json
firebase_key_json = os.getenv("FIREBASE_KEY")
cred = credentials.Certificate(json.loads(firebase_key_json))

firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

db = firestore.client()


@app.get("/balls")
def get_all_balls():
    docs = db.collection("ball_ID").stream()

    all_balls = []
    for doc in docs:
        ball_data = doc.to_dict()
        all_balls.append(ball_data)

    return {"balls": all_balls}
