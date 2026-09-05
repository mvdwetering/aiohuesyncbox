import asyncio
import logging
import ssl
from types import TracebackType
from typing import Self

import aiohttp

from .controllers import (
    Behavior,
    Device,
    Execution,
    Hdmi,
    Hue,
    Ir,
    Presets,
    Registrations,
)
from .models import (
    BehaviorData,
    DeviceData,
    ExecutionData,
    HdmiData,
    HueData,
    IrData,
    RegistrationCredentials,
)
from .errors import raise_error, RequestError, Unauthorized
from .hsb_cacert import HSB_CACERT

MIN_API_LEVEL = 4

logger = logging.getLogger(__name__)


class HueSyncBox:
    """Control a Philips Hue Play HDMI Sync Box."""

    def __init__(
        self,
        host: str,
        id: str,
        access_token: str | None = None,
        port: int = 443,
        path: str = "/api",
    ) -> None:
        self._host = host
        self._id = id
        self._access_token = access_token
        self._port = port
        self._path = path

        self._clientsession: aiohttp.ClientSession | None = None

        # API endpoints
        self.behavior: Behavior | None
        self.device: Device
        self.execution: Execution
        self.hdmi: Hdmi | None
        self.hue: Hue
        self.ir: Ir | None
        self.registrations = Registrations(self.request)
        self.presets = Presets(self.request)

        self._last_response: dict | None = None  # For debugging purposes

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def _get_clientsession(self) -> aiohttp.ClientSession:
        """
        Get a clientsession that is tuned for communication with the Hue Syncbox
        """

        def _build_ssl_context() -> ssl.SSLContext:
            context = ssl.create_default_context(cadata=HSB_CACERT)
            context.hostname_checks_common_name = True
            return context

        # Creating an SSL context has some blocking IO so need to run it in the executor
        loop = asyncio.get_running_loop()
        context = await loop.run_in_executor(None, _build_ssl_context)

        connector = aiohttp.TCPConnector(
            enable_cleanup_closed=True,  # Home Assistant sets it so lets do it also
            ssl=context,
            limit_per_host=1,  # Syncbox can handle a limited amount of connections, only take what we need
        )

        return aiohttp.ClientSession(
            connector=connector, timeout=aiohttp.ClientTimeout(total=10)
        )

    @property
    def access_token(self) -> str | None:
        return self._access_token

    @property
    def last_response(self) -> dict | None:
        return self._last_response

    async def is_registered(self) -> bool:
        try:
            await self.request("get", "/registrations")
            return True
        except Unauthorized:
            return False

    async def register(
        self,
        application_name: str,
        instance_name: str,
        use_registered_token: bool = True,
    ) -> RegistrationCredentials | None:
        """
        Register with the huesyncbox

        application_name : Userfriendly name of your application
        instance_name : The specific instance of your application, e.g. a specific device the application is running on
        use_registered_token: When true use the token (if obtained) for subsequent requests

        returns registration info on success
        """
        info = await self.registrations.create(application_name, instance_name)
        if info and use_registered_token:
            self._access_token = info.access_token
        return info

    async def unregister(self, registration_id: str) -> None:
        """Unregister application from the huesyncbox, you can only unregister the id associated with the token in use."""
        await self.registrations.delete(registration_id)

    async def initialize(self) -> None:
        await self.refresh()
        if self.device.api_level < MIN_API_LEVEL:
            logger.error(
                "This library requires at least API version %s. Please update the Philips Hue Play HDMI Sync Box.",
                MIN_API_LEVEL,
            )

    async def close(self) -> None:
        if self._clientsession is not None:
            await self._clientsession.close()

    async def refresh(self) -> None:
        response = await self.request("get", "")
        self._last_response = response

        if response:
            self.behavior = (
                Behavior(BehaviorData.from_dict(response["behavior"]), self.request)
                if "behavior" in response
                else None
            )
            self.device = Device(DeviceData.from_dict(response["device"]), self.request)
            self.execution = Execution(
                ExecutionData.from_dict(response["execution"]), self.request
            )
            self.hue = Hue(HueData.from_dict(response["hue"]), self.request)
            self.hdmi = (
                Hdmi(HdmiData.from_dict(response["hdmi"]), self.request)
                if "hdmi" in response
                else None
            )
            self.ir = (
                Ir(IrData.from_dict(response["ir"]), self.request)
                if "ir" in response
                else None
            )
            self.registrations.load(response["registrations"])
            self.presets.load(response["presets"])

    async def request(
        self, method: str, path: str, data: dict | None = None, auth: bool = True
    ) -> dict | None:
        """Make a request to the API."""

        if self._clientsession is None:
            self._clientsession = await self._get_clientsession()
            assert self._clientsession is not None

        if self._clientsession.closed:
            # Avoid runtime errors when connection is closed.
            # This solves an issue when Updates were scheduled and HA was shutdown
            return None

        url = f"https://{self._host}:{self._port}{self._path}/v1{path}"

        try:
            logger.debug("%s, %s, %s", method, url, data)

            headers = {"Content-Type": "application/json"}
            if auth and self._access_token:
                headers["Authorization"] = f"Bearer {self._access_token}"

            async with self._clientsession.request(
                method, url, json=data, headers=headers, server_hostname=self._id
            ) as resp:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug("%s, %s", resp.status, await resp.text("utf-8"))

                data = None
                if resp.content_type == "application/json":
                    data = await resp.json()
                    if resp.status != 200:
                        if isinstance(data, dict):
                            _raise_on_error(data)
                        else:
                            logger.error("Received unexpected data format: %s", data)
                return data
        except aiohttp.ClientError as err:
            logger.debug(err, exc_info=True)
            raise RequestError(f"Error requesting data from {self._host}") from err
        except asyncio.TimeoutError as err:
            logger.debug(err, exc_info=True)
            raise RequestError(f"Timeout requesting data from {self._host}") from err


def _raise_on_error(data: dict) -> None:
    """Check response for error message."""
    raise_error(data["code"], data["message"])
