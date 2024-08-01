import asyncio
import ipaddress
import logging
import ssl
import socket
from typing import Dict, Optional

import aiohttp

from .behavior import Behavior
from .device import Device
from .execution import Execution
from .hue import Hue
from .hdmi import Hdmi
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
        access_token: Optional[str] = None,
        port: int = 443,
        path: str = "/api",
    ) -> None:
        self._host = host
        self._id = id
        self._access_token = access_token
        self._port = port
        self._path = path

        self._clientsession = self._get_clientsession()

        # API endpoints
        self.behavior: Behavior
        self.device: Device
        self.execution: Execution
        self.hdmi: Hdmi
        self.hue: Hue

        self._last_response = None  # For debugging purposes

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    def _get_clientsession(self) -> aiohttp.ClientSession:
        """
        Get a clientsession that is tuned for communication with the Hue Syncbox
        """
        context = ssl.create_default_context(cadata=HSB_CACERT)
        context.hostname_checks_common_name = True

        connector = aiohttp.TCPConnector(
            enable_cleanup_closed=True,  # Home Assistant sets it so lets do it also
            ssl=context,
            limit_per_host=1,  # Syncbox can handle a limited amount of connections, only take what we need
        )

        return aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=10))

    @property
    def access_token(self) -> str | None:
        return self._access_token

    @property
    def last_response(self) -> Dict | None:
        return self._last_response

    async def is_registered(self):
        try:
            await self.request("get", "/registrations")
            return True
        except Unauthorized:
            return False
        return False

    async def register(
        self,
        application_name: str,
        instance_name: str,
        use_registered_token: bool = True,
    ):
        """
        Register with the huesyncbox

        application_name : Userfriendly name of your application
        instance_name : The specific instance of your application, e.g. a specific device the application is running on
        use_registered_token: When true use the token (if obtained) for subsequent requests

        returns registration info on success
        """
        response = await self.request(
            "post",
            "/registrations",
            {"appName": application_name, "instanceName": instance_name},
            auth=False,
        )  # Make sure to _not_ use a possibly invalid token as it will be rejected

        info = None
        if response:
            info = {
                "registration_id": response["registrationId"],
                "access_token": response["accessToken"],
            }

            if use_registered_token:
                self._access_token = info["access_token"]

        return info

    async def unregister(self, registration_id: str):
        """Unregister application from the huesyncbox, you can only unregister the id associated with the token in use."""
        await self.request("delete", f"/registrations/{registration_id}")

    async def initialize(self):
        await self.update()
        if self.device.api_level < MIN_API_LEVEL:
            logger.error(
                "This library requires at least API version %s. Please update the Philips Hue Play HDMI Sync Box.",
                MIN_API_LEVEL,
            )

    async def close(self):
        await self._clientsession.close()

    async def update(self):
        response = await self.request("get", "")
        self._last_response = response

        if response:
            self.behavior = Behavior(response["behavior"], self.request)
            self.device = Device(response["device"], self.request)
            self.execution = Execution(response["execution"], self.request)
            self.hue = Hue(response["hue"], self.request)
            self.hdmi = Hdmi(response["hdmi"], self.request)

    async def request(
        self, method: str, path: str, data: Optional[Dict] = None, auth: bool = True
    ):
        """Make a request to the API."""

        if self._clientsession.closed:
            # Avoid runtime errors when connection is closed.
            # This solves an issue when Updates were scheduled and HA was shutdown
            return None

        url = f"https://{self._host}:{self._port}{self._path}/v1{path}"

        try:
            logger.debug("%s, %s, %s" % (method, url, data))

            headers = {"Content-Type": "application/json"}
            if auth and self._access_token:
                headers["Authorization"] = f"Bearer {self._access_token}"

            async with self._clientsession.request(
                method, url, json=data, headers=headers, server_hostname=self._id
            ) as resp:
                logger.debug("%s, %s" % (resp.status, await resp.text("utf-8")))

                data = None
                if resp.content_type == "application/json":
                    data = await resp.json()
                    if resp.status != 200:
                        if isinstance(data, dict):
                            _raise_on_error(data)
                        else:
                            logger.error(
                                "Received unexpected data format: %s" % str(data)
                            )
                return data
        except aiohttp.ClientError as err:
            logger.debug(err, exc_info=True)
            raise RequestError(
                f"Error requesting data from {self._host}"
            ) from err
        except asyncio.TimeoutError as err:
            logger.debug(err, exc_info=True)
            raise RequestError(
                f"Timeout requesting data from {self._host}"
            ) from err


def _raise_on_error(data: Dict):
    """Check response for error message."""
    raise_error(data["code"], data["message"])
