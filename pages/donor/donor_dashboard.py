from nicegui import ui, app
import asyncio
import requests
from utils.api import (
    base_url,
    get_my_donation_history,
    get_donor_profile,
    respond_to_donation_request,
)

app.add_static_files("/assets", "assets")

# components
from components.donor_header import donor_header
from components.donor_sidebar import donor_sidebar

Timeout = 10


# ---- FETCH FUNCTIONS ----
async def fetch_data(url: str):
    """Fetches JSON data from the FastAPI backend asynchronously."""
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: requests.get(url, timeout=Timeout))
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print("Error fetching data:", e)
        return None


async def fetch_dashboard_data():
    """Fetch all required data from the backend."""
    try:
        donation_history = await get_my_donation_history()
        donor_profile = await get_donor_profile()
        return donation_history, donor_profile
    except Exception as e:
        print(f"Error fetching dashboard data: {e}")
        return [], {"name": "Donor", "blood_group": "-", "total_donations": 0}


# ---- DONATION HISTORY SECTION ----
def donation_history_section(donation_history=None, loading=False):
    """Render donation history with grid/list toggle and shimmer loading effect."""

    # Table Columns
    COLUMNS = [
        {'name': 'date', 'label': 'DATE', 'field': 'date', 'align': 'left'},
        {'name': 'location', 'label': 'LOCATION', 'field': 'location', 'align': 'left'},
        {'name': 'type', 'label': 'TYPE', 'field': 'type', 'align': 'left'},
        {'name': 'status', 'label': 'STATUS', 'field': 'status', 'align': 'center'},
    ]

    # State for view toggle
    view_mode = ui.label('list').props('hidden')
    history_container = ui.column().classes("w-full mt-4")

    def render_list_view():
        """Render as table/list view."""
        with history_container:
            ui.table(columns=COLUMNS, rows=donation_history, row_key='id') \
                .props('flat bordered dense') \
                .classes('w-full rounded-lg overflow-hidden')

    def render_grid_view():
        """Render as grid view."""
        with history_container:
            with ui.row().classes("w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"):
                for donation in donation_history:
                    with ui.card().classes("p-4 shadow-sm rounded-xl bg-white border-t-4 border-red-500 transition hover:shadow-md"):
                        ui.label(donation.get('date', 'N/A')).classes("text-sm text-gray-500")
                        ui.label(donation.get('location', 'N/A')).classes("text-lg font-semibold text-gray-800")
                        with ui.row().classes("w-full justify-between items-center mt-2 text-sm"):
                            ui.label(f"Type: {donation.get('type', '-') }").classes("text-red-600 font-medium")
                            ui.label(f"ID: {donation.get('id', '')}").classes("text-gray-500")
                        ui.badge(donation.get('status', 'Pending'), color='green').classes("mt-2 px-3 py-1 text-xs font-semibold")

    def update_history_view():
        history_container.clear()
        if view_mode.text == 'list':
            render_list_view()
        else:
            render_grid_view()

    def toggle_view(mode):
        view_mode.set_text(mode)
        update_icons()
        update_history_view()

    def update_icons():
        # Highlight the active button in red
        if view_mode.text == 'list':
            list_btn.props('flat color=red')
            grid_btn.props('flat color=gray')
        else:
            list_btn.props('flat color=gray')
            grid_btn.props('flat color=red')

    # Donation History Card
    with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white mt-6"):
        # --- Header Section (fixed order) ---
        with ui.row().classes("w-full justify-between items-center mb-4 border-b pb-4"):
            ui.label("Donation History").classes("text-xl font-semibold text-gray-800")

            # Modern icon toggle (FontAwesome)
            with ui.row().classes("items-center gap-2"):
                list_btn = ui.button(icon="fa-solid fa-list", on_click=lambda: toggle_view('list')).props('flat round dense')
                grid_btn = ui.button(icon="fa-solid fa-grip", on_click=lambda: toggle_view('grid')).props('flat round dense')
                update_icons()

        # --- Content Section ---
        if loading:
            # Shimmer loader placeholder
            with ui.column().classes("w-full animate-pulse space-y-4"):
                for _ in range(4):
                    ui.row().classes("h-20 bg-gray-200 rounded-lg")
        else:
            history_container
            update_history_view()


# ---- MAIN DASHBOARD PAGE ----
@ui.page("/donor/dashboard")
async def donor_dashboard_page():
    """Main donor dashboard page with live backend data."""
    ui.add_head_html('<script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>')
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")

    with ui.header(elevated=True).classes('bg-white dark:bg-gray-800 text-black dark:text-white'):
        donor_header()
    with ui.left_drawer(bordered=True).classes('bg-gray-100 dark:bg-gray-900'):
        donor_sidebar()

    # Create a parent container that we can later clear
    dashboard_container = ui.column().classes("flex-grow w-full p-4 md:p-8")

    # Show shimmer while data loads
    with dashboard_container:
        donation_history_section([], loading=True)
        ui.label("Loading donor data...").classes("text-gray-500 text-center mb-6")

    # Fetch donor data (simulate or call actual function)
    donation_history, donor_profile = await fetch_dashboard_data()

    # Clear loading content
    dashboard_container.clear()

    # Re-render real dashboard
    with dashboard_container:
        # Header section
        with ui.row().classes("w-full items-center justify-between mb-6"):
            ui.label("Donor Dashboard").classes("text-3xl font-bold text-gray-800")
            ui.label(f"Welcome, {donor_profile.get('name', 'Donor')}!").classes("text-lg text-gray-600 sm:block")

        # Donation History Section
        donation_history_section(donation_history)

