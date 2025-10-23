# from nicegui import ui
# import requests
# from utils.api import base_url
# import json

# PROFILE_ENDPOINT = f"{base_url}/donors/me/profile"


# def donor_sidebar(auth_token: str = None):
#     # Initial donor info with default values
#     donor_info = {
#         "name": "Name",
#         "blood_type": "None",
#         "donor_id": "None",
#         "location": "N/A",
#         "profile_picture_url": "https://placehold.co/100x100/A00000/FFFFFF?text=JD",
#         "is_available": False,
#     }

#     # Fetch donor profile from backend if token exists
#     if auth_token:
#         try:
#             headers = {"Authorization": f"Bearer {auth_token}"}
#             response = requests.get(PROFILE_ENDPOINT, headers=headers, timeout=10)
#             if response.status_code == 200:
#                 data = response.json()
#                 donor_info["name"] = data.get("full_name", "Donor").upper()
#                 donor_info["blood_type"] = data.get("blood_type", "None")
#                 donor_info["location"] = data.get("location", "N/A")
#                 donor_info["donor_id"] = str(data.get("donor_id", "0000"))
#             else:
#                 ui.notify(f"Failed to load donor profile ({response.status_code})", color="red")
#         except Exception as e:
#             ui.notify(f"Error fetching donor data: {e}", color="red")
#     else:
#         ui.notify("No authentication token found. Please log in.", color="red")

#     # Refreshable label for availability status
#     @ui.refreshable
#     def availability_status_text(is_available):
#         status_text = "Available" if is_available else "Unavailable"
#         ui.label(status_text).classes("text-lg font-medium text-gray-700")

#     # Toggle handler for availability status
#     def handle_availability_toggle(e):
#         donor_info["is_available"] = e.value
#         availability_status_text.refresh(donor_info["is_available"])
#         new_status = "Available" if e.value else "Unavailable"
#         ui.notify(f"Updating availability to: {new_status}. API call pending...", color="info")

#     # Donor card popup
#     def show_donor_card():
#         with ui.dialog() as dialog, ui.card().classes('p-6 w-full max-w-md rounded-2xl shadow-2xl bg-white'):
#             with ui.column().classes('items-center space-y-4'):
#                 ui.label("My Donor Card").classes("text-2xl font-bold text-red-700 self-start")

#                 with ui.card().classes('w-90 items-center border border-gray-300 rounded-xl p-4 shadow-md bg-white'):
#                     ui.image('assets/donor_profile.png').classes("w-20 h-20 rounded-full object-cover border-2 border-red-600")
#                     ui.label("Life Link GH").classes("text-lg font-semibold text-gray-800 mb-2")
#                     ui.separator()
#                     ui.label("NAME").classes("text-xs text-gray-500 mt-2")
#                     ui.label(donor_info["name"]).classes("text-xl font-bold text-gray-900")

#                     ui.label("BLOOD TYPE").classes("text-xs text-gray-500 mt-3")
#                     ui.label(donor_info["blood_type"]).classes("text-2xl font-extrabold text-red-600")

#                     ui.label("LOCATION").classes("text-xs text-gray-500 mt-3")
#                     ui.label(donor_info["location"]).classes("text-lg font-semibold text-red-500")

#                     ui.separator().classes("my-3")

#                     with ui.row().classes("justify-between items-center w-full"):
#                         ui.label("Valued Blood Donor").classes("text-sm text-gray-600 italic")
#                         with ui.column().classes("items-center"):
#                             ui.icon("bloodtype").classes("text-red-600 text-4xl")
#                             ui.label(f"ID: {donor_info['donor_id']}").classes("text-xs font-semibold tracking-wide text-gray-600")

#                 ui.button("Print Card", icon="print") \
#                     .classes("w-full bg-green-500 text-white hover:bg-green-600 mt-3 rounded-lg") \
#                     .on_click(lambda: ui.run_javascript("window.print();"))

#                 ui.button("Close", icon="close") \
#                     .props("outline no-caps") \
#                     .classes("w-full text-gray-600 hover:bg-gray-100") \
#                     .on_click(dialog.close)

#         dialog.open()

#     # Sidebar layout
#     with ui.column().classes("w-full bg-white shadow-xl rounded-xl p-4 space-y-4"):
#         with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white"):
#             ui.label("My Information").classes("text-xl font-semibold text-gray-800 mb-4")

#             # Blood Group Section
#             with ui.row().classes("w-full items-center space-x-4 mb-4"):
#                 ui.icon("water_drop").classes("text-4xl text-red-600")
#                 with ui.column().classes("gap-0"):
#                     ui.label("Blood Group").classes("text-sm text-gray-500")
#                     ui.label(donor_info["blood_type"]).classes("text-3xl font-bold text-red-600")

#             ui.separator().classes("my-4")

#             # Quick Actions
#             with ui.column().classes("w-full space-y-3"):
#                 ui.button("Edit Profile", icon="edit") \
#                     .props("outline no-caps") \
#                     .classes("w-full bg-red-200 text-red border-gray-300 hover:bg-red-100") \
#                     .on("click", lambda: ui.navigate.to("/donor/profile"))

#         # Availability Section
#         ui.separator().classes("my-4")
#         with ui.card().classes("w-full p-4 rounded-xl shadow-lg bg-red-50 ring-2 ring-red-100"):
#             ui.label("Update Availability").classes("text-base font-semibold text-red-700 mb-2")

#             with ui.row().classes("w-full items-center justify-between"):
#                 # Left: Icon and status
#                 with ui.row().classes("items-center space-x-4"):
#                     with ui.card().classes("p-3 bg-white rounded-lg shadow-sm"):
#                         ui.icon("favorite", size="2xl").classes("text-red-600")
#                     with ui.column().classes("gap-0"):
#                         ui.label("Status").classes("text-sm text-gray-500")
#                         availability_status_text(donor_info["is_available"])

#                 # Right: The Switch
#                 ui.switch(value=donor_info["is_available"], on_change=handle_availability_toggle) \
#                     .props('color="red" size="lg"')

#         # Donor Card Button
#         with ui.column().classes("w-full space-y-3 mt-4"):
#             ui.button("View My Donor Card", icon="medical_services") \
#                 .props("flat no-caps") \
#                 .classes("w-full text-gray bg-red-100 hover:bg-red-200") \
#                 .on_click(show_donor_card)
