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


def donation_history_section(donation_history):
    """Render donation history with list/grid toggle."""

    # Table Columns
    COLUMNS = [
        {'name': 'date', 'label': 'DATE', 'field': 'date', 'align': 'left'},
        {'name': 'location', 'label': 'LOCATION', 'field': 'location', 'align': 'left'},
        {'name': 'type', 'label': 'TYPE', 'field': 'type', 'align': 'left'},
        {'name': 'status', 'label': 'STATUS', 'field': 'status', 'align': 'center'},
    ]

    # State for view toggle
    view_mode = ui.label('table').props('hidden')
    history_container = ui.column().classes("w-full")

    def render_table_view():
        """Render as list/table view."""
        with history_container:
            ui.table(columns=COLUMNS, rows=donation_history, row_key='id') \
                .props('flat bordered dense') \
                .classes('w-full rounded-lg overflow-hidden')

    def render_grid_view():
        """Render as grid view."""
        with history_container:
            with ui.row().classes("w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"):
                for donation in donation_history:
                    with ui.card().classes("p-4 shadow-sm rounded-lg bg-white border-t-4 border-red-500"):
                        ui.label(donation.get('date', 'N/A')).classes("text-sm text-gray-500")
                        ui.label(donation.get('location', 'N/A')).classes("text-lg font-semibold text-gray-800")
                        with ui.row().classes("w-full justify-between items-center mt-2 text-sm"):
                            ui.label(f"Type: {donation.get('type', '-') }").classes("text-red-600 font-medium")
                            ui.label(f"ID: {donation.get('id', '')}").classes("text-gray-500")
                        ui.badge(donation.get('status', 'Pending'), color='green').classes("mt-2 px-3 py-1 text-xs font-semibold")

    def update_history_view():
        history_container.clear()
        if view_mode.text == 'table':
            render_table_view()
        else:
            render_grid_view()

    # Donation History Card
    with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white mt-4"):
        with ui.row().classes("w-full justify-between items-center mb-4 border-b pb-4"):
            ui.label("Donation History").classes("text-xl font-semibold text-gray-800")
            ui.toggle({'table': 'list', 'grid': 'grid_view'}, value='table') \
                .props('dense outline toggle-color=red') \
                .on('update:model-value', lambda e: (view_mode.set_text(e.value), update_history_view()))

        history_container
        update_history_view()


@ui.page("/donor/dashboard")
async def donor_dashboard_page():
    """Main donor dashboard page with live backend data."""
    ui.add_head_html('<script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>')
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")

    # Header & Sidebar
    with ui.header(elevated=True).classes('bg-white dark:bg-gray-800 text-black dark:text-white'):
        donor_header()
    with ui.left_drawer(bordered=True).classes('bg-gray-100 dark:bg-gray-900'):
        donor_sidebar()

    with ui.column().classes("flex-grow w-full p-4 md:p-8"):
        spinner = ui.spinner(size="lg").classes("text-red-500 mx-auto")
        ui.label("Loading donor data...").classes("text-gray-500 text-center")

        # Fetch data asynchronously
        donation_history, donor_profile = await fetch_dashboard_data()
        spinner.delete()

        # Dashboard Header
        with ui.row().classes("w-full items-center justify-between mb-6"):
            ui.label("Donor Dashboard").classes("text-3xl font-bold text-gray-800")
            ui.label(f"Welcome, {donor_profile.get("name", "Donor")}!").classes("text-lg text-gray-600 sm:block")

        # Donation History
        donation_history_section(donation_history)

        # Impact Section
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
        with ui.card().classes("p-6 shadow-lg rounded-xl bg-white"):
            ui.label("Upcoming Appointments").classes("text-xl font-semibold text-gray-800 mb-4")
            next_appt = donor_profile.get("next_appointment", None)
            if next_appt:
                ui.label(f"{next_appt['date']} at {next_appt['location']}").classes("text-gray-700")
                ui.button("Cancel", color="red").props("flat dense")
            else:
                ui.label("No upcoming appointments").classes("text-gray-500")
                ui.label("Schedule a new appointment to continue saving lives")
                # ui.label("Data will load from backend once endpoint is exposed.")
                ui.button("Find a Drive", icon="add_circle").props("no-caps").classes("bg-red text-white px-6 py-3 mt-3 rounded-xl shadow-lg hover:bg-red transition text-lg")
                # ui.button("Schedule New Donation", icon="add_circle").classes("bg-red text-white mt-3")
                        
                        

# Initialize dark mode functionality for the page
# dark_mode = ui.dark_mode(value=False)

