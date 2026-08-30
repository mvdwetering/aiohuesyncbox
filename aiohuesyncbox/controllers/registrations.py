from typing import Dict, Optional

from ..models import Registration, RequestFunc
from .base import CollectionResource


class Registrations(CollectionResource[Registration]):
    """Control the Registrations resource of the huesyncbox."""

    def __init__(self, request: RequestFunc) -> None:
        super().__init__("/registrations", Registration, request)

    async def create(
        self, application_name: str, instance_name: str
    ) -> Optional[Dict[str, str]]:
        """Register a new application/instance.

        Make sure to _not_ use a possibly invalid token for this request, as
        it will be rejected; the caller is responsible for passing auth=False
        to the underlying request function used here.
        """
        response = await self._request(
            "post",
            self._path,
            {"appName": application_name, "instanceName": instance_name},
            auth=False,
        )
        if not response:
            return None
        return {
            "registration_id": response["registrationId"],
            "access_token": response["accessToken"],
        }
