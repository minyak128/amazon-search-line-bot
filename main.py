from fastapi import FastAPI, Request, BackgroundTasks 
from linebot import WebhookParser
from linebot.models import TextMessage
from aiolinebot import AioLineBotApi

line_api = AioLineBotApi(channel_access_token="9k2mygZ1fZU7pNWurCyNzLgABSxTPmbFo6CnYKn8Q5HYGkEh1E2bEMC3sGOC+uTK1q6lXelpiSv0gErHV/z2EHH3ssLzGG6hCm3tvW1E2A55Khpda0fmnTiwLuIqWR+9UopOnGOVvMJy3cZ+nwMNgwdB04t89/1O/w1cDnyilFU=")
parser = WebhookParser(channel_secret="735773daaef5822c0f2ebf1a28594258")

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
        