from nicegui import ui, app, run
from utils.api import base_url
import requests

app.add_static_files("/assets", "assets")


_broadcast_btn: ui.button = None


def _run_broadcast(data, token):
    """Handles the actual POST request to the backend."""
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return requests.post(f"{base_url}/requests", data=data, headers=headers)


async def _broadcast(data):
    """Async handler for the broadcast process."""
    _broadcast_btn.props(add="disable loading")

    token = app.storage.user.get("access_token")
    if not token:
        ui.notify("You must be logged in to broadcast a request!", type="warning")
        _broadcast_btn.props(remove="disable loading")
        return

    response = await run.cpu_bound(_run_broadcast, data, token)
    print(response.status_code, response.content)

    _broadcast_btn.props(remove="disable loading")

    if response.status_code in [200, 201]:
        ui.notify("Blood request broadcasted successfully!", color="positive")
        return ui.navigate.to("/hospital/dashboard")
    elif response.status_code == 401:
        ui.notify("Unauthorized! Please log in again.", type="warning")
        return ui.navigate.to("/hospital/login")
    else:
        ui.notify("Failed to broadcast blood request!", type="warning")


@ui.page("/hospital/dashboard")
def hospital_dashboard_page():
    global _broadcast_btn
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")
    with ui.element("main").classes("min-h-screen w-full flex flex-col"):
        # Navbar
        with ui.row().classes(
            "flex flex-col md:flex-row items-center justify-between shadow-md w-full px-3 md:px-7 py-1 border border-red-100"
        ):
            with ui.row().classes("gap-2 items-center justify-center"):
                ui.image("/assets/logo.png").classes("w-12 h-12")
                ui.link("LifeLink GH", "/").classes("no-underline text-xl font-bold text-gray-700")
            with ui.row().classes("gap-6 mt-3 md:mt-0"):
                ui.link("Dashboard", "/hospital/dashboard").classes("no-underline text-red-500 hover:text-red-500 transition")
                ui.link("Donors", "").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("Requests", "/contact").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("Education", "/education").classes("no-underline text-gray-700 hover:text-red-500 transition")
            with ui.row().classes("gap-4 items-center"):
                ui.icon("notifications").classes("text-gray-700 text-2xl cursor-pointer")
                ui.image("/assets/hero2.png").classes("w-10 h-10 rounded-full object-cover")

        # main for request and donor matches
        with ui.row().classes("flex flex-col md:flex-row justify-center gap-6 w-full px-2 py-6"):
            # Blood Request Form Card 
            with ui.card().classes("w-full md:w-1/4 p-6 bg-white shadow-md rounded-md border border-red-100"):
                ui.label("Blood Request Form").classes("text-xl font-bold text-gray-700 mb-1")

                # Blood Type selector
                with ui.element("div").classes("flex flex-col mb-1 w-full"):
                    ui.label("Blood Type").classes("text-sm text-left")
                    blood_type = ui.select(
                        ["Select Blood Type", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                        value="Select Blood Type",
                    ).props("outlined dense").classes("bg-red-50 text-xs")

                # Urgency selector
                with ui.element("div").classes("flex flex-col mb-1 w-full"):
                    ui.label("Urgency").classes("text-sm text-left")
                    ui.select(
                        ["Urgent", "Not Urgent"],
                        value="Urgent",
                    ).props("outlined dense").classes("bg-red-50 text-xs")

                # Quantity
                with ui.element("div").classes("flex flex-col mb-1 w-full"):
                    ui.label("Quantity (Units)").classes("text-sm text-left")
                    quantity = ui.input(placeholder="Enter Quantity").props("flat outlined dense").classes(
                        "bg-red-50 text-xs"
                    )

                # Patient Condition textarea
                with ui.element("div").classes("flex flex-col mb-1 w-full"):
                    ui.label("Patient Condition").classes("text-sm text-left")
                    condition = ui.textarea(placeholder="Describe Patient Condition").props("outlined").classes(
                        "bg-red-50 rounded-md text-xs"
                    )

                # Broadcast Button
                _broadcast_btn = (ui.button(
                    "Broadcast Request",on_click=lambda: _broadcast(
                                {
                                    "blood_type": blood_type.value,
                                    "quantity": quantity.value,
                                    "patient_condition": condition.value,
                                }
                            ),
                        )
                ).props("no-caps flat dense").classes(
                    "bg-red-600 text-white hover:bg-red-500 rounded-md py-2 px-4 w-full"
                )

            # Donor Matches Card
            with ui.column().classes("w-full md:w-3/5"):
                ui.label("Welcome to your Dashboard!").classes(
                    "text-2xl font-semibold text-gray-800 mb-2 text-center"
                )

                with ui.card().classes("w-full p-6 bg-white shadow-md rounded-md border border-red-100 border border-red-100"):
                    ui.label("Donor Matches").classes("text-xl font-bold text-gray-700 mb-2")

                    with ui.row().classes("grid grid-cols-1 md:grid-cols-5 gap-4 w-full"):
                        with ui.element("div").classes("flex flex-col col-span-3"):
                            ui.label("Search").classes("text-sm text-left")
                            ui.input(placeholder="🔍 Search donors by name, location").props(
                                "flat outlined dense"
                            ).classes("bg-red-50 text-xs rounded-md")

                        with ui.element("div").classes("flex flex-col col-span-1"):
                            ui.label("Blood Type").classes("text-sm text-left")
                            ui.select(
                                ["All", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                                value="All",
                            ).props("outlined dense").classes("bg-red-50 text-xs rounded-md")

                        with ui.element("div").classes("flex flex-col col-span-1"):
                            ui.label("Distance").classes("text-sm text-left")
                            ui.input(placeholder="Enter distance (km)").props("flat outlined dense").classes(
                                "bg-red-50 text-xs rounded-md"
                            )

                    with ui.row().classes(
                        "grid grid-cols-5 gap-4 w-full bg-red-50 text-gray-700 font-semibold text-sm mt-3 p-2"
                    ):
                        ui.label("DONOR NAME").classes("text-center")
                        ui.label("BLOOD TYPE").classes("text-center")
                        ui.label("DISTANCE").classes("text-center")
                        ui.label("AVAILABILITY").classes("text-center")
                        ui.label("CONTACT").classes("text-center")

        # Map 
        with ui.row().classes("flex flex-col md:flex-row justify-center gap-6 w-full px-4 py-6"):
            with ui.card().classes("w-full md:w-1/4 p-6 bg-white shadow-md rounded-md border border-red-100"):
                ui.label("Nearby Donors").classes("text-xl font-bold text-gray-700 mb-2")
                ui.html(
                    """
                    <iframe
                        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3915.40477804116!2d-0.195!3d5.55!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2z5L2c5ZOB5aSn!5e0!3m2!1sen!2sgh!4v1633871595096!5m2!1sen!2sgh"
                        width="100%" height="200" style="border:0; border-radius: 12px;" allowfullscreen=""
                        loading="lazy"
                    ></iframe>
                    """,
                    sanitize=False,
                ).classes("w-full h-50 rounded-md overflow-hidden")
            
            # Request history 
            with ui.card().classes("w-full md:w-3/5 p-6 bg-white shadow-md rounded-md border border-red-100"):
                ui.label("Request History").classes("text-xl font-bold text-gray-700 mb-2")

                # Header row
                with ui.row().classes(
                    "grid grid-cols-5 gap-2 w-full bg-red-50 text-gray-800 font-semibold rounded-md px-2 py-2 text-sm"
                ):
                    ui.label("REQUEST ID").classes("text-center")
                    ui.label("BLOOD TYPE").classes("text-center")
                    ui.label("QUANTITY").classes("text-center")
                    ui.label("STATUS").classes("text-center")
                    ui.label("DATE").classes("text-center")

                # Container for request rows
                request_table = ui.column().classes("w-full")

                async def load_requests():
                    """Fetch all blood requests from backend and display them."""
                    token = app.storage.user.get("access_token")
                    if not token:
                        ui.notify("You must be logged in to view request history!", type="warning")
                        return

                    try:
                        response = await run.io_bound(
                            lambda: requests.get(
                                f"{base_url}/requests/all",
                                headers={"Authorization": f"Bearer {token}"}
                            )
                        )

                        if response.status_code == 200:
                            result = response.json()
                            # print("Backend response:", result)

                            # Extract 'data' key from response
                            data = result.get("data", [])

                            # Sort by date (newest first)
                            data = sorted(data, key=lambda x: x.get("request_date", ""), reverse=True)

                            # Clear old entries before loading new ones
                            request_table.clear()

                            for req in data:
                                with request_table:
                                    with ui.row().classes(
                                        "grid grid-cols-5 gap-2 w-full border-b border-gray-100 text-sm py-1"
                                    ):
                                        req_id = str(req.get("id", "N/A"))
                                        short_id = req_id[-6:]  # show only the last 6 chars

                                        # Make the ID clickable to navigate to details page
                                        ui.link(
                                            short_id,
                                            f"/hospital/request/{req_id}","hospital/dashboard/request_details"
                                        ).classes("text-center text-red-600 no-underline hover:text-red-800")

                                        ui.label(req.get("blood_type", "N/A")).classes("text-center")
                                        ui.label(str(req.get("quantity", "N/A"))).classes("text-center")

                                        # Color-coded status
                                        status = req.get("status", "Pending").capitalize()
                                        status_color = (
                                            "bg-green-50 rounded-full"  if status == "Fulfilled"
                                            else "bg-yellow-50 rounded-full" if status == "Active"
                                            else "text-gray-500"
                                        )
                                        ui.label(status).classes(f"text-center font-medium {status_color}")

                                        # Format date
                                        date_str = req.get("request_date")
                                        if date_str:
                                            from datetime import datetime
                                            try:
                                                date_obj = datetime.fromisoformat(date_str.replace("Z", ""))
                                                date_str = date_obj.strftime("%Y-%m-%d %H:%M")
                                            except Exception:
                                                pass
                                        ui.label(date_str or "N/A").classes("text-center")

                        else:
                            ui.notify(f"Failed to load requests: {response.status_code}", type="warning")

                    except Exception as e:
                        ui.notify(f"Error fetching requests: {e}", type="negative")

                # Fetch once when dashboard loads
                ui.timer(0.5, load_requests, once=True)


        # Footer
        with ui.row().classes(
            "flex flex-col md:flex-row items-center justify-between px-7 w-full bg-gray-50 py-5 text-sm text-gray-700 mt-auto"
        ):
            ui.label("© 2025 LifeLink. All rights reserved.").classes("mb-3 md:mb-0")
            with ui.row().classes("gap-6"):
                ui.link("About").classes("no-underline text-gray-700 transition")
                ui.link("Contact").classes("no-underline hover:text-white text-gray-700 transition")
                ui.link("Privacy Policy").classes("no-underline text-gray-700 transition")
