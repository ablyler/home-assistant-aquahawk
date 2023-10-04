import logging
from typing import Any, Dict, Optional

from homeassistant import core, config_entries
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import voluptuous as vol

from aquahawk_client import AquaHawkClient, AuthenticationError

from .const import (
    DOMAIN,
    CONF_ACCOUNT_NUMBER,
    CONF_HOSTNAME,
    CONF_PASSWORD,
    CONF_USERNAME,
)

_LOGGER = logging.getLogger(__name__)

AUTH_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ACCOUNT_NUMBER): cv.string,
        vol.Required(CONF_HOSTNAME): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


async def validate_auth(
    account_number: str,
    hostname: str,
    username: str,
    password: str,
    hass: core.HomeAssistant) -> None:
    """Validates a GitHub access token.

    Raises a ValueError if the auth token is invalid.
    """
    session = async_get_clientsession(hass)
    aquahawk = AquaHawkClient(account_number, hostname, username, password, session)
    try:
        aquahawk.authenticate()
    except AuthenticationError:
        raise ValueError

class AquahawkConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """AquaHawk Custom config flow."""

    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            try:
                await validate_auth(
                    user_input[CONF_ACCOUNT_NUMBER],
                    user_input[CONF_HOSTNAME],
                    user_input[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                    self.hass
                )
            except ValueError:
                errors["base"] = "auth"
            if not errors:
                # Input is valid, set data.
                self.data = user_input
            # Return the form of the next step.
            return self.async_create_entry(title="AquaHawk", data=self.data)

        return self.async_show_form(
            step_id="user", data_schema=AUTH_SCHEMA, errors=errors
        )

