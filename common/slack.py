class SlackBotName:
    SETTING_BOT = "SETTING_BOT"

class SlackEnvKey:
    """
    Slack Bot 환경변수 키 정의

    ⚠️ 주의
    - 현재는 개발 / 포트폴리오용 값
    - 토큰 값은 반드시 crypto 암호화 후 저장할 것
    """

    BOT_TOKENS = {
        SlackBotName.SETTING_BOT: "gAAAAABpaJN7uCjMENGwZKzZwZaIlAGdSfS1f_vS_TuwTlXjVRFgzvfaiDo3iXO70q5NIVaodnz9C69JhH9J0faDhDOeM9A65GEKLV_m_zcXEAnAZOIBvW9VwsyujwPTVQ6w914oiUxZC_7udRGUMsPeSRDtaU2yvQ==",
    }

    SIGNING_SECRETS = {
        SlackBotName.SETTING_BOT: "gAAAAABpaJQP9_x_drHai_z2NKyqkURbv7YtxSNDJD59JB0bkKiUFYiCv_cz_szFnvX-m_rd4Crvp3jYFoam6-DJ-F_cqrXUqDqkt_Wb169txFqTJoflB1Rmos8KpLk7VuCd8dYh6Y96",
    }

class Channels:
    DEVICE_PICKUP_INFO = "C0A8FMYSB0F"  # 수령 예약 확인용 관리자 채널