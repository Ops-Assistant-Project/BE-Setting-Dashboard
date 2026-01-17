from slack_bolt import App
from common.crypto import decrypt
from common.slack import SlackEnvKey


class BoltApp:
    """
    Slack Bolt App 싱글톤 래퍼
    """
    _apps: dict[str, App] = {}

    def __new__(cls, app_name: str) -> App:
        if app_name in cls._apps:
            return cls._apps[app_name]

        token_env = SlackEnvKey.BOT_TOKENS.get(app_name)
        secret_env = SlackEnvKey.SIGNING_SECRETS.get(app_name)

        if not token_env or not secret_env:
            raise ValueError(f"Slack env key not defined for app: {app_name}")

        app = App(
            token=decrypt(token_env),
            signing_secret=decrypt(secret_env),
        )

        cls._apps[app_name] = app
        return app
