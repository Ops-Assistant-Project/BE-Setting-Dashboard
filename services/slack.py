import json
from slack_sdk.errors import SlackApiError
from common.slack import Channels
from common.slack_blocks import get_mrkdwn_block
from blocks.setting import pickup_notice_modal_view, pickup_reserve_message_block

# @slack_app.action("open_pickup_modal")
def open_pickup_modal(ack, body, client):
    ack()
    try:
        client.views_open(
            trigger_id=body["trigger_id"],
            view=pickup_notice_modal_view(channel_id=body["channel"]["id"], message_ts=body["message"]["ts"])
        )
    except SlackApiError as e:
        print(f"Slack error: {e.response['error']}")

# @slack_app.view("pickup_info_submit")
def handle_pickup_submission(ack, body, client):
    ack()

    user_slack_id = body.get("user", {}).get("id", "")

    metadata = json.loads(body.get("view", {}).get("private_metadata", ""))
    channel_id = metadata.get("channel_id", "")
    message_ts = metadata.get("message_ts", "")

    values = body.get("view", {}).get("state", {}).get("values", {})
    pickup_date = values.get("pickup_date_block", {}).get("pickup_date", {}).get("selected_date", "")
    pickup_time = values.get("pickup_time_block", {}).get("pickup_time", {}).get("selected_time", "")
    pickup_disk = values.get("backup_disk_block", {}).get("backup_disk", {}).get("selected_option", {}).get("text", {}).get("text", "")
    try:
        # 관리자 채널에 확인용 메시지 전송
        client.chat_postMessage(
            channel=Channels.DEVICE_PICKUP_INFO,
            text="장비 수령 예약 완료",
            blocks=pickup_reserve_message_block(user_slack_id=user_slack_id, pickup_date=pickup_date, pickup_time=pickup_time, backup_disk=pickup_disk)
        )

        # 수령자 DM에서 수령 버튼을 확인용 메시지로 수정
        client.chat_update(
            channel=channel_id,
            ts=message_ts,
            text="장비 수령 예약 완료",
            blocks=[get_mrkdwn_block(f"수령 예약: *{pickup_date} {pickup_time}* / 백업디스크: *{pickup_disk}*")]
        )
    except SlackApiError as e:
        print(f"Slack error: {e.response['error']}")