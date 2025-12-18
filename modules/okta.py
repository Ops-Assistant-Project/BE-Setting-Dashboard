import os
import requests
from dotenv import load_dotenv
from core.common_response import CommonResponse


class OktaClient():
    def __init__(self):
        load_dotenv()
        self.okta_domain = os.getenv("OKTA_DOMAIN")
        self.base_url = f"https://{self.okta_domain}/api/v1"
        self.headers = {
            "Authorization": f"Bearer {os.getenv('OKTA_AUTH_TOKEN')}",
        }

    def okta_call_api(self, endpoint: str = None, params: dict = None, method: str = 'GET') -> CommonResponse:
        if method:
            method = method.upper()

        try:
            response = requests.request(
                method=method,
                url=f"{self.base_url}{endpoint}",
                params=params,
                headers=self.headers,
            )
        except requests.RequestException as e:
            return CommonResponse.failure(error=str(e), status_code=500)

        if not response.ok:
            return CommonResponse.failure(
                error=response.text,
                status_code=response.status_code
            )

        if response.status_code == 204:
            return CommonResponse.success(data=None, status_code=204)

        return CommonResponse.success(
            data=response.json(),
            status_code=response.status_code
        )

    def add_user_to_group(self, group_id: str, user_id: str):
        """
        그룹에 사용자 추가
        :param group_id: Okta group id
        :param user_id: Okta user id
        :return: 204 No Content
        """
        return self.okta_call_api(endpoint=f"/groups/{group_id}/users/{user_id}", method="PUT")

    def activate_user(self, user_id: str, send_email: bool = False):
        """
        사용자 계정 활성화
        :param user_id: Okta user id
        :param send_email: 사용자에게 활성화 이메일 보냄(default: False)
        :return: 200 { activationToken: str, activationUrl: str }
        """
        return self.okta_call_api(endpoint=f"/users/{user_id}/lifecycle/activate?sendEmail={send_email}", method="POST")

