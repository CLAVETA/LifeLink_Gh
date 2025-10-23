from nicegui import ui, app
import requests
from components.donor_footer import donor_footer
from components.donor_header import donor_header

# ---------------- THEME ----------------
PRIMARY_COLOR = "#ec1313"
BACKGROUND_LIGHT = "#f8f6f6"
TEXT_DARK = "#221010"

# ---------------- API ENDPOINTS ----------------
API_URL = "https://lifelinkgh-api.onrender.com/requests/all?limit=10&skip=0"
RESPOND_URL = "https://lifelinkgh-api.onrender.com/donors/requests/{request_id}/respond"


@ui.page("/donor/donation_request")
def donation_request_page():

    # ---------- FETCH DATA ----------
    try:
        response = requests.get(API_URL, headers={"accept": "application/json"})
        response.raise_for_status()
        donation_requests = response.json()
        data_list = donation_requests.get("data", donation_requests)
    except Exception as e:
        data_list = []
        print(f"Error fetching data: {e}")

    # ---------- RESPONSE FUNCTION ----------
    def respond_to_request(request_id: str):
        """Send donor response to backend when user commits."""
        token = app.storage.user.get("access_token")
        print(f"Auth Token: {token}")

        if not token:
            ui.notify("⚠️ Please log in first — missing authorization token.", color="red")
            return

        try:
            url = RESPOND_URL.format(request_id=request_id)
            # payload = {"commitment_status": "committed"}
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/x-www-form-urlencoded",
            }

            res = requests.post(url, headers=headers)
            print(f"Response Status: {res.status_code}, Body: {res.text}")
            print(f"Responded to request ID: {request_id}")
            if res.status_code == 201:
                ui.notify("✅ Successfully responded to this request.", color="green")
            else:
                ui.notify(f"⚠️ Failed to respond: {res.text}", color="red")
        except Exception as ex:
            ui.notify(f"❌ Error: {ex}", color="red")
            print(ex)

    # ---------- HEADER ----------
    with ui.header(elevated=True).classes("bg-white dark:text-white shadow-md px-6 py-3 flex justify-between items-center sticky top-0 z-50"):
            donor_header()
    #     with ui.row().classes("items-center gap-2"):
    #         ui.icon("favorite").classes("text-red-600 text-3xl")
    #         ui.label("LiveLink").classes("text-2xl font-bold text-gray-900")

    #     with ui.row().classes("hidden md:flex items-center gap-6"):
    #         ui.link("Home", "#").classes("text-gray-700 hover:text-red-600 transition-colors")
    #         ui.link("About", "#").classes("text-gray-700 hover:text-red-600 transition-colors")
    #         ui.link("Contact", "/about#contact").classes("text-gray-700 hover:text-red-600 transition-colors")

    #     with ui.row().classes("items-center gap-3"):
    #         ui.button("Donate Now", color=PRIMARY_COLOR).classes(
    #             "text-white font-semibold rounded-lg hover:bg-red-700 transition-all"
    #         )
    #         with ui.button(icon="notifications").classes(
    #             "relative bg-white text-gray-700 rounded-full hover:bg-gray-100 transition"
    #         ):
    #             with ui.element("span").classes("absolute top-0 right-0 flex h-3 w-3").props(
    #                 "style='transform: translate(25%, -25%)'"
    #             ):
    #                 ui.html("""
    #                     <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-75"></span>
    #                     <span class="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
    #                 """, sanitize=False)

    # ---------- MAIN CONTENT ----------
    with ui.column().classes("p-8 md:px-[10%] items-center"):
        ui.label("Donation Requests").classes("text-3xl font-extrabold text-gray-900 mb-8")

        if not data_list:
            ui.label("No active donation requests found.").classes("text-gray-600 italic")
        else:
            with ui.row().classes("grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 w-full justify-center"):
                for req in data_list:
                    request_id = req.get("_id") or req.get("id", None)
                    blood_type = req.get("blood_type", "blood_type")
                    hospital = req.get("hospital_name", "hospital")
                    location = req.get("location", "Location")
                    urgency = req.get("urgency", "Normal")
                    description = req.get("description", "No description available.")
                    image_url = req.get(
                        "image_url",
                        "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?q=80&w=1470&auto=format&fit=crop"
                    )

                    with ui.card().classes("shadow-lg rounded-xl overflow-hidden hover:shadow-2xl transition transform hover:scale-[1.02]"):
                        with ui.column().classes("p-6 text-left"):
                            with ui.row().classes("justify-between items-center w-full mb-3"):
                                ui.label(hospital).classes("text-xl font-bold text-gray-900")
                                ui.label(f"Urgency: {urgency}").classes(
                                    f"text-sm font-semibold {'text-red-600' if urgency.lower() == 'urgent' else 'text-gray-500'}"
                                )

                            with ui.element("div").classes("relative w-full h-40 rounded-lg overflow-hidden mb-4"):
                                ui.html(f"""
                                    <div class='absolute inset-0 bg-cover bg-center' 
                                         style='background-image: url("{image_url}");'></div>
                                    <div class='absolute inset-0 bg-black/40'></div>
                                """, sanitize=False)
                                with ui.column().classes("absolute inset-0 text-white justify-center items-left pl-4"):
                                    ui.label("Blood Type Needed").classes("uppercase text-xs font-semibold text-red-300 tracking-wider")
                                    ui.label(blood_type).classes("text-3xl font-black mb-1")
                                    ui.label(location).classes("text-sm text-gray-200 font-medium")

                            ui.label(description).classes("text-gray-700 text-sm mb-6 line-clamp-3")

                            with ui.row().classes("grid grid-cols-2 gap-3"):
                                ui.button(
                                    "Respond",
                                    icon="bloodtype",
                                    color=PRIMARY_COLOR,
                                    on_click=lambda req_id=request_id: respond_to_request(req_id)
                                ).props("dense flat no-caps").classes(
                                    "w-full py-2 font-bold text-white hover:bg-red-600 transition"
                                )
                                ui.button(
                                    "Hospital Info",
                                    icon="local_hospital"
                                ).props("dense flat no-caps").classes(
                                    "w-full py-2 font-bold text-red-600 bg-red-100 hover:bg-red-200 transition"
                                )

    donor_footer()
