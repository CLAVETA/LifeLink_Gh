from nicegui import ui, app
import os
import requests
from utils.api import base_url
from components.footer import show_footer
from components.navbar import show_navbar
from typing import Set

PROFILE_ENDPOINT = f"{base_url}/donors/me/profile"
DELETE_PROFILE_ENDPOINT = f"{base_url}/donors/me/profile"
RESPONDED_REQUESTS_KEY = "responded_request_ids"


def clear_user_storage_safe():
    """Safely clear per-user storage without crashing on Windows file locks."""
    try:
        app.storage.user.clear()
    except PermissionError:
        try:
            for key in list(app.storage.user.keys()):
                try:
                    del app.storage.user[key]
                except Exception:
                    pass
        except Exception:
            pass
    except Exception:
        pass


def show_donor_card(profile: dict):
    """Shows a printable donor card dialog."""
    with (
        ui.dialog() as dialog,
        ui.card().classes("p-6 w-full max-w-md rounded-2xl shadow-2xl bg-white"),
    ):
        with ui.column().classes("items-center space-y-4"):
            ui.label("My Donor Card").classes(
                "text-2xl font-bold text-red-700 self-start"
            )
            with ui.card().classes(
                "w-full border border-gray-300 rounded-xl p-6 shadow-md bg-white"
            ):
                with ui.row().classes("w-full justify-between items-center mb-4"):
                    # optional logo if available
                    if os.path.exists(os.path.join(os.getcwd(), "assets", "logo.png")):
                        ui.image("/assets/logo.png").classes("h-12")
                    ui.label("LifeLink GH").classes("text-xl font-bold text-red-700")

                ui.image(
                    profile.get(
                        "profile_picture_url",
                        profile.get(
                            "avatar",
                            "https://placehold.co/200x200/ff0000/ffffff?text=JD",
                        ),
                    )
                ).classes("w-24 h-24 mx-auto rounded-full border-2 border-red-600")
                ui.label(profile.get("full_name", "")).classes("text-xl font-bold")
                ui.label(f"Blood Type: {profile.get('blood_type', '')}").classes(
                    "text-2xl font-extrabold text-red-600"
                )
                ui.label(f"ID: {profile.get('id', profile.get('_id', ''))}").classes(
                    "text-sm font-medium"
                )
                ui.label(f"Location: {profile.get('location', '')}").classes("text-sm")
                ui.separator()
                with ui.column().classes("text-center text-sm text-gray-600 space-y-1"):
                    ui.label("Registered: on file")
                    ui.label("Emergency Contact: +233 XX XXX XXXX")

            with ui.row().classes("w-full justify-between gap-4 mt-4"):
                ui.button("Print Card", icon="print").classes(
                    "flex-1 bg-red-600 text-white"
                ).on_click(lambda: ui.run_javascript("window.print();"))
                ui.button("Close", icon="close").props("outline").classes(
                    "flex-1"
                ).on_click(dialog.close)
    dialog.open()


def show_delete_confirmation(token: str):
    """Shows delete profile confirmation dialog and deletes on confirm."""
    with ui.dialog() as dialog, ui.card().classes("p-6 max-w-md"):
        ui.label("Delete Profile").classes("text-xl font-bold text-red-600 mb-4")
        ui.label(
            "Are you sure you want to delete your profile? This action cannot be undone."
        ).classes("text-gray-700 mb-6")

        async def delete_profile():
            try:
                headers = {
                    "Authorization": f"Bearer {token}",
                    "accept": "application/json",
                }
                resp = requests.delete(
                    DELETE_PROFILE_ENDPOINT, headers=headers, timeout=10
                )
                if resp.status_code in (200, 204):
                    ui.notify("Profile deleted successfully", color="green")
                    clear_user_storage_safe()
                    ui.navigate.to("/")
                else:
                    ui.notify(
                        f"Failed to delete profile: {resp.status_code}", color="red"
                    )
            except Exception as e:
                ui.notify(f"Error deleting profile: {e}", color="red")
            finally:
                dialog.close()

        with ui.row().classes("w-full justify-end gap-4"):
            ui.button("Cancel", icon="close").props("flat").on_click(dialog.close)
            ui.button("Delete Profile", icon="delete").classes(
                "bg-red-600 text-white"
            ).on_click(delete_profile)


def get_responded_requests() -> Set[str]:
    """Get set of request IDs that the current donor has already responded to."""
    try:
        return set(app.storage.user.get(RESPONDED_REQUESTS_KEY, []))
    except (AttributeError, AssertionError):
        return set()


def mark_request_as_responded(request_id: str):
    """Mark a request as responded to prevent showing it again."""
    try:
        responded = get_responded_requests()
        responded.add(request_id)
        app.storage.user[RESPONDED_REQUESTS_KEY] = list(responded)
    except (AttributeError, AssertionError):
        pass  # Storage not available


