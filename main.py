from fastapi import FastAPI, Request, BackgroundTasks 
from linebot import WebhookParser
from linebot.models import TextMessage
from aiolinebot import AioLineBotApi

line_api = AioLineBotApi(channel_access_token="CHANNEL_ACCESS_TOKEN")
parser = WebhookParser(channel_secret="CHANNEL_SECRET")

app = FastAPI()

@app.get("/health")
def health_check():
    return {'status': 'OK'}

@app.post("/callback")
async def callback(request: Request, background_tasks: BackgroundTasks):
    events = parser.parse(
        (await request.body()).decode("utf-8"),
        request.headers.get("X-Line-Signature", "")
    )
    
    background_tasks.add_task(handle_events, events=events)

    return 'OK'

async def handle_events(events):
    for event in events:
        try:
            await line_api.reply_message_async(
                event.reply_token,
                TextMessage(text=event.message.text))
        except Exception:
            print("Error!")
        