# def donation_history():
#     # Example data (replace with actual data from your backend)
#     DONATION_HISTORY_DATA = [
#         {'date': 'Oct 10, 2025', 'location': 'City Hospital', 'type': 'Whole Blood', 'status': 'Completed', 'id': 'D12345'},
#         {'date': 'Jul 15, 2025', 'location': 'Red Cross Drive', 'type': 'Platelets', 'status': 'Completed', 'id': 'D12344'},
#         {'date': 'Apr 02, 2025', 'location': 'Community Center', 'type': 'Whole Blood', 'status': 'Completed', 'id': 'D12343'},
#         {'date': 'Jan 05, 2025', 'location': 'University Campus', 'type': 'Plasma', 'status': 'Completed', 'id': 'D12342'},
#     ]

#     COLUMNS = [
#         {'name': 'date', 'label': 'DATE', 'field': 'date', 'align': 'left'},
#         {'name': 'location', 'label': 'LOCATION', 'field': 'location', 'align': 'left'},
#         {'name': 'type', 'label': 'TYPE', 'field': 'type', 'align': 'left'},
#         {'name': 'status', 'label': 'STATUS', 'field': 'status', 'align': 'center'},
#     ]

#     # State for view mode: 'table' or 'grid'
#     view_mode = ui.label('table').props('hidden') # Hidden label to store the state, defaulting to 'table'

#     # Placeholder container for the dynamic content
#     history_container = ui.column().classes("w-full")

#     def render_table_view():
#         """Renders the donation history as a table."""
#         with history_container:
#             with ui.table(columns=COLUMNS, rows=DONATION_HISTORY_DATA, row_key='id') \
#                 .props('flat bordered dense') \
#                 .classes('w-full rounded-lg overflow-hidden'):
                
#                 # Custom body for status column to render badges (FIXED BINDING)
#                 with ui.row().classes('w-full') as body:
#                     body.props('slot=body-cell-status slot-scope="props"')
#                     # Correct client-side binding using :label
#                     ui.badge().props('color=green :label=props.row.status').classes('px-2 py-1 rounded-full text-white text-xs font-semibold')
                                

#     def render_grid_view():
#         """Renders the donation history as a responsive card grid."""
#         with history_container:
#             with ui.row().classes("w-full grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"):
#                 for donation in DONATION_HISTORY_DATA:
#                     with ui.card().classes("w-full p-4 shadow-sm rounded-lg bg-white border-t-4 border-red-500"):
#                         ui.label(donation['date']).classes("text-sm text-gray-500")
#                         ui.label(donation['location']).classes("text-lg font-semibold text-gray-800")
                        
#                         # Type and ID details
#                         with ui.row().classes("w-full justify-between items-center mt-2 text-sm"):
#                             ui.label(f"Type: {donation['type']}").classes("text-red-600 font-medium")
#                             ui.label(f"ID: {donation['id']}").classes("text-gray-500")
                        
#                         # Status chip
#                         ui.badge(donation['status'], color='green').classes("mt-2 px-3 py-1 text-xs font-semibold")

#     def update_history_view():
#         """Clears the container and renders the selected view."""
#         history_container.clear()
#         if view_mode.text == 'table':
#             render_table_view()
#         else:
#             render_grid_view()

#     # Main card for the Donation History section
#     with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white mt-4"):
#         # This row contains the fixed header elements
#         with ui.row().classes("w-full justify-between items-center mb-4 border-b pb-4"):
#             ui.label("Donation History").classes("text-xl font-semibold text-gray-800")
            
#             # View Toggle Buttons
#             ui.toggle({
#                 'table': 'list', 
#                 'grid': 'grid_view'
#             }, value='table') \
#             .props('dense outline toggle-color=red') \
#             .on('update:model-value', lambda e: (view_mode.set_text(e.value), update_history_view()))
        
#         # history_container is defined here, making it a child of ui.card
#         # and positioned directly below the fixed header row.
#         history_container 
        
#         # Initial render of the history view
#         update_history_view()
                
# @ui.page("/donor/dashboard")
# def donor_dashboard_page():
#     # Setup for responsive design and removing default NiceGUI margins
#     ui.add_head_html('<script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>')
#     ui.query(".nicegui-content").classes("m-0 p-0 gap-0")

#     # Header
#     with ui.header(elevated=True).classes('bg-white dark:bg-gray-800 text-black dark:text-white'):
#         # Assuming donor_header() is defined
#         donor_header()      
        
#     # Left Drawer (Sidebar)
#     with ui.left_drawer(bordered=True).classes('bg-gray-100 dark:bg-gray-900'):
#         # Assuming donor_sidebar() is defined
#         donor_sidebar()
        
#     # Main Portal Container
#     with ui.column().classes("flex-grow w-full p-4 md:p-8"):
#         # Title and Welcome Message
#         with ui.row().classes("w-full items-center justify-between mb-6"):
#             ui.label("Donor Dashboard").classes("text-3xl font-bold text-gray-800")
#             ui.label("Welcome, Jane Doe!").classes("text-lg text-gray-600 sm:block")

#         # 3. Donation History Section (CORRECT PLACEMENT)
#         # This function call places the entire card containing the header and the history container
#         # directly below the Donor Dashboard title.
#         donation_history()
        
