from nicegui import ui, app, run
from utils.api import base_url
import requests
import json

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
        ui.notify("Session expired. Redirecting to login...", type="warning")
        return ui.open("/hospital/login")
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
                ui.link("LifeLink GH", "/").classes(
                    "no-underline text-xl font-bold text-gray-700"
                )
            with ui.row().classes("gap-6 mt-3 md:mt-0"):
                ui.link("Dashboard", "/hospital/dashboard").classes(
                    "no-underline text-red-500 hover:text-red-500 transition"
                )
                ui.link("Donors", "/hospital/dashboard#donors").classes(
                    "no-underline text-gray-700 hover:text-red-500 transition"
                )
                ui.link("Requests", "/hospital/dashboard#request").classes(
                    "no-underline text-gray-700 hover:text-red-500 transition"
                )
                ui.link("Education", "/education").classes(
                    "no-underline text-gray-700 hover:text-red-500 transition"
                )
            with ui.row().classes("gap-4 items-center"):
                # Notification bell and count
                notification_count = ui.label("0").classes(
                    "text-sm text-red-500 hidden"
                )
                notification_bell = ui.icon("notifications").classes(
                    "text-gray-700 text-2xl cursor-pointer"
                )

                async def update_notifications():
                    # Simulate fetching notification count from backend
                    count = app.storage.user.get("notification_count", 0)
                    notification_count.set_text(str(count))
                    if count > 0:
                        notification_count.classes(remove="hidden")
                        # Simulate beep sound
                        print("Beep! New notification.")
                    else:
                        notification_count.classes(add="hidden")

                # Periodically check for new notifications
                ui.timer(5, update_notifications)

                with ui.image("/assets/hero2.png").classes(
                    "w-10 h-10 rounded-full object-cover cursor-pointer"
                ):
                    with ui.menu():
                        ui.menu_item("View Profile")
                        ui.menu_item("Settings")
                        ui.menu_item("Help")
                        ui.menu_item("Logout", on_click=lambda: logout_modal.open())

        # main for request and donor matches
        with ui.row().classes(
            "flex flex-col md:flex-row justify-center gap-6 w-full px-2 py-6"
        ):
            # Blood Request Form Card
            with ui.card().classes(
                "w-full md:w-1/4 p-6 bg-white shadow-md rounded-md border border-red-100"
            ):
                ui.label("Blood Request Form").classes(
                    "text-xl font-bold text-gray-700 mb-1"
                )

                # Blood Type selector
                with ui.element("div").classes("flex flex-col mb-1 w-full"):
                    ui.label("Blood Type").classes("text-sm text-left")
                    blood_type = (
                        ui.select(
                            [
                                "Select Blood Type",
                                "A+",
                                "A-",
                                "B+",
                                "B-",
                                "AB+",
                                "AB-",
                                "O+",
                                "O-",
                            ],
                            value="Select Blood Type",
                        )
                        .props("outlined dense color=red-100")
                        .classes("bg-red-50 text-xs")
                    )

                # Urgency selector
                with ui.element("div").classes("flex flex-col mb-1 w-full"):
                    ui.label("Urgency").classes("text-sm text-left")
                    ui.select(
                        ["Urgent", "Not Urgent"],
                        value="Urgent",
                    ).props("outlined dense color=red-100").classes("bg-red-50 text-xs")

                # Quantity
                with ui.element("div").classes("flex flex-col mb-1 w-full"):
                    ui.label("Quantity (Units)").classes("text-sm text-left")
                    quantity = (
                        ui.input(placeholder="Enter Quantity")
                        .props("flat outlined dense color=red-100")
                        .classes("bg-red-50 text-xs")
                    )

                # Patient Condition textarea
                with ui.element("div").classes("flex flex-col mb-1 w-full"):
                    ui.label("Patient Condition").classes("text-sm text-left")
                    condition = (
                        ui.textarea(placeholder="Describe Patient Condition")
                        .props("outlined color=red-100")
                        .classes("bg-red-50 rounded-md text-xs")
                    )

                # Broadcast Button
                _broadcast_btn = (
                    (
                        ui.button(
                            "Broadcast Request",
                            on_click=lambda: _broadcast(
                                {
                                    "blood_type": blood_type.value,
                                    "quantity": quantity.value,
                                    "patient_condition": condition.value,
                                }
                            ),
                        )
                    )
                    .props("no-caps flat dense")
                    .classes(
                        "bg-red-600 text-white hover:bg-red-500 rounded-md py-2 px-4 w-full"
                    )
                )

            # Donor Matches Card
            with ui.column().classes("w-full md:w-[65%]"):
                # Welcome label and hospital name
                with ui.row().classes("items-center justify-center gap-3"):
                    ui.label("Welcome to your Dashboard!").classes(
                        "text-2xl font-semibold text-gray-800 mb-2 text-center"
                    )
                    hospital_name_label = ui.label("").classes(
                        "text-lg font-semibold text-gray-600 mb-2 text-center"
                    )

                with (
                    ui.card()
                    .props("id=donors")
                    .classes(
                        "w-full p-6 bg-white shadow-md rounded-md border border-red-100"
                    )
                ):
                    ui.label("Donor Matches").classes(
                        "text-xl font-bold text-gray-700 mb-2"
                    )

                    # Search filters
                    with ui.row().classes(
                        "grid grid-cols-1 md:grid-cols-5 gap-4 w-full items-end"
                    ):
                        with ui.element("div").classes("flex flex-col col-span-2"):
                            ui.label("Search").classes("text-sm text-left")
                            dm_search = (
                                ui.input(placeholder="🔍 Enter hospital location")
                                .props("flat outlined dense")
                                .classes("bg-red-50 text-xs rounded-md")
                            )

                        with ui.element("div").classes("flex flex-col col-span-1"):
                            ui.label("Blood Type").classes("text-sm text-left")
                            dm_blood = (
                                ui.select(
                                    [
                                        "All",
                                        "A+",
                                        "A-",
                                        "B+",
                                        "B-",
                                        "AB+",
                                        "AB-",
                                        "O+",
                                        "O-",
                                    ],
                                    value="All",
                                )
                                .props("outlined dense")
                                .classes("bg-red-50 text-xs rounded-md")
                            )

                        with ui.element("div").classes("flex flex-col col-span-1"):
                            ui.label("Distance (km)").classes("text-sm text-left")
                            dm_distance = (
                                ui.input(placeholder="10")
                                .props("flat outlined dense")
                                .classes("bg-red-50 text-xs rounded-md")
                            )

                        # Search button (aligned at the bottom)
                        with ui.element("div").classes(
                            "flex flex-col col-span-1 justify-end"
                        ):
                            search_btn = (
                                ui.button(
                                    "Search", on_click=lambda e: load_donor_matches()
                                )
                                .props("color=red unelevated")
                                .classes("text-xs font-semibold w-full")
                            )

                    # Header row
                    with ui.row().classes(
                        "grid grid-cols-6 gap-4 w-full bg-red-50 text-gray-700 font-semibold mt-3 p-2"
                    ):
                        ui.label("DONOR NAME").classes("text-left")
                        ui.label("BLOOD TYPE").classes("text-left")
                        ui.label("LOCATION").classes("text-left")
                        ui.label("DISTANCE").classes("text-left")
                        ui.label("AVAILABILITY").classes("text-left")
                        ui.label("CONTACT").classes("text-left")

                    # Donor table container
                    donor_table = ui.column().classes("w-full")

                    async def load_donor_matches():
                        token = app.storage.user.get("access_token")

                        params = {}
                        blood_type = dm_blood.value if dm_blood.value != "All" else None
                        if blood_type:
                            params["blood_type"] = blood_type

                        location_name = dm_search.value
                        params["location_name"] = location_name

                        print(f"This is the location name:{location_name}")

                        try:
                            radius = float(dm_distance.value or 10)
                        except Exception:
                            radius = 10
                        params["radius"] = radius

                        print(f"This is the parameters: {params}")

                        headers = {"Authorization": f"Bearer {token}"} if token else {}

                        try:
                            resp = await run.io_bound(
                                lambda: requests.get(
                                    f"{base_url}/donors/search",
                                    params=params,
                                    headers=headers,
                                )
                            )
                            print(f"Response: {resp.status_code, resp.content}")
                        except Exception as ex:
                            ui.notify(f"Failed to search donors: {ex}", type="negative")
                            return

                        if resp.status_code != 200:
                            try:
                                err = resp.json()
                            except Exception:
                                err = resp.text
                            # ui.notify(f"Failed to search donors: {resp.status_code} - {err}", type="warning")
                            # print("Donor search error", resp.status_code, err)
                            # return

                        try:
                            donors = resp.content
                            print(f"Donors2: {donors}")
                        except Exception:
                            donors = []

                        try:
                            donors_data = json.loads(donors)
                            donors_list = donors_data.get("donors", [])
                            message = donors_data.get("message", "")
                            print(f"Message: {message}")
                        except json.JSONDecodeError as e:
                            ui.notify(
                                f"Failed to parse donor data: {e}", type="negative"
                            )
                            return

                        donor_table.clear()

                        for d in donors_list:
                            print(f"Donor: {d}")
                            if not isinstance(d, dict):
                                continue

                            full = d.get("full_name") or "N/A"
                            phone = d.get("phone_number") or "N/A"
                            blood = d.get("blood_type") or "N/A"
                            distance_val = d.get("distance_km")
                            distance_str = (
                                f"{distance_val} km"
                                if distance_val is not None
                                else "N/A"
                            )
                            location = d.get("location_details") or "N/A"
                            availability = d.get("Availability", "Unknown")

                            with donor_table:
                                with ui.row().classes(
                                    "grid grid-cols-6 gap-4 w-full text-gray-700  mt-3 p-2"
                                ):
                                    ui.label(full).classes("text-left text-sm")
                                    ui.label(blood).classes("text-left text-sm")
                                    ui.label(location).classes("text-left text-sm")
                                    ui.label(distance_str).classes("text-left text-sm")
                                    ui.label(availability).classes("text-left text-sm")
                                    ui.label(phone).classes("text-left text-sm")

                    # Auto load donors on page load
                    ui.timer(0.5, load_donor_matches, once=True)

        # Map
        with ui.row().classes(
            "flex flex-col md:flex-row justify-center gap-6 w-full px-4 py-6"
        ):
            with ui.card().classes(
                "w-full md:w-1/4 p-6 bg-white shadow-md rounded-md border border-red-100"
            ):
                ui.label("Nearby Donors").classes(
                    "text-xl font-bold text-gray-700 mb-2"
                )
                # container that will hold the map iframe; we'll replace its contents when we have hospital location
                hospital_map = ui.column().classes(
                    "w-full h-50 rounded-md overflow-hidden"
                )
                with hospital_map:
                    ui.html(
                        """
                        <iframe
                            src="https://www.google.com/maps?q=Accra,+Ghana&output=embed"
                            width="100%" height="200" style="border:0; border-radius: 12px;" allowfullscreen=""
                            loading="lazy"
                        ></iframe>
                        """,
                        sanitize=False,
                    ).classes("w-full h-50 rounded-md overflow-hidden")

            # Request history
            with (
                ui.card()
                .props("id=request")
                .classes(
                    "w-full md:w-[65%] p-6 bg-white shadow-md rounded-md border border-red-100"
                )
            ):
                ui.label("Request History").classes(
                    "text-xl font-bold text-gray-700 mb-2"
                )

                # Header row
                with ui.row().classes(
                    "grid grid-cols-5 gap-1 w-full bg-red-50 text-gray-800 font-semibold rounded-md px-2 py-2 text-sm"
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
                        ui.notify(
                            "You must be logged in to view request history!",
                            type="warning",
                        )
                        return

                    try:
                        response = await run.io_bound(
                            lambda: requests.get(
                                f"{base_url}/requests/all",
                                headers={"Authorization": f"Bearer {token}"},
                            )
                        )

                        if response.status_code == 200:
                            result = response.json()
                            # print("Backend response:", result)

                            # Extract 'data' key from response
                            data = result.get("data", [])

                            # Attempt to determine current hospital id so we can filter requests
                            hospital_id = app.storage.user.get("hospital_id")
                            if not hospital_id:
                                # Try to decode hospital id from JWT access token payload (best-effort)
                                token_payload = app.storage.user.get("access_token")
                                if token_payload:
                                    try:
                                        import base64, json

                                        parts = token_payload.split(".")
                                        if len(parts) >= 2:
                                            payload_b64 = parts[1]
                                            # add padding
                                            padding = "=" * (-len(payload_b64) % 4)
                                            payload_b64 += padding
                                            decoded = base64.urlsafe_b64decode(
                                                payload_b64.encode()
                                            ).decode()
                                            payload_json = json.loads(decoded)
                                            # common keys that might contain the hospital id
                                            for key in (
                                                "hospital_id",
                                                "hospitalId",
                                                "hospital",
                                                "id",
                                                "sub",
                                                "user_id",
                                                "userId",
                                            ):
                                                if key in payload_json:
                                                    maybe = payload_json.get(key)
                                                    if (
                                                        isinstance(maybe, dict)
                                                        and "id" in maybe
                                                    ):
                                                        hospital_id = maybe.get("id")
                                                    else:
                                                        hospital_id = maybe
                                                    break
                                    except Exception:
                                        hospital_id = None

                            # If we resolved a hospital_id, filter the data client-side so only this hospital's
                            # requests are displayed. Requests may store hospital id under different keys or
                            # as a nested 'hospital' object, so check a few possibilities.
                            if hospital_id:

                                def _req_hospital_id(r):
                                    # direct keys
                                    for k in (
                                        "hospital_id",
                                        "hospitalId",
                                        "hospital_id",
                                    ):
                                        if k in r:
                                            return r.get(k)
                                    # nested object
                                    h = r.get("hospital")
                                    if isinstance(h, dict) and "id" in h:
                                        return h.get("id")
                                    # fallback
                                    return r.get("id")

                                data = [
                                    r
                                    for r in data
                                    if str(_req_hospital_id(r)) == str(hospital_id)
                                ]
                            # Sort by date (newest first)
                            data = sorted(
                                data,
                                key=lambda x: x.get("request_date", ""),
                                reverse=True,
                            )

                            # Clear old entries before loading new ones
                            request_table.clear()

                            for req in data:
                                with request_table:
                                    # keep the 5-column grid but add a hover bg on the whole row
                                    with ui.row().classes(
                                        "grid grid-cols-5 gap-2 w-full border-b border-gray-100 text-sm py-1 hover:bg-red-50 transition-colors cursor-default"
                                    ):
                                        req_id = str(req.get("id", "N/A"))
                                        short_id = req_id[
                                            -6:
                                        ]  # show only the last 6 chars

                                        # Make the ID clickable to navigate to details page
                                        ui.link(
                                            short_id,
                                            f"/hospital/request/{req_id}",
                                            "hospital/dashboard/request_details",
                                        ).classes(
                                            "text-center no-underline text-gray-900"
                                        )

                                        ui.label(req.get("blood_type", "N/A")).classes(
                                            "text-center"
                                        )
                                        ui.label(
                                            str(req.get("quantity", "N/A"))
                                        ).classes("text-center")

                                        # Color-coded status
                                        status = req.get(
                                            "status", "Pending"
                                        ).capitalize()
                                        status_color = (
                                            "bg-green-50 rounded-full"
                                            if status == "Fulfilled"
                                            else "bg-yellow-50 rounded-full"
                                            if status == "Active"
                                            else "text-gray-500"
                                        )
                                        ui.label(status).classes(
                                            f"text-center font-medium {status_color}"
                                        )

                                        # Format date and add three-dot dropdown (in same cell)
                                        date_str = req.get("request_date")
                                        if date_str:
                                            from datetime import datetime

                                            try:
                                                date_obj = datetime.fromisoformat(
                                                    date_str.replace("Z", "")
                                                )
                                                date_str = date_obj.strftime(
                                                    "%Y-%m-%d %H:%M"
                                                )
                                            except Exception:
                                                pass

                                        # Place date and menu inside the same grid cell so layout stays 5 columns
                                        # use nowrap so the three-dot doesn't wrap to the next line
                                        with ui.element("div").classes(
                                            "flex items-center justify-center whitespace-nowrap gap-2"
                                        ):
                                            ui.label(date_str or "N/A").classes(
                                                "text-center whitespace-nowrap"
                                            )

                                            with (
                                                ui.button(icon="more_vert")
                                                .props("flat dense")
                                                .classes("text-red p-0")
                                            ):
                                                with ui.menu():
                                                    # Edit request: open edit dialog and PUT to /requests/{id}
                                                    async def _on_edit(_ev=None, r=req):
                                                        token = app.storage.user.get(
                                                            "access_token"
                                                        )
                                                        dlg = ui.dialog()
                                                        with dlg:
                                                            with ui.card().classes(
                                                                "w-[90vw] md:w-[25vw] p-4"
                                                            ):
                                                                ui.label(
                                                                    "Edit Request"
                                                                ).classes(
                                                                    "text-lg font-semibold mb-1 text-center"
                                                                )
                                                                ui.label(
                                                                    "Blood Type"
                                                                ).classes(
                                                                    "text-sm text-left"
                                                                )
                                                                bt = (
                                                                    ui.select(
                                                                        [
                                                                            "A+",
                                                                            "A-",
                                                                            "B+",
                                                                            "B-",
                                                                            "AB+",
                                                                            "AB-",
                                                                            "O+",
                                                                            "O-",
                                                                        ],
                                                                        value=r.get(
                                                                            "blood_type",
                                                                            "A+",
                                                                        ),
                                                                    )
                                                                    .props(
                                                                        "outlined dense"
                                                                    )
                                                                    .classes(
                                                                        "bg-red-50 text-xs w-full"
                                                                    )
                                                                )
                                                                ui.label(
                                                                    "Quantity"
                                                                ).classes(
                                                                    "text-sm text-left"
                                                                )
                                                                qty = (
                                                                    ui.input(
                                                                        value=str(
                                                                            r.get(
                                                                                "quantity",
                                                                                "",
                                                                            )
                                                                        )
                                                                    )
                                                                    .props(
                                                                        "flat outlined dense"
                                                                    )
                                                                    .classes(
                                                                        "bg-red-50 text-xs w-full"
                                                                    )
                                                                )
                                                                ui.label(
                                                                    "Patient Condition"
                                                                ).classes(
                                                                    "text-sm text-left"
                                                                )
                                                                cond = (
                                                                    ui.textarea(
                                                                        value=r.get(
                                                                            "patient_condition",
                                                                            "",
                                                                        )
                                                                    )
                                                                    .props("outlined")
                                                                    .classes(
                                                                        "bg-red-50 text-xs w-full"
                                                                    )
                                                                )
                                                                with ui.row().classes(
                                                                    "justify-end gap-2 mt-3"
                                                                ):

                                                                    async def _submit_edit(
                                                                        _ev=None,
                                                                    ):
                                                                        # add immediate feedback
                                                                        if not token:
                                                                            ui.notify(
                                                                                "You must be logged in to edit a request",
                                                                                type="warning",
                                                                            )
                                                                            return
                                                                        save_btn.props(
                                                                            add="disable loading"
                                                                        )
                                                                        payload = {
                                                                            "blood_type_update": bt.value,
                                                                            "quantity_update": qty.value,
                                                                            "patient_condition_update": cond.value,
                                                                        }

                                                                        def _put():
                                                                            return requests.put(
                                                                                f"{base_url}/requests/{r.get('id')}",
                                                                                data=payload,
                                                                                headers={
                                                                                    "Authorization": f"Bearer {token}"
                                                                                },
                                                                            )

                                                                        try:
                                                                            resp = await run.io_bound(
                                                                                _put
                                                                            )
                                                                        except (
                                                                            Exception
                                                                        ) as ex:
                                                                            ui.notify(
                                                                                f"Network error: {ex}",
                                                                                type="negative",
                                                                            )
                                                                            save_btn.props(
                                                                                remove="disable loading"
                                                                            )
                                                                            return

                                                                        save_btn.props(
                                                                            remove="disable loading"
                                                                        )
                                                                        if (
                                                                            resp.status_code
                                                                            in (
                                                                                200,
                                                                                201,
                                                                            )
                                                                        ):
                                                                            ui.notify(
                                                                                "Request updated",
                                                                                color="positive",
                                                                            )
                                                                            dlg.close()
                                                                            await load_requests()
                                                                        elif (
                                                                            resp.status_code
                                                                            == 401
                                                                        ):
                                                                            ui.notify(
                                                                                "Session expired. Redirecting to login...",
                                                                                type="warning",
                                                                            )
                                                                            ui.open(
                                                                                "/hospital/login"
                                                                            )
                                                                        else:
                                                                            # try to surface backend message
                                                                            try:
                                                                                msg = resp.json()
                                                                            except Exception:
                                                                                msg = resp.text
                                                                            ui.notify(
                                                                                f"Failed to update: {resp.status_code} {msg}",
                                                                                type="warning",
                                                                            )

                                                                    save_btn = (
                                                                        ui.button(
                                                                            "Save",
                                                                            on_click=_submit_edit,
                                                                        )
                                                                        .props(
                                                                            "flat dense"
                                                                        )
                                                                        .classes(
                                                                            "bg-red-600 text-white"
                                                                        )
                                                                    )
                                                                    ui.button(
                                                                        "Cancel",
                                                                        on_click=lambda: dlg.close(),
                                                                    ).props(
                                                                        "flat dense"
                                                                    )
                                                        dlg.open()

                                                    ui.menu_item(
                                                        "Edit Request",
                                                        on_click=_on_edit,
                                                    ).props("icon=edit")

                                                    # Delete request: ask for confirmation then DELETE /requests/{id}
                                                    async def _on_delete(
                                                        _ev=None, r=req
                                                    ):
                                                        token = app.storage.user.get(
                                                            "access_token"
                                                        )
                                                        dlg = ui.dialog()
                                                        with dlg:
                                                            with ui.card().classes(
                                                                "p-4 w-[90vw] md:w-[30vw]"
                                                            ):
                                                                ui.label(
                                                                    "Delete Request"
                                                                ).classes(
                                                                    "text-lg font-semibold"
                                                                )
                                                                ui.label(
                                                                    "Are you sure you want to delete this request? This action cannot be undone."
                                                                ).classes(
                                                                    "text-sm text-gray-700 my-3"
                                                                )
                                                                with ui.row().classes(
                                                                    "justify-end gap-2"
                                                                ):

                                                                    async def _confirm_delete(
                                                                        _ev=None,
                                                                    ):
                                                                        if not token:
                                                                            ui.notify(
                                                                                "You must be logged in to delete a request",
                                                                                type="warning",
                                                                            )
                                                                            return
                                                                        delete_btn.props(
                                                                            add="disable loading"
                                                                        )

                                                                        def _del():
                                                                            return requests.delete(
                                                                                f"{base_url}/requests/{r.get('id')}",
                                                                                headers={
                                                                                    "Authorization": f"Bearer {token}"
                                                                                },
                                                                            )

                                                                        try:
                                                                            resp = await run.io_bound(
                                                                                _del
                                                                            )
                                                                        except (
                                                                            Exception
                                                                        ) as ex:
                                                                            ui.notify(
                                                                                f"Network error: {ex}",
                                                                                type="negative",
                                                                            )
                                                                            delete_btn.props(
                                                                                remove="disable loading"
                                                                            )
                                                                            return

                                                                        delete_btn.props(
                                                                            remove="disable loading"
                                                                        )
                                                                        if (
                                                                            resp.status_code
                                                                            in (
                                                                                200,
                                                                                204,
                                                                            )
                                                                        ):
                                                                            ui.notify(
                                                                                "Request deleted",
                                                                                color="positive",
                                                                            )
                                                                            dlg.close()
                                                                            await load_requests()
                                                                        elif (
                                                                            resp.status_code
                                                                            == 401
                                                                        ):
                                                                            ui.notify(
                                                                                "Session expired. Redirecting to login...",
                                                                                type="warning",
                                                                            )
                                                                            ui.open(
                                                                                "/hospital/login"
                                                                            )
                                                                        else:
                                                                            try:
                                                                                msg = resp.json()
                                                                            except Exception:
                                                                                msg = resp.text
                                                                            ui.notify(
                                                                                f"Failed to delete: {resp.status_code} {msg}",
                                                                                type="warning",
                                                                            )

                                                                    delete_btn = (
                                                                        ui.button(
                                                                            "Delete",
                                                                            on_click=_confirm_delete,
                                                                        )
                                                                        .props(
                                                                            "flat dense"
                                                                        )
                                                                        .classes(
                                                                            "bg-red-600 text-white"
                                                                        )
                                                                    )
                                                                    ui.button(
                                                                        "Cancel",
                                                                        on_click=lambda: dlg.close(),
                                                                    ).props(
                                                                        "flat dense"
                                                                    )
                                                        dlg.open()

                                                    ui.menu_item(
                                                        "Delete Request",
                                                        on_click=_on_delete,
                                                    ).props("icon=delete")

                                                    # Confirm donation: open responses modal where user can POST to confirm
                                                    async def _on_confirm(
                                                        _ev=None, r=req
                                                    ):
                                                        token = app.storage.user.get(
                                                            "access_token"
                                                        )
                                                        dlg = ui.dialog()
                                                        with dlg:
                                                            with ui.card().classes(
                                                                "p-4 w-[95vw] md:w-[60vw]"
                                                            ):
                                                                ui.label(
                                                                    "Responses"
                                                                ).classes(
                                                                    "text-lg font-semibold"
                                                                )
                                                                list_container = ui.column().classes(
                                                                    "max-h-60 overflow-auto my-2"
                                                                )

                                                                async def _load_responses():
                                                                    if not token:
                                                                        ui.notify(
                                                                            "You must be logged in to view responses",
                                                                            type="warning",
                                                                        )
                                                                        return
                                                                    get_btn.props(
                                                                        add="disable loading"
                                                                    )

                                                                    def _get():
                                                                        return requests.get(
                                                                            f"{base_url}/requests/{r.get('id')}/responses",
                                                                            headers={
                                                                                "Authorization": f"Bearer {token}"
                                                                            },
                                                                        )

                                                                    try:
                                                                        resp = await run.io_bound(
                                                                            _get
                                                                        )
                                                                    except (
                                                                        Exception
                                                                    ) as ex:
                                                                        ui.notify(
                                                                            f"Network error: {ex}",
                                                                            type="negative",
                                                                        )
                                                                        get_btn.props(
                                                                            remove="disable loading"
                                                                        )
                                                                        return
                                                                    get_btn.props(
                                                                        remove="disable loading"
                                                                    )
                                                                    if (
                                                                        resp.status_code
                                                                        == 200
                                                                    ):
                                                                        j = json.loads(
                                                                            resp.content.decode(
                                                                                "utf-8"
                                                                            )
                                                                        )
                                                                        print(f"j: {j}")

                                                                        for it in j:
                                                                            print(
                                                                                f"it: {it}"
                                                                            )
                                                                            with list_container:
                                                                                with ui.row().classes(
                                                                                    "items-center justify-between"
                                                                                ):
                                                                                    ui.label(
                                                                                        f"Responder ID: {it.get('request_id', 'N/A')} | Token : {it.get('confirmation_token', '')}"
                                                                                    ).classes(
                                                                                        "text-sm"
                                                                                    )

                                                                                    async def _confirm_resp(
                                                                                        _ev=None,
                                                                                    ):
                                                                                        confirm_btn.props(
                                                                                            add="disable loading"
                                                                                        )
                                                                                        confirmation_token = (
                                                                                            str(
                                                                                                token_input.value
                                                                                            ).strip()
                                                                                            if token_input.value
                                                                                            else None
                                                                                        )
                                                                                        donation_date = (
                                                                                            str(
                                                                                                date_input.value
                                                                                            ).strip()
                                                                                            if date_input.value
                                                                                            else None
                                                                                        )
                                                                                        recipient_info = (
                                                                                            recipient_input.value.strip()
                                                                                            if recipient_input.value
                                                                                            else None
                                                                                        )

                                                                                        # Debugging payload
                                                                                        print(
                                                                                            f"DEBUG: Payload={{'confirmation_token': {confirmation_token}, 'donation_date': {donation_date}, 'recipient_info': {recipient_info}}}"
                                                                                        )

                                                                                        # Validate payload
                                                                                        if (
                                                                                            not confirmation_token
                                                                                            or not donation_date
                                                                                        ):
                                                                                            ui.notify(
                                                                                                "Confirmation token and donation date are required.",
                                                                                                type="warning",
                                                                                            )
                                                                                            confirm_btn.props(
                                                                                                remove="disable loading"
                                                                                            )
                                                                                            return

                                                                                        # determine response id from the responder item
                                                                                        response_id = (
                                                                                            it.get(
                                                                                                "id"
                                                                                            )
                                                                                            or it.get(
                                                                                                "_id"
                                                                                            )
                                                                                            or it.get(
                                                                                                "response_id"
                                                                                            )
                                                                                        )
                                                                                        if not response_id:
                                                                                            ui.notify(
                                                                                                "Unable to determine response id for confirmation.",
                                                                                                type="warning",
                                                                                            )
                                                                                            confirm_btn.props(
                                                                                                remove="disable loading"
                                                                                            )
                                                                                            return

                                                                                        def _post():
                                                                                            payload = {
                                                                                                "confirmation_token": confirmation_token,
                                                                                                "donation_date": donation_date,
                                                                                                "recipient_info": recipient_info,
                                                                                            }
                                                                                            # send as form-encoded data to match the provided curl example
                                                                                            headers = {
                                                                                                "Authorization": f"Bearer {token}",
                                                                                                "Accept": "application/json",
                                                                                            }
                                                                                            return requests.post(
                                                                                                f"{base_url}/responses/{response_id}/confirm-donation",
                                                                                                headers=headers,
                                                                                                data=payload,
                                                                                            )

                                                                                        try:
                                                                                            rresp = await run.io_bound(
                                                                                                _post
                                                                                            )
                                                                                        except Exception as ex:
                                                                                            ui.notify(
                                                                                                f"Network error: {ex}",
                                                                                                type="negative",
                                                                                            )
                                                                                            confirm_btn.props(
                                                                                                remove="disable loading"
                                                                                            )
                                                                                            return

                                                                                        confirm_btn.props(
                                                                                            remove="disable loading"
                                                                                        )
                                                                                        if (
                                                                                            rresp.status_code
                                                                                            in (
                                                                                                200,
                                                                                                201,
                                                                                            )
                                                                                        ):
                                                                                            try:
                                                                                                response_data = rresp.json()
                                                                                            except Exception:
                                                                                                response_data = {}
                                                                                            message = response_data.get(
                                                                                                "message",
                                                                                                "Donation confirmed successfully.",
                                                                                            )
                                                                                            confirmation_token_resp = response_data.get(
                                                                                                "confirmation_token",
                                                                                                response_data.get(
                                                                                                    "confirmation_token_if_committed",
                                                                                                    "N/A",
                                                                                                ),
                                                                                            )
                                                                                            ui.notify(
                                                                                                f"{message}\nConfirmation Token: {confirmation_token_resp}",
                                                                                                color="positive",
                                                                                            )

                                                                                            await _load_responses()
                                                                                            await load_requests()
                                                                                        elif (
                                                                                            rresp.status_code
                                                                                            == 401
                                                                                        ):
                                                                                            ui.notify(
                                                                                                "Unauthorized. Please log in again.",
                                                                                                type="warning",
                                                                                            )
                                                                                        else:
                                                                                            try:
                                                                                                msg = rresp.json()
                                                                                            except Exception:
                                                                                                msg = rresp.text
                                                                                                print(
                                                                                                    f"DEBUG: Failed to confirm response. Status: {rresp.status_code}, Message: {msg}"
                                                                                                )
                                                                                            ui.notify(
                                                                                                f"Failed to confirm: {rresp.status_code} {msg}",
                                                                                                type="warning",
                                                                                            )

                                                                                    with list_container:
                                                                                        with ui.row().classes(
                                                                                            "items-center justify-between"
                                                                                        ):
                                                                                            ui.label(
                                                                                                f"Responder: {it.get('recipient_info', it.get('name', 'N/A'))} | Message: {it.get('message', '')}"
                                                                                            ).classes(
                                                                                                "text-sm"
                                                                                            )
                                                                                            token_input = ui.input(
                                                                                                label="Confirmation Token"
                                                                                            ).classes(
                                                                                                "w-full"
                                                                                            )
                                                                                            date_input = (
                                                                                                ui.input(
                                                                                                    label="Donation Date"
                                                                                                )
                                                                                                .props(
                                                                                                    "type=date"
                                                                                                )
                                                                                                .classes(
                                                                                                    "w-full"
                                                                                                )
                                                                                            )
                                                                                            recipient_input = ui.input(
                                                                                                label="Recipient Info (Optional)"
                                                                                            ).classes(
                                                                                                "w-full"
                                                                                            )
                                                                                            confirm_btn = (
                                                                                                ui.button(
                                                                                                    "Confirm",
                                                                                                    on_click=_confirm_resp,
                                                                                                )
                                                                                                .props(
                                                                                                    "flat dense"
                                                                                                )
                                                                                                .classes(
                                                                                                    "bg-green-600 text-white"
                                                                                                )
                                                                                            )
                                                                    else:
                                                                        ui.notify(
                                                                            f"Failed to load responses: {resp.status_code}",
                                                                            type="warning",
                                                                        )

                                                                get_btn = (
                                                                    ui.button(
                                                                        "Refresh",
                                                                        on_click=lambda: _load_responses(),
                                                                    )
                                                                    .props("flat dense")
                                                                    .classes("ml-0")
                                                                )
                                                                await _load_responses()
                                                                with ui.row().classes(
                                                                    "justify-end mt-3"
                                                                ):
                                                                    ui.button(
                                                                        "Close",
                                                                        on_click=lambda: dlg.close(),
                                                                    ).props(
                                                                        "flat dense"
                                                                    )
                                                        dlg.open()

                                                    ui.menu_item(
                                                        "Confirm Donation",
                                                        on_click=_on_confirm,
                                                    ).props("icon=check_circle")

                                                    # View responses: same as confirm but read-only view
                                                    async def _on_view(_ev=None, r=req):
                                                        token = app.storage.user.get(
                                                            "access_token"
                                                        )
                                                        dlg = ui.dialog()
                                                        with dlg:
                                                            with ui.card().classes(
                                                                "p-4 w-[95vw] md:w-[60vw]"
                                                            ):
                                                                ui.label(
                                                                    "Responses"
                                                                ).classes(
                                                                    "text-lg font-semibold"
                                                                )
                                                                list_container = ui.column().classes(
                                                                    "max-h-60 overflow-auto my-2"
                                                                )

                                                                def _get_sync():
                                                                    return requests.get(
                                                                        f"{base_url}/requests/{r.get('id')}/responses",
                                                                        headers={
                                                                            "Authorization": f"Bearer {token}"
                                                                        },
                                                                    )

                                                                resp = (
                                                                    await run.io_bound(
                                                                        _get_sync
                                                                    )
                                                                )
                                                                print(
                                                                    f"Donor_responses: {resp.content}"
                                                                )
                                                                if (
                                                                    resp.status_code
                                                                    == 200
                                                                ):
                                                                    items = json.loads(
                                                                        resp.content.decode(
                                                                            "utf-8"
                                                                        )
                                                                    )  # Decode and parse JSON content
                                                                    print(
                                                                        f"items: {items}"
                                                                    )
                                                                    for it in items:
                                                                        print(
                                                                            f"it: {it}"
                                                                        )
                                                                        with list_container:
                                                                            if not isinstance(
                                                                                it, dict
                                                                            ):
                                                                                ui.label(
                                                                                    f"Invalid responder data: {it}"
                                                                                ).classes(
                                                                                    "text-sm"
                                                                                )
                                                                                continue
                                                                            ui.label(
                                                                                f"Responder ID: {it.get('request_id', 'N/A')} | Token: {it.get('confirmation_token', 'N/A')}"
                                                                            ).classes(
                                                                                "text-sm"
                                                                            )
                                                                else:
                                                                    ui.notify(
                                                                        f"Failed to load responses: {resp.status_code}",
                                                                        type="warning",
                                                                    )

                                                                with ui.row().classes(
                                                                    "justify-end mt-3"
                                                                ):
                                                                    ui.button(
                                                                        "Close",
                                                                        on_click=lambda: dlg.close(),
                                                                    ).props(
                                                                        "flat dense"
                                                                    )
                                                        dlg.open()

                                                    ui.menu_item(
                                                        "View Responses",
                                                        on_click=_on_view,
                                                    ).props("icon=reply")

                        else:
                            ui.notify(
                                f"Failed to load requests: {response.status_code}",
                                type="warning",
                            )

                    except Exception as e:
                        ui.notify(f"Error fetching requests: {e}", type="negative")

                # Fetch once when dashboard loads
                ui.timer(0.5, load_requests, once=True)

                # Load hospital info (name and location) and update label/map
                async def load_hospital_info():
                    token = app.storage.user.get("access_token")
                    if not token:
                        return

                    # try /hospitals/me first
                    def _get_me():
                        return requests.get(
                            f"{base_url}/hospitals/me/profile",
                            headers={"Authorization": f"Bearer {token}"},
                        )

                    try:
                        resp = await run.io_bound(_get_me)
                    except Exception:
                        resp = None

                    data = None
                    if resp and resp.status_code == 200:
                        try:
                            data = resp.json()
                        except Exception:
                            data = None

                    # fallback to decoding hospital id from token and hitting /hospitals/{id}
                    if not data:
                        hospital_id = app.storage.user.get("hospital_id")
                        if not hospital_id:
                            # attempt to decode from token
                            try:
                                import base64, json

                                parts = token.split(".")
                                if len(parts) >= 2:
                                    payload_b64 = parts[1]
                                    padding = "=" * (-len(payload_b64) % 4)
                                    payload_b64 += padding
                                    decoded = base64.urlsafe_b64decode(
                                        payload_b64.encode()
                                    ).decode()
                                    payload_json = json.loads(decoded)
                                    hospital_id = (
                                        payload_json.get("hospital_id")
                                        or payload_json.get("hospitalId")
                                        or payload_json.get("sub")
                                    )
                            except Exception:
                                hospital_id = None

                        if hospital_id:

                            def _get_by_id():
                                return requests.get(
                                    f"{base_url}/hospitals/{hospital_id}",
                                    headers={"Authorization": f"Bearer {token}"},
                                )

                            try:
                                resp2 = await run.io_bound(_get_by_id)
                                if resp2.status_code == 200:
                                    try:
                                        data = resp2.json()
                                    except Exception:
                                        data = None
                            except Exception:
                                data = None

                    if data:
                        # data may be the hospital object or a wrapper {data: {...}}
                        if (
                            isinstance(data, dict)
                            and "data" in data
                            and isinstance(data.get("data"), dict)
                        ):
                            hosp = data.get("data")
                        else:
                            hosp = data

                        name = (
                            hosp.get("hospital_name")
                            or hosp.get("name")
                            or hosp.get("hospitalName")
                        )
                        address = (
                            hosp.get("location_address")
                            or hosp.get("address")
                            or hosp.get("location")
                        )

                        if name:
                            try:
                                hospital_name_label.set_text(name)
                            except Exception:
                                pass

                        if address:
                            # update the map iframe to center on the provided address
                            iframe_html = f"""<iframe src="https://www.google.com/maps?q={requests.utils.quote(address)}&output=embed" width="100%" height="200" style="border:0; border-radius: 12px;" allowfullscreen="" loading="lazy"></iframe>"""
                            hospital_map.clear()
                            with hospital_map:
                                ui.html(iframe_html, sanitize=False).classes(
                                    "w-full h-50 rounded-md overflow-hidden"
                                )

                ui.timer(0.6, load_hospital_info, once=True)

        # Footer
        with ui.row().classes(
            "flex flex-col md:flex-row items-center justify-between px-7 w-full bg-gray-50 py-5 text-sm text-gray-700 mt-auto"
        ):
            ui.label("© 2025 LifeLink. All rights reserved.").classes("mb-3 md:mb-0")
            with ui.row().classes("gap-6"):
                ui.link("About").classes("no-underline text-gray-700 transition")
                ui.link("Contact").classes(
                    "no-underline hover:text-white text-gray-700 transition"
                )
                ui.link("Privacy Policy").classes(
                    "no-underline text-gray-700 transition"
                )

        # Profile modal
        profile_modal = ui.dialog()
        with profile_modal:
            with ui.menu().props("anchor=top-left"):
                ui.menu_item("View Profile")
                ui.menu_item("Settings")
                ui.menu_item("Help")
                ui.menu_item("Logout", on_click=lambda: logout_modal.open())
        # Logout confirmation modal
        logout_modal = ui.dialog()
        with logout_modal:
            with ui.card().classes("p-4 w-[90vw] md:w-[25vw]"):
                ui.label("Confirm Logout").classes("text-lg font-semibold mb-3")
                ui.label("Are you sure you want to logout?").classes(
                    "text-sm text-gray-700 mb-3"
                )
                with ui.row().classes("justify-end gap-2"):
                    ui.button("Cancel", on_click=lambda: logout_modal.close()).props(
                        "flat dense"
                    )
                    ui.button("Logout", on_click=lambda: ui.navigate.to("/")).props(
                        "flat dense"
                    ).classes("bg-red-600 text-white")
