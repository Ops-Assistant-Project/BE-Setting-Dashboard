from fastapi import APIRouter, Request
from slack_bolt.adapter.fastapi import SlackRequestHandler
from modules.slack import BoltApp
from common.slack import SlackBotName
from services.slack import open_pickup_modal, handle_pickup_submission, open_password_modal

router = APIRouter(prefix="/slack", tags=["Slack"])

slack_app = BoltApp(SlackBotName.SETTING_BOT)
handler = SlackRequestHandler(slack_app)

slack_app.action("open_pickup_modal")(open_pickup_modal)
slack_app.view("pickup_info_submit")(handle_pickup_submission)
slack_app.action("open_password_modal")(open_password_modal)

@router.post("/events")
async def slack_events(req: Request):
    return await handler.handle(req)
