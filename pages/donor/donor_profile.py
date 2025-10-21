from nicegui import ui, client
import requests
import os
from utils.api import base_url
from components.donor_sidebar import donor_sidebar
from components.donor_header import donor_header
from pages.donor.donor_dashboard import footer

# Extend JavaScript timeout (prevents TimeoutError)
client.Client.JAVASCRIPT_TIMEOUT = 10.0

API_PROFILE_GET = f"{base_url}/donors/me"
API_PROFILE_UPDATE = f"{base_url}/donors/me/profile"

# Define local assets folder path
ASSETS_PATH = os.path.join("assets", "profile_pics")


@ui.page("/donor/profile")
def donor_profile_page():
    """Donor Profile Page — loads profile image from local assets folder if available."""

    # ---------- HEAD + STYLE ----------
    ui.add_head_html('''
        <script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>
        <style>
            .success-overlay {
                position: fixed;
                top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(255, 255, 255, 0.8);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 9999;
                animation: fadeOut 2.5s ease forwards;
            }
            .checkmark-circle {
                width: 90px;
                height: 90px;
                border-radius: 50%;
                background-color: #22c55e;
                display: flex;
                align-items: center;
                justify-content: center;
                animation: scaleIn 0.4s ease-out;
            }
            .checkmark {
                font-size: 40px;
                color: white;
                transform: scale(0);
                animation: scaleIn 0.5s ease-out forwards 0.2s;
            }
            .success-text {
                margin-top: 15px;
                font-size: 18px;
                font-weight: 600;
                color: #166534;
                animation: fadeIn 0.8s ease-in-out;
            }
            @keyframes fadeOut {
                0% {opacity: 1;}
                80% {opacity: 1;}
                100% {opacity: 0; visibility: hidden;}
            }
            @keyframes scaleIn {
                0% {transform: scale(0);}
                100% {transform: scale(1);}
            }
            @keyframes fadeIn {
                from {opacity: 0;}
                to {opacity: 1;}
            }
        </style>
    ''')

    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")

    # ---------- HEADER + SIDEBAR ----------
    with ui.header(elevated=True).classes('bg-white dark:bg-gray-800 text-black dark:text-white'):
        donor_header()
    with ui.left_drawer(bordered=True).classes('bg-gray-100 dark:bg-gray-900'):
        donor_sidebar()

    donor_profile = {}

    # ---------- LOADING SPINNER ----------
    spinner_card = ui.card().classes(
        "absolute inset-0 flex flex-col items-center justify-center bg-white/80 z-50 backdrop-blur-sm"
    )
    ui.spinner(size="lg", color="red").classes("mb-4")
    ui.label("Loading profile information...").classes("text-gray-600 text-sm font-medium")

    # ---------- FETCH PROFILE ----------
    def fetch_profile():
        try:
            res = requests.get(API_PROFILE_GET, timeout=10)
            if res.status_code == 200:
                return res.json()
            else:
                ui.notify("Failed to load profile", color="red")
        except Exception as e:
            print("Error fetching profile:", e)
            ui.notify("Unable to connect to server", color="red")
        return {}

    donor_profile.update(fetch_profile())
    spinner_card.delete()

    # ---------- SUCCESS CHECKMARK ----------
    def show_success_checkmark():
        with ui.element("div").classes("success-overlay") as overlay:
            with ui.element("div").classes("checkmark-circle"):
                ui.icon("check", size="40px").classes("checkmark")
            ui.label("Profile Updated!").classes("success-text")
        ui.timer(2.5, lambda: overlay.delete(), once=True)

    # ---------- REFRESH PROFILE UI ----------
    def refresh_profile_ui():
        name_input.value = donor_profile.get("full_name", "-") or "-"
        phone_input.value = donor_profile.get("phone_number", "-") or "-"
        email_input.value = donor_profile.get("email", "-") or "-"
        location_input.value = donor_profile.get("location", "-") or "-"
        blood_input.value = donor_profile.get("blood_type", "-") or "-"
        status_input.value = donor_profile.get("availability_status", "-") or "-"


    # ---------- EDIT MODAL ----------
    with ui.dialog() as edit_modal, ui.card().classes("w-full max-w-2xl p-6"):
        ui.label("Edit Profile").classes("text-xl font-bold mb-4 text-gray-800")

        with ui.column().classes("gap-4 w-full"):
            name_edit = ui.input(label="Full Name", value=donor_profile.get("full_name", "")).props("outlined dense")
            phone_edit = ui.input(label="Phone Number", value=donor_profile.get("phone_number", "")).props("outlined dense")
            email_edit = ui.input(label="Email", value=donor_profile.get("email", "")).props("outlined dense")
            location_edit = ui.input(label="Location", value=donor_profile.get("location", "")).props("outlined dense")
            blood_edit = ui.select(
                ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"],
                label="Blood Type",
                value=donor_profile.get("blood_type", "O+"),
            ).props("outlined dense")
            status_edit = ui.select(
                ["Available", "Unavailable"],
                label="Availability Status",
                value=donor_profile.get("availability_status", "Available"),
            ).props("outlined dense")

        # ---- UPDATE PROFILE ----
        def update_profile():
            payload = {
                "full_name": name_edit.value,
                "phone_number": phone_edit.value,
                "email": email_edit.value,
                "location": location_edit.value,
                "blood_type": blood_edit.value,
                "availability_status": status_edit.value,
            }

            try:
                res = requests.put(API_PROFILE_UPDATE, json=payload, timeout=15)
                if res.status_code in (200, 201):
                    updated_data = res.json()
                    donor_profile.update(updated_data)
                    refresh_profile_ui()
                    ui.notify("Profile updated successfully!", color="green")
                    show_success_checkmark()
                    edit_modal.close()
                else:
                    ui.notify("Failed to update profile", color="red")
            except Exception as e:
                print("Error updating profile:", e)
                ui.notify("Error connecting to backend", color="red")

        with ui.row().classes("justify-end w-full mt-4"):
            ui.button("Cancel", on_click=edit_modal.close).props("outline").classes("text-gray-600")
            ui.button("Save Changes", on_click=update_profile).classes("bg-red-600 text-white")

    # ---------- MAIN PROFILE UI ----------
    with ui.column().classes("flex-grow w-full p-6 bg-gray-50 min-h-screen"):
        with ui.row().classes("items-center justify-between mb-4 w-full"):
            ui.label("My Profile").classes("text-3xl font-bold text-gray-800")
            ui.button("Edit Profile", icon="edit", on_click=edit_modal.open).props("flat no-caps").classes(
                "text-red-600 hover:bg-red-100"
            )

        with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white mb-6"):
            with ui.row().classes("items-center gap-4"):
                ui.image('assets\donor_profile.png').classes("w-20 h-20 rounded-full object-cover border-2 border-red-600")
                ui.label(donor_profile.get("full_name") or "Donor Name").classes("text-xl font-semibold text-gray-800")

        with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white"):
            ui.label("Profile Information").classes("text-xl font-semibold text-gray-800 mb-4 border-b pb-2")
            with ui.row().classes("grid grid-cols-1 md:grid-cols-2 gap-4 w-full mt-4"):
                with ui.column():
                    ui.label("Full Name").classes("text-xs font-medium text-gray-500")
                    name_input = ui.input().props("outlined dense readonly")
                with ui.column():
                    ui.label("Phone Number").classes("text-xs font-medium text-gray-500")
                    phone_input = ui.input().props("outlined dense readonly")
                with ui.column():
                    ui.label("Email Address").classes("text-xs font-medium text-gray-500")
                    email_input = ui.input().props("outlined dense readonly")
                with ui.column():
                    ui.label("Location").classes("text-xs font-medium text-gray-500")
                    location_input = ui.input().props("outlined dense readonly")
                with ui.column():
                    ui.label("Blood Type").classes("text-xs font-medium text-gray-500")
                    blood_input = ui.input().props("outlined dense readonly")
                with ui.column():
                    ui.label("Availability Status").classes("text-xs font-medium text-gray-500")
                    status_input = ui.input().props("outlined dense readonly")

    refresh_profile_ui()

    footer()
