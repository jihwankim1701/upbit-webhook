# main.py
import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Slack Bot Token from environment variable
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_NAME = "#test"


def send_to_slack(message):
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=utf-8",
    }
    payload = {
        "channel": CHANNEL_NAME,
        "text": message,
    }
    response = requests.post("https://slack.com/api/chat.postMessage", json=payload, headers=headers)
    print(f"Slack response status: {response.status_code}")
    print(f"Slack response text: {response.text}")
    return response.status_code


class ChartPayload(BaseModel):
    image: str
    filename: str


@app.post("/analyze")
async def analyze_chart(payload: ChartPayload):
    try:
        img_data = base64.b64decode(payload.image)
        img = Image.open(BytesIO(img_data))

        # Placeholder for MACD/RSI analysis
        result = "✅ 분석 결과: MACD 골든크로스, RSI 67, 볼밴 상단 근접"

        # Send result to Slack
        slack_message = f"📈 *{payload.filename}* 분석 결과:\n{result}"
        send_to_slack(slack_message)

        return {"status": "ok", "filename": payload.filename, "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
