import datetime
import random
import string


PASSWORD_CHANGE_INTERVAL_WEEKS = 2  # 주기(현재는 2주마다)

def generate_custom_password():
    part1 = ''.join(random.choices(string.ascii_uppercase, k=5))
    part2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    part3 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"{part1}-{part2}-{part3}"


def generate_password_for_week(start_date: datetime.date = None) -> str:
    """
    현재 날짜 기준으로 PASSWORD_CHANGE_INTERVAL_WEEKS마다
    같은 비밀번호를 반환. 주 단위로 계산.

    :param start_date: 시작 기준 날짜 (없으면 오늘 기준)
    :return: 패턴에 맞춘 비밀번호 문자열
    """
    start_date = start_date or datetime.date(2026, 1, 16)
    today = datetime.date.today()

    # 시작일부터 몇 주 지났는지 계산
    delta_weeks = ((today - start_date).days) // 7

    # 몇 번째 주기인지
    cycle_index = delta_weeks // PASSWORD_CHANGE_INTERVAL_WEEKS

    # 시드 고정 → 같은 주기에는 항상 같은 비밀번호
    random.seed(cycle_index)
    password = generate_custom_password()

    return password
