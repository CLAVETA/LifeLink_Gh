from nicegui import ui, app
import asyncio
import requests
# NOTE: Assumes components are correctly imported from the local 'components' directory
from components.donor_header import donor_header
from components.donor_sidebar import donor_sidebar
from components.donor_footer import donor_footer

PROFILE_ENDPOINT = "https://lifelinkgh-api.onrender.com/donors/me/profile"
HISTORY_ENDPOINT = "https://lifelinkgh-api.onrender.com/donors/me/history"
Timeout = 10


# -------- FETCH HELPERS ----------
async def fetch_data(url: str):
    """Fetches data from a given endpoint with authentication and handles common errors."""
    token = app.storage.user.get("access_token")
    
    if not token:
        ui.notify("You are not logged in. Redirecting...", color="red")
        await asyncio.sleep(1)
        # FIX: Use run_javascript for reliable navigation from an async task context
        ui.run_javascript('window.location.href = "/donor/login"')
        return None

    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    try:
        loop = asyncio.get_event_loop()
        # Run synchronous requests.get in a separate thread to prevent blocking NiceGUI's event loop
        response = await loop.run_in_executor(
            None, lambda: requests.get(url, headers=headers, timeout=Timeout)
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            ui.notify("Session expired. Please log in again.", color="red")
            await asyncio.sleep(1)
            # FIX: Use run_javascript for reliable navigation from an async task context
            ui.run_javascript('window.location.href = "/donor/login"')
        else:
            print(f"API error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Fetch error: {e}")
    return None


async def fetch_dashboard_data():
    """Fetch donor data concurrently and safely handle exceptions."""
    try:
        results = await asyncio.gather(
            fetch_data(HISTORY_ENDPOINT),
            fetch_data(PROFILE_ENDPOINT),
            return_exceptions=True,
        )
        donation_history, donor_profile = results

        # Handle exceptions for profile fetch
        if isinstance(donor_profile, Exception) or donor_profile is None:
            print(f"Profile fetch failed: {donor_profile}")
            donor_profile = {"full_name": "Donor", "blood_type": "-", "total_donations": 0}

        # Handle exceptions for history fetch
        if isinstance(donation_history, Exception) or donation_history is None:
            # This is where the error message was being printed if the exception occurred in fetch_data
            print(f"History fetch failed: {donation_history}")
            donation_history = []

        return donation_history, donor_profile

    except Exception as e:
        print(f"Error fetching dashboard data: {e}")
        return [], {"full_name": "Donor", "blood_type": "-", "total_donations": 0}


# -------- DONATION HISTORY COMPONENT ----------
def donation_history_section(donation_history=None, loading=False):
    """Render donation history with toggle view."""
    donation_history = donation_history or []

    COLUMNS = [
        {"name": "id", "label": "ID", "field": "id", "align": "left"},
        {"name": "donation_date", "label": "DATE", "field": "donation_date", "align": "left"},
        {"name": "location", "label": "LOCATION", "field": "location", "align": "left"},
        {"name": "recipient_info", "label": "RECIPIENT INFO", "field": "recipient_info", "align": "left"},
        {"name": "status", "label": "STATUS", "field": "status", "align": "center"},
    ]

    view_mode = ui.label("table").props("hidden")
    history_container = ui.column().classes("w-full mt-4")

    def render_list_view():
        with history_container:
            if not donation_history:
                 ui.label("No donation history found.").classes("text-center text-lg text-gray-500 p-8 w-full")
                 return
            ui.table(columns=COLUMNS, rows=donation_history, row_key="id") \
                .props("flat bordered dense") \
                .classes("w-full rounded-lg overflow-hidden")

    def render_grid_view():
        with history_container:
            if not donation_history:
                 ui.label("No donation history found.").classes("text-center text-lg text-gray-500 p-8 w-full")
                 return
            with ui.row().classes("grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 w-full"):
                for donation in donation_history:
                    with ui.card().classes(
                        "p-4 shadow-sm rounded-xl bg-white border-t-4 border-red-500 hover:shadow-md transition"
                    ):
                        ui.label(f"ID: {donation.get('id', 'N/A')}").classes("text-sm text-gray-500")
                        ui.label(donation.get("donation_date", "N/A")).classes("text-lg font-semibold text-gray-800")
                        ui.label(donation.get("location", "N/A")).classes("text-gray-600 text-sm mt-1")
                        ui.label(f"Recipient: {donation.get('recipient_info', '-') }").classes(
                            "text-gray-600 text-sm mt-1"
                        )
                        ui.badge(donation.get("status", "Pending"), color="green").classes(
                            "mt-2 px-3 py-1 text-xs font-semibold"
                        )

    def update_history_view():
        history_container.clear()
        if view_mode.text == "table":
            render_list_view()
        else:
            render_grid_view()

    def toggle_view(mode):
        view_mode.set_text(mode)
        update_icons()
        update_history_view()

    def update_icons():
        if view_mode.text == "table":
            list_btn.props("flat color=red")
            grid_btn.props("flat color=gray")
        else:
            list_btn.props("flat color=gray")
            grid_btn.props("flat color=red")

    with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white mt-6"):
        with ui.row().classes("w-full justify-between items-center mb-4 border-b pb-4"):
            ui.label("Donation History").classes("text-xl font-semibold text-gray-800")
            with ui.row().classes("items-center gap-2"):
                list_btn = ui.button(icon="fa-solid fa-list", on_click=lambda: toggle_view("table")).props(
                    "flat round dense"
                )
                grid_btn = ui.button(icon="fa-solid fa-grip", on_click=lambda: toggle_view("grid")).props(
                    "flat round dense"
                )
                update_icons()

        if loading:
            with ui.column().classes("w-full animate-pulse space-y-4"):
                for _ in range(4):
                    # Placeholder rows for loading state
                    ui.row().classes("h-20 bg-gray-200 rounded-lg")
        else:
            history_container
            update_history_view()


# -------- DASHBOARD PAGE ----------
@ui.page("/donor/dashboard")
def donor_dashboard_page():
    # Load Font Awesome for icons
    ui.add_head_html(
        '<script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>'
    )
    # Remove default NiceGUI padding/gap
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")

    with ui.header(elevated=True).classes("bg-white text-black"):
        donor_header()

    with ui.left_drawer(bordered=True).classes("bg-gray-100"):
        donor_sidebar()

    # Main content container for the dashboard
    dashboard_container = ui.column().classes("flex-grow w-full p-4 md:p-8")

    # Initial Loading State (Shimmer)
    with dashboard_container:
        with ui.row().classes("w-full items-center justify-between mb-6"):
            ui.label("Donor Dashboard").classes("text-3xl font-bold text-gray-800")
            ui.label("Loading donor profile...").classes("text-lg text-gray-600 sm:block")
        donation_history_section([], loading=True)

    # -------- ASYNC FUNCTION TO UPDATE UI AFTER DATA FETCH --------
    async def update_dashboard():
        """Fetches data and updates the UI elements."""
        donation_history, donor_profile = await fetch_dashboard_data()

        # Ensure donor_profile is a valid dict
        if not isinstance(donor_profile, dict):
            donor_profile = {"full_name": "Donor", "blood_type": "-", "total_donations": 0}

        # Clear the container and re-render the dashboard with fetched data
        with dashboard_container:
            dashboard_container.clear()

            # Dashboard Header
            with ui.row().classes("w-full items-center justify-between mb-6"):
                ui.label("Donor Dashboard").classes("text-3xl font-bold text-gray-800")
                ui.label(f"Welcome, {donor_profile.get('full_name', 'Donor')}!") \
                    .classes("text-lg text-gray-600 sm:block")

            # Donation History Section
            donation_history_section(donation_history)

            # My Impacts Section
            with ui.element("section").props("id=impacts").classes("w-full py-12 px-4 md:px-12 bg-white mt-6"):
                ui.label("My Impacts").classes("text-2xl font-bold text-gray-800 mb-4")
                with ui.row().classes("grid grid-cols-1 md:grid-cols-4 gap-4 w-full"):
                    # Define statistics cards using data from donor_profile
                    stats = [
                        ("Total Donations", donor_profile.get("total_donations", 0), "red-500"),
                        ("Last Donation Date", donor_profile.get("last_donation", "N/A"), "blue-500"),
                        ("Lives Saved", donor_profile.get("lives_saved", 0), "green-500"),
                        ("Impact Score", donor_profile.get("impact_score", "A"), "purple-500"),
                    ]
                    for label, value, color in stats:
                        with ui.card().classes(f"p-4 shadow-md rounded-xl border-l-4 border-{color} bg-white"):
                            ui.label(label).classes("text-gray-600 text-lg")
                            ui.label(str(value)).classes("text-3xl font-bold text-gray-900")

    # Run the dashboard update coroutine safely in the background.
    asyncio.create_task(update_dashboard())

    donor_footer()
