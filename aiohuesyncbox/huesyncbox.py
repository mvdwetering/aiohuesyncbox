import asyncio
import ipaddress
import logging
import ssl
import socket
import pathlib

import aiohttp

from .device import Device
from .execution import Execution
from .hue import Hue
from .hdmi import Hdmi
from .errors import raise_error, RequestError, Unauthorized
from .hsb_cacert import HSB_CACERT

MIN_API_LEVEL = 4

logger = logging.getLogger(__name__)

class CommonNameInserterResolver(aiohttp.DefaultResolver):

    def __init__(self, common_name, loop=None, *args, **kwargs):
        super().__init__(loop=loop, *args, **kwargs)
        self._common_name = common_name

    async def resolve(self, host, port=0, family=socket.AF_INET):
        hosts = []
        if host.startswith('_'):
            # Host was an IP address that was mangled to force a DNS lookup (_ are not valid)
            # and with that forced lookup end up in this call.
            # This is needed as IP addresses don't need lookup,
            # but I need to set the hostname to the common_name for certificate validation
            # and this seems to be the only place I could hook into

            # Generate a suitable entry in the hosts list
            hosts.append({
                'host': host[1:],
                'port': port,
                'family': family,
                'proto': 6, # TCP I think
                'flags': socket.AI_NUMERICHOST,
            })
        else:
            hosts.append(await super().resolve(host, port=port, family=family))

        for host in hosts:
            host['hostname'] = self._common_name

        return hosts


class HueSyncBox:
    """Control a Philips Hue Play HDMI Sync Box."""

    def __init__(self, host, id, access_token=None, port=443, path='/api'):
        self._host = host
        self._id = id
        self._access_token = access_token
        self._port = port
        self._path = path

        self._clientsession = self._get_clientsession()

        # API endpoints
        self.device = None
        self.execution = None
        self.hue = None
        self.hdmi = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    def _get_clientsession(self):
        """
        Get a clientsession that is tuned for communication with the Hue Syncbox
        """
        context = ssl.create_default_context(cadata=HSB_CACERT)
        context.hostname_checks_common_name = True

        connector = aiohttp.TCPConnector(
            enable_cleanup_closed=True, # Home Assistant sets it so lets do it also
            ssl=context,
            resolver=CommonNameInserterResolver(self._id) # Use custom resolver to get certificate validation on common_name working
        )

        return aiohttp.ClientSession(connector=connector)

    @property
    def access_token(self):
        return self._access_token

    async def is_registered(self):
        try:
            await self.request('get', '/registrations')
            return True
        except Unauthorized:
            return False
        return False

    async def register(self, application_name, instance_name, use_registered_token=True):
        """
        Register with the huesyncbox

        application_name : Userfriendly name of your application
        instance_name : The specific instance of your application, e.g. a specific device the application is running on
        use_registered_token: When true use the token (if obtained) for subsequent requests
        """
        result = await self.request('post', '/registrations', {
            "appName": application_name,
            "instanceName": instance_name
        }, auth=False) # Make sure to _not_ use a possibly invalid token as it will be rejected

        if result:
            info = {
                'registration_id': result['registrationId'],
                'access_token': result['accessToken']
            }

            if use_registered_token:
                self._access_token = info['access_token']

        return info

    async def unregister(self, registration_id):
        """Unregister application from the huesyncbox, you can only unregister the id associated with the token in use."""
        await self.request('delete', f'/registrations/{registration_id}')

    async def initialize(self):
        await self.update()
        if self.device.api_level < MIN_API_LEVEL:
            logger.error("This library requires at least API version %s. Please update the Philips Hue Play HDMI Sync Box.", MIN_API_LEVEL)

    async def close(self):
        await self._clientsession.close()

    async def update(self):
        result = await self.request('get', '')
        self.device = Device(result['device'], self.request)
        self.execution = Execution(result['execution'], self.request)
        self.hue = Hue(result['hue'], self.request)
        self.hdmi = Hdmi(result['hdmi'], self.request)

    def _mangled_host(self):
        """
        Returns the hostname or a modified hostname in case the host is an IP address
        to make sure DNS lookups are required as that allows to use the common_name
        instead of servername for certificate validation.
        """
        try:
            ipaddress.ip_address(self._host)
            return f"_{self._host}"
        except ValueError:
            pass
        return self._host

    async def request(self, method, path, json=None, auth=True):
        """Make a request to the API."""

        url = f'https://{self._mangled_host()}:{self._port}{self._path}/v1{path}'

        try:
            headers = {'Content-Type': 'application/json'}
            if auth and self._access_token:
                headers['Authorization'] = f'Bearer {self._access_token}'
            logger.debug(f'{method}, {url}, {json}, {headers}')
            async with self._clientsession.request(method, url, json=json, headers=headers) as res:
                data = None
                if res.content_type == 'application/json':
                    data = await res.json()
                    logger.debug(f'data: {data}')
                    if res.status != 200:
                        _raise_on_error(data)
                return data
        except aiohttp.client_exceptions.ClientError as err:
            raise RequestError(
                'Error requesting data from {}: {}'.format(self._host, err)
            ) from None


def _raise_on_error(data):
    """Check response for error message."""
    raise_error(data['code'], data["message"])