#         # 1. Stats Cards Section (Total Donations, Last Donation, Impact Score)
#         ui.label("My Impacts").classes("text-3xl font-bold text-gray-800 mt-8")
#         with ui.row().classes("grid grid-cols-1 md:grid-cols-4 gap-4 w-full mb-8"):
                            
#             # Card 1: Total Donations
#             with ui.card().classes("w-full p-4 shadow-lg rounded-xl bg-white border-l-4 border-red-500"):
#                 ui.label("Total Donations").classes("text-2xl font-medium text-gray-500")
#                 ui.label("04").classes("text-3xl font-extrabold text-gray-900 mt-1")
#                 ui.label("+10%").classes("text-sm text-red-500 mt-1")
                
#             # Card 2: Last Donation
#             with ui.card().classes("w-full h-full p-4 shadow-lg rounded-xl bg-white border-l-4 border-blue-500"):
#                 ui.label("Last Donation").classes("text-2xl font-medium text-gray-500")
#                 ui.label("3 Months Ago").classes("text-sm font-extrabold text-gray-900 mt-1 md-2")

#             # Card 3: Lives Saved
#             with ui.card().classes("w-full p-4 shadow-lg rounded-xl bg-white border-l-4 border-green-500"):
#                 ui.label("Lives Saved").classes("text-2xl font-medium text-gray-500")
#                 ui.label("9").classes("text-3xl font-extrabold text-gray-900 mt-1") 
#                 ui.label("+5%").classes("text-sm text-red-500 mt-1")                       
                
#             # Card 4: Impact Score
#             with ui.card().classes("w-full p-4 shadow-lg rounded-xl bg-white border-l-4 border-green-500"):
#                 ui.label("Impact Score").classes("text-2xl font-medium text-gray-500")
#                 ui.label("A+").classes("text-3xl font-extrabold text-gray-900 mt-1")
#                 ui.label("+15%").classes("text-sm text-red-500 mt-1")
                        
#         # 2. Main Content Cards (Appointments and Profile Actions)
#         with ui.row().classes("grid grid-cols-1 lg:grid-cols-3 gap-6 w-full"):
            
#             # Left Column (Appointments & History - Takes 2/3 space on large screens)
#             with ui.column().classes("lg:col-span-2 w-full space-y-6"):
                
#                 # Upcoming/Recent Appointments Card (Matches top left of screen.png)
#                 with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white"):
#                     ui.label("Upcoming & Recent Appointments").classes("text-xl font-semibold text-gray-800 mb-4")
                    
#                     # Next Appointment
#                     with ui.row().classes("w-full items-center justify-between border-b pb-3 mb-3"):
#                         with ui.row().classes("items-center space-x-3"):
#                             ui.icon("calendar_month").classes("text-3xl text-red-500")
#                             with ui.column().classes("gap-0"):
#                                 ui.label("Next Appointment").classes("font-medium text-gray-900")
#                                 ui.label("December 15, 2025, 11:00 AM at City Hospital").classes("text-sm text-gray-500")
#                         ui.button("Cancel").props("flat dense color=red").classes("text-red-500 hover:bg-red-100")

#                     # Last Donation (Matches bottom half of the appointments card in screen.png)
#                     with ui.row().classes("w-full items-center justify-between"):
#                         with ui.row().classes("items-center space-x-3"):
#                             ui.icon("check_circle").classes("text-3xl text-green-500")
#                             with ui.column().classes("gap-0"):
#                                 ui.label("Last Donation").classes("font-medium text-gray-900")
#                                 ui.label("October 10, 2025, 10:00 AM").classes("text-sm text-gray-500")
#                         ui.link("Details", "#").classes("text-red-500 font-medium text-sm hover:underline")
                        
#                     ui.separator().classes("my-4")
                    
#                     # Schedule Button (Primary Action)
#                     with ui.column().classes("w-full items-center mt-4"):
#                         ui.label("Schedule a new appointment to continue saving lives")
#                         ui.button("Find a Drive", icon="add_circle").props("no-caps").classes("bg-red text-white px-6 py-3 rounded-xl shadow-lg hover:bg-red-500 transition text-lg")
                        

#             # Right Column (Recent activity - Takes 1/3 space on large screens)
#             with ui.column().classes("lg:col-span-1 w-full space-y-6"):
                
#                 # Profile Info Card (Matches top right of screen.png)
#                 with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white"):
#                     ui.label("Recent Activity").classes("text-xl font-semibold text-gray-800 mb-4")
                    
#                     # Blood Group
#                     with ui.row().classes("w-full items-center space-x-4 mb-4"):
#                         ui.icon("water_drop").classes("text-4xl text-red-600")
#                         with ui.column().classes("gap-0"):
#                             ui.label("Blood Group").classes("text-sm text-gray-500")
#                             ui.label("O+").classes("text-3xl font-bold text-red-600")
                            
#                     ui.separator().classes("my-4")
                    