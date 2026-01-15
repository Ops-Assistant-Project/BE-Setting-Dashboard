import json
from datetime import datetime
from zoneinfo import ZoneInfo

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

def pickup_notice_message_block():
    return [
        {
            "type": "header",
            "text": {
              "type": "plain_text",
              "text": "📦 장비 수령 안내",
              "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
              "type": "mrkdwn",
              "text": "PC 세팅이 완료되어 장비 수령이 가능합니다 🙌\n아래 버튼을 눌러 *수령 희망 시간과 백업 디스크 필요 여부* 를 선택해주세요."
            }
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": ":warning: 장비는 4층 IT팀에서 수령 가능합니다"
                }
            ]
        }
    ]

def pickup_notice_button_block():
    return [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "🕒 수령 날짜 및 시간 선택",
                        "emoji": True
                    },
                    "style": "primary",
                    "action_id": "open_pickup_modal"
                }
            ]
        }
    ]

def pickup_notice_modal_view(channel_id: str, message_ts: str):
    kst_now = datetime.now(ZoneInfo("Asia/Seoul")).date()

    return {
        "title": {
            "type": "plain_text",
            "text": ":computer: 장비 수령",
            "emoji": True
        },
        "private_metadata": json.dumps({
            "channel_id": channel_id,
            "message_ts": message_ts,
        }),
        "submit": {
            "type": "plain_text",
            "text": "제출"
        },
        "type": "modal",
        "callback_id": "pickup_info_submit",
        "close": {
            "type": "plain_text",
            "text": "취소"
        },
        "blocks": [
            {
                "type": "input",
                "block_id": "pickup_date_block",
                "label": {
                    "type": "plain_text",
                    "text": "수령 희망 날짜"
                },
                "element": {
                    "type": "datepicker",
                    "initial_date": f"{kst_now}",
                    "action_id": "pickup_date",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "날짜를 선택해주세요"
                    }
                }
            },
            {
                "type": "input",
                "block_id": "pickup_time_block",
                "label": {
                    "type": "plain_text",
                    "text": "수령 희망 시간"
                },
                "element": {
                    "type": "timepicker",
                    "initial_time": "10:00",
                    "action_id": "pickup_time",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "시간을 선택해주세요"
                    }
                }
            },
            {
                "type": "input",
                "block_id": "backup_disk_block",
                "label": {
                    "type": "plain_text",
                    "text": "백업 디스크 필요 여부"
                },
                "element": {
                    "type": "static_select",
                    "action_id": "backup_disk",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "선택해주세요"
                    },
                    "initial_option": {
                        "text": {
                            "type": "plain_text",
                            "text": "필요없어요"
                        },
                        "value": "no"
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "필요없어요"
                            },
                            "value": "no"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "필요해요"
                            },
                            "value": "yes"
                        }
                    ]
                }
            }
        ]
    }

def pickup_reserve_message_block(user_slack_id: str, pickup_date: str, pickup_time: str, backup_disk: str):
    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":alarm_clock: 장비 수령 정보 제출됨",
                "emoji": True
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*사용자:*\n<@{user_slack_id}>"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*날짜:*\n{pickup_date}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*시간:*\n{pickup_time}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*백업 디스크 필요 여부:*\n{backup_disk}"
                }
            ]
        }
    ]