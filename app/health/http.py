from http import HTTPStatus
from traceback import format_exc

from fastapi_healthchecks.checks._base import Check, CheckResult

try:
    from aiohttp import BasicAuth, ClientResponseError, ClientSession, ClientTimeout, TCPConnector
except ImportError as exc:
    raise ImportError("Using this module requires the aiohttp library.") from exc


class HttpUACheck(Check):
    _url: str
    _username: str | None
    _password: str | None
    _verify_ssl: bool
    _timeout: float
    _name: str

    def __init__(
        self,
        url: str,
        user_agent: str,
        username: str | None = None,
        password: str | None = None,
        verify_ssl: bool = True,
        timeout: float = 60.0,
        name: str = "HTTP",
    ) -> None:
        self._url = url
        self._user_agent = user_agent
        self._username = username
        self._password = password
        self._verify_ssl = verify_ssl
        self._timeout = timeout
        self._name = name

    async def __call__(self) -> CheckResult:
        try:
            async with (
                ClientSession(
                    connector=TCPConnector(verify_ssl=self._verify_ssl, enable_cleanup_closed=True),
                    auth=BasicAuth(self._username, self._password or "") if self._username else None,
                    timeout=ClientTimeout(self._timeout),
                    headers={'User-Agent': self._user_agent if self._user_agent else 'HttpUACheck/1.0'},
                ) as session,
                session.get(self._url) as response,
            ):
                if response.status >= HTTPStatus.INTERNAL_SERVER_ERROR or (
                    self._username and response.status in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
                ):
                    response.raise_for_status()
                return CheckResult(name=self._name, passed=response.ok)
        except ClientResponseError as response_error:
            return CheckResult(name=self._name, passed=False, details=str(response_error))
        except Exception:
            details: str = format_exc()
            return CheckResult(name=self._name, passed=False, details=details)