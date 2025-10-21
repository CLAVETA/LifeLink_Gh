from nicegui import ui, app
import asyncio
import requests
from utils.api import (
    base_url,
    get_my_donation_history,
    get_donor_profile,
)
from components.donor_header import donor_header
from components.donor_sidebar import donor_sidebar

app.add_static_files("/assets", "assets")
Timeout = 10

def footer():
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


# -------- FETCH HELPERS ----------
async def fetch_data(url: str):  
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(None, lambda: requests.get(url, timeout=Timeout))
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Fetch error: {e}")
        return None


async def fetch_dashboard_data():
    """Fetch donor data concurrently (faster page load)."""
    try:
        results = await asyncio.gather(
            get_my_donation_history(),
            get_donor_profile(),
            return_exceptions=True
        )
        donation_history, donor_profile = results
        if isinstance(donation_history, Exception):
            donation_history = []
        if isinstance(donor_profile, Exception):
            donor_profile = {"name": "Donor", "blood_group": "-", "total_donations": 0}
        return donation_history, donor_profile
    except Exception as e:
        print("Error fetching dashboard data:", e)
        return [], {"name": "Donor", "blood_group": "-", "total_donations": 0}


# -------- DONATION HISTORY COMPONENT ----------
def donation_history_section(donation_history=None, loading=False):
    """Render donation history with list/grid toggle and shimmer loader."""
    donation_history = donation_history or []

    # Updated column definitions to match backend schema
    COLUMNS = [
        {'name': 'id', 'label': 'ID', 'field': 'id', 'align': 'left'},
        {'name': 'donation_date', 'label': 'DATE', 'field': 'donation_date', 'align': 'left'},
        {'name': 'location', 'label': 'LOCATION', 'field': 'location', 'align': 'left'},
        {'name': 'recipient_info', 'label': 'RECIPIENT INFO', 'field': 'recipient_info', 'align': 'left'},
        {'name': 'status', 'label': 'STATUS', 'field': 'status', 'align': 'center'},
    ]

    view_mode = ui.label('table').props('hidden')
    history_container = ui.column().classes("w-full mt-4")

    def render_list_view():
        """Render donation history in a table format."""
        with history_container:
            ui.table(columns=COLUMNS, rows=donation_history, row_key='id') \
                .props('flat bordered dense') \
                .classes('w-full rounded-lg overflow-hidden')

    def render_grid_view():
        """Render donation history in a card grid format."""
        with history_container:
            with ui.row().classes("w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"):
                for donation in donation_history:
                    with ui.card().classes("p-4 shadow-sm rounded-xl bg-white border-t-4 border-red-500 hover:shadow-md transition"):
                        ui.label(f"ID: {donation.get('id', 'N/A')}").classes("text-sm text-gray-500")
                        ui.label(donation.get('donation_date', 'N/A')).classes("text-lg font-semibold text-gray-800")
                        ui.label(donation.get('location', 'N/A')).classes("text-gray-600 text-sm mt-1")
                        ui.label(f"Recipient: {donation.get('recipient_info', '-') }").classes("text-gray-600 text-sm mt-1")
                        ui.badge(donation.get('status', 'Pending'), color='green').classes("mt-2 px-3 py-1 text-xs font-semibold")

    def update_history_view():
        history_container.clear()
        if view_mode.text == 'table':
            render_list_view()
        else:
            render_grid_view()

    def toggle_view(mode):
        view_mode.set_text(mode)
        update_icons()
        update_history_view()

    def update_icons():
        if view_mode.text == 'table':
            list_btn.props('flat color=red')
            grid_btn.props('flat color=gray')
        else:
            list_btn.props('flat color=gray')
            grid_btn.props('flat color=red')

    # Render component
    with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white mt-6"):
        with ui.row().classes("w-full justify-between items-center mb-4 border-b pb-4"):
            ui.label("Donation History").classes("text-xl font-semibold text-gray-800")
            with ui.row().classes("items-center gap-2"):
                list_btn = ui.button(icon="fa-solid fa-list", on_click=lambda: toggle_view('table')).props('flat round dense')
                grid_btn = ui.button(icon="fa-solid fa-grip", on_click=lambda: toggle_view('grid')).props('flat round dense')
                update_icons()

        if loading:
            with ui.column().classes("w-full animate-pulse space-y-4"):
                for _ in range(4):
                    ui.row().classes("h-20 bg-gray-200 rounded-lg")
        else:
            history_container
            update_history_view()


# -------- DASHBOARD PAGE ----------
@ui.page("/donor/dashboard")
async def donor_dashboard_page():
    """Donor dashboard — async optimized and API-integrated."""
    ui.add_head_html('<script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>')
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")

    # Layout
    with ui.header(elevated=True).classes('bg-white dark:bg-gray-800 text-black dark:text-white'):
        donor_header()
    with ui.left_drawer(bordered=True).classes('bg-gray-100 dark:bg-gray-900'):
        donor_sidebar()

    dashboard_container = ui.column().classes("flex-grow w-full p-4 md:p-8")

    # Instant shimmer on load
    with dashboard_container:
        with ui.row().classes("w-full items-center justify-between mb-6"):
            ui.label("Donor Dashboard").classes("text-3xl font-bold text-gray-800")
            ui.label("Loading donor profile...").classes("text-lg text-gray-600 sm:block")
        donation_history_section([], loading=True)

    # Background data loading (non-blocking)
    async def update_dashboard():
        donation_history, donor_profile = await fetch_dashboard_data()

        dashboard_container.clear()
        with dashboard_container:
            with ui.row().classes("w-full items-center justify-between mb-6"):
                ui.label("Donor Dashboard").classes("text-3xl font-bold text-gray-800")
                ui.label(f"Welcome, {donor_profile.get('name', 'Donor')}!").classes("text-lg text-gray-600 sm:block")

            # Render fetched donation history
            donation_history_section(donation_history)

            # Simple impact section
            with ui.element("section").props("id=impacts").classes("w-full py-12 px-4 md:px-12 bg-white mt-6"):
                ui.label("My Impacts").classes("text-2xl font-bold text-gray-800 mb-4")
                with ui.row().classes("grid grid-cols-1 md:grid-cols-4 gap-4 w-full"):
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

    asyncio.create_task(update_dashboard())



    # 4. Footer (Consistent with the style used in the other pages)
    footer()
