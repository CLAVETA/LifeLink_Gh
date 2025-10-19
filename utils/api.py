# base_url = "https://lifelinkgh-api.onrender.com"

import httpx
from nicegui import app

base_url = "https://lifelinkgh-api.onrender.com"

# ---------------- AUTHENTICATED REQUEST WRAPPER ---------------- #

def get_auth_header():
    """Retrieve JWT token stored in NiceGUI session and return authorization header."""
    token = app.storage.user.get("access_token")
    if not token:
        raise ValueError("User not authenticated: access_token not found in session.")
    return {"Authorization": f"Bearer {token}"}

# ---------------- API CALLS ---------------- #

async def get_my_donation_history():
    """Fetch donation history for logged-in donor."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/donors/me/history", headers=get_auth_header()
        )
        response.raise_for_status()
        return response.json()

async def get_donor_profile():
    """Fetch donor profile details."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/donors/me", headers=get_auth_header())
        response.raise_for_status()
        return response.json()

async def respond_to_donation_request(request_id: str, response_type: str):
    """
    Respond to a donation request.

    Args:
        request_id: ID of the donation request.
        response_type: 'accept' or 'decline'
    """
    payload = {"response": response_type}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/donors/requests/{request_id}/respond",
            json=payload,
            headers=get_auth_header(),
        )
        response.raise_for_status()
        return response.json()
