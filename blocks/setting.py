def password_notice_message_block(user_name: str):
    return [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "🔐 Okta 비밀번호 자동 초기화 안내",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"{user_name}님, 안녕하세요 :wave: \n장비 세팅을 위해 *Okta 비밀번호가 자동으로 초기화될 예정* 이에요. 초기화가 완료되면 *세팅봇 DM으로 초기화된 비밀번호가 전송* 될 예정이니 확인해주세요."
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "⚠️ 장비 수령 전까지는 *비밀번호를 변경하지 말아주세요*"
				}
			]
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "문의 사항이 있으면 *IT Manager* 에게 연락해주세요"
				}
			]
		}
	]