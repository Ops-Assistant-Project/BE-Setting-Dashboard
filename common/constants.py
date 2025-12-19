class OktaGroups:
    """
    Okta 그룹 ID 상수 정의

    ⚠️ 주의
    - 실제 운영 환경에서는 아래 값들을
      Okta Admin Console에서 발급된 Group ID로 교체해야 함
    - 현재는 개발 / 포트폴리오용 임시 값
    """

    # 모든 세팅 대상 사용자가 기본적으로 포함되는 그룹
    ALL_SETTING = "your_setting_group_id"

    # Windows PC 세팅 대상 사용자 그룹
    WIN_SETTING = "your_win_setting_group_id"
    O365_INTUNE = "your_o365_setting_group_id"
