from slack_bolt import App
from slack_bolt.context.say import Say

def register_test_command(app: App):

    @app.command("/test")
    def handle_test_command(ack, body, say: Say):
        # Slack에 "응답 받았음" 알려줘야 타임아웃 안 남
        ack()

        user_id = body["user_id"]
        channel_id = body["channel_id"]

        say(
            text=f"👋 <@{user_id}> /test 커맨드 정상 작동 중!",
            channel=channel_id
        )
