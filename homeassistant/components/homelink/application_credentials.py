"""application_credentials platform the homelink integration."""

from homeassistant.components.application_credentials import AuthorizationServer
from homeassistant.core import HomeAssistant

OAUTH2_AUTHORIZE = "https://hl-userpool-naelick-sandbox.auth.us-east-2.amazoncognito.com/oauth2/authorize"
OAUTH2_TOKEN = (
    "https://hl-userpool-naelick-sandbox.auth.us-east-2.amazoncognito.com/oauth2/token"
)


async def async_get_authorization_server(hass: HomeAssistant) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )
