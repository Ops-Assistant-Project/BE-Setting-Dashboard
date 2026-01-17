from typing import Any, Optional


class CommonResponse:
    def __init__(
        self,
        ok: bool,
        data: Optional[Any] = None,
        error: Optional[str] = None,
        status_code: Optional[int] = None
    ):
        self.ok = ok
        self.data = data
        self.error = error
        self.status_code = status_code

    @classmethod
    def success(cls, data: Any = None, status_code: int = 200):
        return cls(
            ok=True,
            data=data,
            status_code=status_code
        )

    @classmethod
    def failure(cls, error: str, status_code: int):
        return cls(
            ok=False,
            error=error,
            status_code=status_code
        )