def is_request_responded(request_id: str) -> bool:
    """Check if donor has already responded to this request."""
    return request_id in get_responded_requests()


@ui.page("/donor/profile/edit")
def edit_profile_page():
    """Dedicated page for editing donor profile."""
    token = None
    try:
        token = app.storage.user.get("access_token")
    except AssertionError:
        token = None

    if not token:
        ui.notify("Please log in to edit your profile.", color="red")
        ui.navigate.to("/donor/login")
        return

    try:
        headers = {"Authorization": f"Bearer {token}", "accept": "application/json"}
        resp = requests.get(PROFILE_ENDPOINT, headers=headers, timeout=8)
        resp.raise_for_status()
        profile = resp.json()
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else None
        if status in (401, 403):
            clear_user_storage_safe()
            ui.notify("Session expired. Please log in again.", color="red")
            ui.navigate.to("/donor/login")
            return
        ui.notify(f"Failed to load profile ({status}).", color="red")
        profile = {}
    except Exception as e:
        ui.notify(f"Failed to load profile: {e}", color="red")
        profile = {}

    name = ui.input("Full Name", value=profile.get("full_name", "")).classes("w-full")
    phone = ui.input("Phone Number", value=profile.get("phone_number", "")).classes(
        "w-full"
    )
    location = ui.input("Location", value=profile.get("location", "")).classes("w-full")
    current_status = (profile.get("availability_status") or "").lower() == "available"
    availability = ui.switch("Available for donation", value=current_status)

    async def save_changes():
        if not name.value or not phone.value or not location.value:
            ui.notify("Please fill all required fields", color="red")
            return
        try:
            data = {
                "full_name": name.value,
                "phone_number": phone.value,
                "location": location.value,
                "availability_status": "Available"
                if availability.value
                else "Unavailable",
            }
            headers = {
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            resp = requests.put(
                PROFILE_ENDPOINT, headers=headers, data=data, timeout=10
            )
            if resp.status_code in (200, 201):
                ui.notify("Profile updated successfully!", color="green")
                ui.navigate.to("/donor/profile")
            else:
                ui.notify(f"Update failed: {resp.text}", color="red")
        except Exception as e:
            ui.notify(f"Error updating profile: {e}", color="red")

    with ui.column().classes("w-full min-h-screen"):
        show_navbar()
        with ui.column().classes("flex-grow w-full max-w-3xl mx-auto px-4 py-8"):
            with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white"):
                with ui.row().classes("w-full justify-between items-center mb-4"):
                    ui.label("Edit Profile").classes("text-2xl font-bold")
                    ui.button("Back", icon="arrow_back").props("flat").on_click(
                        lambda: ui.navigate.to("/donor/profile")
                    )

                with ui.column().classes("w-full space-y-4"):
                    name.props("outlined required")
                    phone.props("outlined required")
                    location.props("outlined required")
                    availability.classes("mt-2")
                    with ui.row().classes("w-full justify-end gap-4 mt-4"):
                        ui.button("Cancel", icon="close").props("flat").on_click(
                            lambda: ui.navigate.to("/donor/profile")
                        )
                        ui.button("Save Changes", icon="save").classes(
                            "bg-red-600 text-white"
                        ).on_click(save_changes)
        show_footer()


@ui.page("/donor/profile")
def donor_profile_page():
    """Centered donor profile page with navbar, footer, donor card and delete functionality."""
    # read token safely (app.storage.user may raise AssertionError if no session storage yet)
    try:
        token = app.storage.user.get("access_token")
    except AssertionError:
        token = None

    # debug logging so you can inspect server logs for token presence / partial value
    print("DEBUG: donor_profile_page token present:", bool(token))
    if token:
        try:
            print("DEBUG: token prefix:", token[:8])
        except Exception:
            pass

    # if no token, show a friendly prompt (don't auto-redirect)
    if not token:
        ui.notify("Please log in to view your profile.", color="red")
        with ui.column().classes("w-full min-h-screen items-center justify-center"):
            with ui.card().classes("p-6 w-full max-w-md text-center"):
                ui.label("You're not signed in").classes("text-xl font-bold mb-2")
                ui.label("Please sign in to access your profile and settings.").classes(
                    "text-sm text-gray-600 mb-4"
                )
                ui.button("Go to Login", icon="login").classes(
                    "bg-red-600 text-white"
                ).on_click(lambda: ui.navigate.to("/donor/login"))
        return

    try:
        headers = {"Authorization": f"Bearer {token}", "accept": "application/json"}
        resp = requests.get(PROFILE_ENDPOINT, headers=headers, timeout=8)
        resp.raise_for_status()
        profile = resp.json()
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else None
        if status in (401, 403):
            clear_user_storage_safe()
            ui.notify("Session expired. Please log in again.", color="red")
            ui.navigate.to("/donor/login")
            return
        ui.notify(f"Failed to load profile ({status}).", color="red")
        profile = {}
    except Exception as e:
        ui.notify(f"Failed to load profile: {e}", color="red")
        profile = {}

    # avatar fallback: prefer profile URL, then local asset, then external placeholder
    local_asset_path = os.path.join(os.getcwd(), "assets", "default-avatar.png")
    if profile.get("profile_picture_url"):
        picture = profile.get("profile_picture_url")
    elif os.path.exists(local_asset_path):
        picture = ""
    else:
        picture = "https://placehold.co/200x200/ff0000/ffffff?text=JD"

    # helper to update availability on backend
    async def update_availability_status(new_status: str):
        """Update donor's availability status on the backend. Status must be lowercase."""
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            # Ensure status is lowercase for backend compatibility
            data = {"availability_status": new_status.lower()}
            resp = requests.put(PROFILE_ENDPOINT, headers=headers, data=data, timeout=8)

            if resp.status_code in (200, 201):
                ui.notify(f"Status updated to {new_status}", color="green")
                return True
            ui.notify(f"Failed to update status: {resp.status_code}", color="red")
            return False
        except Exception as e:
            ui.notify(f"Error updating status: {e}", color="red")
            return False

    # Layout
    with ui.column().classes("w-full min-h-screen"):
        show_navbar()

        # top quick bar: back to requests + availability toggle
        with ui.row().classes("w-full bg-gray-50 py-2 shadow-sm"):
            with ui.row().classes(
                "max-w-7xl mx-auto w-full justify-between items-center px-4"
            ):
                ui.button("← Back to Donation Requests", icon="arrow_back").props(
                    "flat color=red"
                ).on_click(lambda: ui.navigate.to("/donor/donation_request"))
                with ui.row().classes("items-center gap-3"):
                    ui.label("Availability:").classes("text-gray-600")
                    current_status = (
                        profile.get("availability_status", "") or ""
                    ).lower() == "available"

                    @ui.refreshable
                    def status_display(is_available: bool):
                        ui.label(
                            "Available" if is_available else "Unavailable"
                        ).classes(
                            "font-medium "
                            + ("text-green-600" if is_available else "text-gray-600")
                        )

                    async def handle_status_change(e):
                        new_status = "available" if e.value else "unavailable"
                        if await update_availability_status(new_status):
                            status_display.refresh(e.value)

                    ui.switch(
                        value=current_status, on_change=handle_status_change
                    ).props('color="red"')
                    status_display(current_status)

        # centered main card
        with ui.column().classes("flex-grow w-full max-w-3xl mx-auto px-4 py-8"):
            with ui.card().classes(
                "w-full p-6 shadow-lg rounded-xl bg-white text-center"
            ):
                ui.image(picture).classes(
                    "w-28 h-28 mx-auto rounded-full border-2 border-red-600 mb-4"
                )
                ui.label(profile.get("full_name", "Donor Name")).classes(
                    "text-2xl font-bold"
                )
                ui.label(profile.get("blood_type", "Blood Type")).classes(
                    "text-xl font-semibold text-red-600 mt-1"
                )
                with ui.row().classes("w-full justify-center gap-4 mt-4"):
                    ui.button("Edit Profile", icon="edit").props(
                        "outline color=red"
                    ).on_click(lambda: ui.navigate.to("/donor/profile/edit"))
                    ui.button("View Donor Card", icon="badge").on_click(
                        lambda: show_donor_card(profile)
                    )
                    ui.button("Delete Profile", icon="delete_forever").classes(
                        "bg-red-600 text-white"
                    ).on_click(lambda: show_delete_confirmation(token))

                ui.separator().classes("my-4")
                # details grid
                with ui.grid().classes(
                    "grid grid-cols-1 md:grid-cols-2 gap-4 text-left"
                ):

                    def field_block(label_text, value):
                        with ui.card().classes("p-4 bg-gray-50 rounded-lg"):
                            ui.label(label_text).classes("text-xs text-gray-500")
                            ui.label(value or "—").classes(
                                "text-base text-gray-800 font-medium mt-1"
                            )

                    field_block("Email", profile.get("email"))
                    field_block("Phone", profile.get("phone_number"))
                    field_block("Location", profile.get("location"))
                    field_block("Date of Birth", profile.get("date_of_birth"))
                    field_block("Availability", profile.get("availability_status"))
                    field_block("Latitude", profile.get("lat"))
                    field_block("Longitude", profile.get("lon"))

        show_footer()
