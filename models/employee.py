from mongoengine import (
    Document,
    StringField,
    EmailField,
    DateTimeField
)


class Employee(Document):
    meta = {"collection": "employees"}

    # 기본 정보
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)

    okta_user_id = StringField()
    ldap_id = StringField()
    slack_id = StringField()

    # 재직 상태
    status = StringField(
        choices=["ACTIVE", "INACTIVE", "SUSPENDED"],
        default="ACTIVE"
    )

    # 인사 정보
    joined_at = DateTimeField() # 입사일
    resigned_at = DateTimeField()   # 퇴사일 (재직 중이면 None)