# @ui.page("/donor/dashboard")
# async def donor_dashboard_page():
#     """Main donor dashboard page with live backend data."""
#     ui.add_head_html('<script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>')
#     ui.query(".nicegui-content").classes("m-0 p-0 gap-0")

#     # Header & Sidebar
#     with ui.header(elevated=True).classes('bg-white dark:bg-gray-800 text-black dark:text-white'):
#         donor_header()
#     with ui.left_drawer(bordered=True).classes('bg-gray-100 dark:bg-gray-900'):
#         donor_sidebar()

#     with ui.column().classes("flex-grow w-full p-4 md:p-8"):

#         # Show shimmer while loading
#         donation_history_section([], is_loading=True)

#         # Fetch data asynchronously
#         donation_history, donor_profile = await fetch_dashboard_data()

#         # Clear and re-render once data arrives
#         ui.clear()
#         with ui.column().classes("flex-grow w-full p-4 md:p-8"):
#             # Dashboard Header
#             with ui.row().classes("w-full items-center justify-between mb-6"):
#                 ui.label("Donor Dashboard").classes("text-3xl font-bold text-gray-800")
#                 ui.label(f"Welcome, {donor_profile.get('name', 'Donor')}!").classes("text-lg text-gray-600 sm:block")

#             # Donation History Section (loaded)
#             donation_history_section(donation_history)

            # Impact Section
    with ui.element("section").props("id=impacts").classes("w-full py-20 px-10 md:px-20 bg-white"):
        ui.label("My Impacts").classes("text-3xl font-bold text-gray-800 mt-8")
        with ui.row().classes("grid grid-cols-1 md:grid-cols-4 gap-4 w-full mb-8"):
                with ui.card().classes("p-4 shadow-lg rounded-xl bg-white border-l-4 border-red-500"):
                    ui.label("Total Donations").classes("text-2xl font-medium text-gray-500")
                    ui.label(str(donor_profile.get("total_donations", 0))).classes("text-3xl font-extrabold text-gray-900 mt-1")

                with ui.card().classes("p-4 shadow-lg rounded-xl bg-white border-l-4 border-blue-500"):
                    ui.label("Last Donation").classes("text-2xl font-medium text-gray-500")
                    ui.label(donor_profile.get("last_donation", "N/A")).classes("text-sm font-extrabold text-gray-900 mt-1")

                with ui.card().classes("p-4 shadow-lg rounded-xl bg-white border-l-4 border-green-500"):
                    ui.label("Lives Saved").classes("text-2xl font-medium text-gray-500")
                    ui.label(str(donor_profile.get("lives_saved", 0))).classes("text-3xl font-extrabold text-gray-900 mt-1")

                with ui.card().classes("p-4 shadow-lg rounded-xl bg-white border-l-4 border-green-500"):
                    ui.label("Impact Score").classes("text-2xl font-medium text-gray-500")
                    ui.label(donor_profile.get("impact_score", "A")).classes("text-3xl font-extrabold text-gray-900 mt-1")

            # Schedule Section
    with ui.element("section").props("id=find_drive").classes("w-full py-20 px-10 md:px-20 bg-white"):
        with ui.card().classes("p-6 shadow-lg rounded-xl bg-white"):
                ui.label("Upcoming Appointments").classes("text-xl font-semibold text-gray-800 mb-4")
                next_appt = donor_profile.get("next_appointment", None)
                if next_appt:
                    ui.label(f"{next_appt['date']} at {next_appt['location']}").classes("text-gray-700")
                    ui.button("Cancel", color="red").props("flat dense")
                else:
                    ui.label("No upcoming appointments").classes("text-gray-500")
                    ui.label("Schedule a new appointment to continue saving lives")
                    ui.button("Find a Drive", icon="add_circle").props("no-caps").classes(
                        "bg-red text-white px-6 py-3 mt-3 rounded-xl shadow-lg hover:bg-red transition text-lg"
                    )
        # 4. Footer (Consistent with the style used in the other pages)
    with ui.row().classes("flex flex-col md:flex-row items-center justify-between px-7 w-full bg-gray-50 py-5 text-sm mt-auto text-gray-500"):
            ui.image("/assets/logo.png").classes("w-24 h-20") 
            ui.label("© 2025 LifeLink. All rights reserved.").classes("mb-3 md:mb-0 text-xl hover:text-red")
            with ui.row().classes("gap-3"):
                ui.link("About","/about").classes("no-underline text-gray-700 hover:text-red transition text-xl")
                ui.link("Contact","/about#contact").classes("no-underline hover:text-red text-gray-700 text-xl transition")
                ui.link("Privacy Policy").classes("no-underline text-gray-700 hover:text-red transition text-xl")            
            with ui.row().classes("gap-6"):
                ui.html('<i class="fa-brands fa-square-linkedin text-xl hover:text-red-600 transition"></i>', sanitize=False)
                ui.html('<i class="fa-brands fa-instagram text-xl hover:text-red-600 transition"></i>', sanitize=False)
                ui.html('<i class="fa-brands fa-facebook text-xl hover:text-red-600 transition"></i>', sanitize=False)
