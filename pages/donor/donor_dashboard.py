from nicegui import ui, app, run
import requests
from utils.api import base_url
from components.donor_header import donor_header


# ---------------- FOOTER ----------------
def footer():
    with ui.row().classes(
        "flex flex-col md:flex-row items-center justify-between px-7 w-full bg-gray-50 py-5 text-sm mt-auto text-gray-500"
    ):
        ui.label("© 2025 LifeLink. All rights reserved.").classes(
            "mb-3 md:mb-0 text-xl hover:text-red"
        )
        with ui.row().classes("gap-3"):
            ui.link("About", "/about").classes(
                "no-underline text-gray-700 hover:text-red transition text-xl"
            )
            ui.link("Contact", "/about#contact").classes(
                "no-underline hover:text-red text-gray-700 text-xl transition"
            )
            ui.link("Privacy Policy").classes(
                "no-underline text-gray-700 hover:text-red transition text-xl"
            )
        with ui.row().classes("gap-6"):
            ui.html(
                '<i class="fa-brands fa-square-linkedin text-xl hover:text-red-600 transition"></i>',
                sanitize=False,
            )
            ui.html(
                '<i class="fa-brands fa-instagram text-xl hover:text-red-600 transition"></i>',
                sanitize=False,
            )
            ui.html(
                '<i class="fa-brands fa-facebook text-xl hover:text-red-600 transition"></i>',
                sanitize=False,
            )


# ---------------- DONATION HISTORY ----------------
def donation_history_section():
    """Render donation history section with backend integration."""

    COLUMNS = [
        {"name": "id", "label": "ID", "field": "id", "align": "left"},
        {
            "name": "donation_date",
            "label": "DATE",
            "field": "donation_date",
            "align": "left",
        },
        {"name": "location", "label": "LOCATION", "field": "location", "align": "left"},
        {
            "name": "recipient_info",
            "label": "RECIPIENT INFO",
            "field": "recipient_info",
            "align": "left",
        },
        {"name": "status", "label": "STATUS", "field": "status", "align": "center"},
    ]

    view_mode = ui.label("table").props("hidden")
    history_container = ui.column().classes("w-full mt-4")

    async def fetch_donation_history():
        """Fetch donation history from backend."""
        token = app.storage.user.get("access_token")
        if not token:
            ui.notify("Please login to view donation history", type="warning")
            return []

        try:
            # Show loading state
            with history_container:
                ui.spinner("dots").classes("text-red-600")
                ui.label("Fetching donation history...").classes("text-gray-500")

            def make_request():
                return requests.get(
                    f"{base_url}/donors/me/history",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Accept": "application/json",
                    },
                )

            response = await run.io_bound(make_request)

            if response.status_code == 200:
                data = response.json()
                # Handle both single object and array responses
                if not isinstance(data, list):
                    data = [data]

                formatted_data = []
                for item in data:
                    formatted_data.append(
                        {
                            "id": item.get("id") or item.get("_id"),
                            "donation_date": item.get("donation_date"),
                            "location": item.get("location", "N/A"),
                            "recipient_info": item.get(
                                "recipient_info", "Not specified"
                            ),
                            "status": item.get("status", "Pending"),
                        }
                    )
                return formatted_data

            elif response.status_code == 401:
                ui.notify("Session expired. Please login again", type="warning")
                ui.navigate.to("/donor/login")
                return []
            else:
                ui.notify(
                    f"Failed to fetch donation history: {response.status_code}",
                    type="negative",
                )
                return []

        except Exception as e:
            print(f"Error fetching donation history: {str(e)}")
            ui.notify(f"Error: {str(e)}", type="negative")
            return []
        finally:
            # Clear loading state
            history_container.clear()

    def render_list_view(donations):
        """Render table with actual donation data."""
        with history_container:
            if not donations:
                ui.label("No donation history available").classes(
                    "text-gray-500 italic text-center py-8 w-full"
                )
                return

            ui.table(columns=COLUMNS, rows=donations, row_key="id").props(
                "flat bordered dense"
            ).classes("w-full rounded-lg overflow-hidden")

    def render_grid_view(donations):
        """Render grid view with donation cards."""
        with history_container:
            if not donations:
                ui.label("No donation history available").classes(
                    "text-gray-500 italic text-center py-8 w-full"
                )
                return

            with ui.grid(columns=3).classes("gap-4 w-full"):
                for donation in donations:
                    with ui.card().classes("p-4"):
                        ui.label(f"Date: {donation['donation_date']}").classes(
                            "font-bold"
                        )
                        ui.label(f"Location: {donation['location']}")
                        ui.label(f"Recipient: {donation['recipient_info']}")
                        with ui.badge().classes(
                            "bg-green-100 text-green-800"
                            if donation["status"] == "Completed"
                            else "bg-yellow-100 text-yellow-800"
                        ):
                            ui.label(donation["status"])

    async def update_history_view():
        history_container.clear()
        donations = await fetch_donation_history()
        if view_mode.text == "table":
            render_list_view(donations)
        else:
            render_grid_view(donations)

    def toggle_view(mode):
        view_mode.set_text(mode)
        update_icons()
        ui.timer(0.1, update_history_view, once=True)

    def update_icons():
        if view_mode.text == "table":
            list_btn.props("flat color=red")
            grid_btn.props("flat color=gray")
        else:
            list_btn.props("flat color=gray")
            grid_btn.props("flat color=red")

    # Layout
    with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white mt-6"):
        with ui.row().classes("w-full justify-between items-center mb-4 border-b pb-4"):
            ui.label("Donation History").classes("text-xl font-semibold text-gray-800")
            with ui.row().classes("items-center gap-2"):
                list_btn = ui.button(
                    icon="fa-solid fa-list", on_click=lambda: toggle_view("table")
                ).props("flat round dense")
                grid_btn = ui.button(
                    icon="fa-solid fa-grip", on_click=lambda: toggle_view("grid")
                ).props("flat round dense")
                update_icons()

        # Initial load
        ui.timer(0.1, update_history_view, once=True)


# ---------------- DASHBOARD PAGE ----------------
@ui.page("/donor/dashboard")
def donor_dashboard_page():
    """Frontend-only donor dashboard with sidebar, header, and footer."""
    ui.add_head_html(
        '<script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>'
    )
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")

    # Layout container
    with ui.row().classes("min-h-screen w-full bg-gray-50 overflow-hidden"):
        # # Fixed Sidebar
        # with ui.element("div").classes(
        #     "fixed left-0 top-0 bottom-0 w-64 bg-white border-r border-gray-200 hidden md:flex"
        # ):
        #     donor_sidebar()

        # Main content area
        with ui.column().classes(
            "flex-1 ml-0 w-full min-h-screen overflow-auto"
        ):
            # Header
            with ui.element().classes(
                "w-full bg-white dark:text-white shadow-md px-6 py-3 flex justify-between items-center sticky top-0 z-50"
            ):
                donor_header()

            # Dashboard Body
            with ui.column().classes("p-6  items-center w-full md:px-[10%]"):
                ui.label(" Welcome to your Donor Dashboard").classes(
                    "text-4xl font-extrabold text-gray-900 mb-4 text-center"
                )
                ui.label(
                    "Track your blood donation activity and responses here."
                ).classes("text-lg text-gray-600 mb-8 text-center")

                # Donation History Table / Grid Placeholder
                donation_history_section()

            # Footer
            footer()
