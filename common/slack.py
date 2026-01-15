class SlackBotToken:
    """
    Slack Bot Token 상수 정의

    ⚠️ 주의
    - 실제 운영 환경에서는 아래 값들을
      Slack App에서 발급된 Bot User OAuth Token으로 교체해야 함
    - 현재는 개발 / 포트폴리오용 임시 값
    - 토큰 값은 반드시 환경변수 또는 Secret Manager로 관리할 것
    """

    # Setting 서비스에서 사용하는 Slack 봇 토큰
    SETTING_BOT = "your_setting_bot_token"