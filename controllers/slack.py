from fastapi import APIRouter, Request
from slack_bolt.adapter.fastapi import SlackRequestHandler
from modules.slack import BoltApp
from common.slack import SlackBotName

router = APIRouter(prefix="/slack", tags=["Slack"])

slack_app = BoltApp(SlackBotName.SETTING_BOT)
handler = SlackRequestHandler(slack_app)

from services.slack import register_test_command
register_test_command(slack_app)    # 테스트용 슬래시 커맨드

@router.post("/events")
async def slack_events(req: Request):
    return await handler.handle(req)
