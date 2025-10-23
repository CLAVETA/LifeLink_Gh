from nicegui import ui, app
import requests
from components.donor_footer import donor_footer
from components.donor_header import donor_header
from components.donor_sidebar import donor_sidebar  # ✅ Import sidebar

# ---------------- THEME ----------------
PRIMARY_COLOR = "#ec1313"
BACKGROUND_LIGHT = "#f8f6f6"
TEXT_DARK = "#221010"

# ---------------- API ENDPOINTS ----------------
API_URL = "https://lifelinkgh-api.onrender.com/requests/all?limit=10&skip=0"
RESPOND_URL = "https://lifelinkgh-api.onrender.com/donors/requests/{request_id}/respond"


@ui.page("/donor/donation_request")
def donation_request_page():
    """Donation Requests Page (Donor Alerts) with Sidebar and Enhanced UI"""

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
        if not token:
            ui.notify("⚠️ Please log in first — missing authorization token.", color="red")
            return

        try:
            url = RESPOND_URL.format(request_id=request_id)
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/x-www-form-urlencoded",
            }

            res = requests.post(url, headers=headers)
            if res.status_code == 201:
                ui.notify("✅ Successfully responded to this request.", color="green")
            else:
                ui.notify(f"⚠️ Failed to respond: {res.text}", color="red")
        except Exception as ex:
            ui.notify(f"❌ Error: {ex}", color="red")
            print(ex)

    # ---------- PAGE LAYOUT ----------
    with ui.row().classes("min-h-screen w-full bg-gray-50 overflow-hidden"):
        # SIDEBAR (fixed)
        with ui.element("div").classes(
            "fixed left-0 top-0 bottom-0 w-64 bg-white border-r border-gray-200 hidden md:flex"
        ):
            donor_sidebar()

        # MAIN CONTENT AREA
        with ui.column().classes(
            "flex-1 ml-0 md:ml-64 w-full min-h-screen overflow-auto"
        ):
            # Header (sticky)
            with ui.header(elevated=True).classes(
                "bg-white dark:text-white shadow-md px-6 py-3 flex justify-between items-center sticky top-0 z-50"
            ):
                donor_header()

            # ---------- MAIN CONTENT ----------
            with ui.column().classes(
                "p-6 sm:p-8 md:px-[6%] bg-gray-50 items-center justify-center min-h-screen"
            ):
                ui.label("🩸 Donation Requests").classes(
                    "text-4xl font-extrabold text-gray-900 mb-8 text-center"
                )

                if not data_list:
                    ui.label("No active donation requests found.").classes(
                        "text-gray-600 italic text-center mt-10"
                    )
                else:
                    with ui.grid(columns=1).classes(
                        "sm:grid-cols-2 lg:grid-cols-3 gap-8 w-full max-w-[1400px] justify-center"
                    ):
                        for req in data_list:
                            request_id = req.get("_id") or req.get("id", None)
                            blood_type = req.get("blood_type", "Unknown")
                            hospital = req.get("hospital_name", "Hospital")
                            location = req.get("location", "Location not provided")
                            urgency = req.get("urgency", "Normal")
                            description = req.get(
                                "description", "No description available."
                            )
                            image_url = req.get(
                                "image_url",
                                "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?q=80&w=1470&auto=format&fit=crop",
                            )

                            # Card layout
                            with ui.card().classes(
                                "shadow-md rounded-2xl overflow-hidden hover:shadow-2xl "
                                "transition-transform duration-300 hover:scale-[1.02] bg-white"
                            ):
                                with ui.column().classes("p-0 text-left"):
                                    # Image Banner
                                    with ui.element("div").classes(
                                        "relative w-full h-44 overflow-hidden"
                                    ):
                                        ui.html(f"""
                                            <div class='absolute inset-0 bg-cover bg-center' 
                                                 style='background-image: url("{image_url}");'></div>
                                            <div class='absolute inset-0 bg-gradient-to-t from-black/60 to-transparent'></div>
                                        """, sanitize=False)
                                        with ui.column().classes(
                                            "absolute bottom-3 left-4 text-white"
                                        ):
                                            ui.label(blood_type).classes(
                                                "text-3xl font-black tracking-wide"
                                            )
                                            ui.label(location).classes(
                                                "text-sm text-gray-200 font-medium"
                                            )

                                    # Text Content
                                    with ui.column().classes("p-5"):
                                        ui.label(hospital).classes(
                                            "text-xl font-bold text-gray-900 mb-1"
                                        )
                                        ui.label(f"Urgency: {urgency}").classes(
                                            f"text-sm font-semibold {'text-red-600' if urgency.lower() == 'urgent' else 'text-gray-500'} mb-3"
                                        )
                                        ui.label(description).classes(
                                            "text-gray-700 text-sm mb-6 line-clamp-3"
                                        )

                                        # Action Buttons
                                        with ui.row().classes("gap-3"):
                                            ui.button(
                                                "Respond",
                                                icon="bloodtype",
                                                color=PRIMARY_COLOR,
                                                on_click=lambda req_id=request_id: respond_to_request(req_id)
                                            ).props("dense flat no-caps").classes(
                                                "flex-1 py-2 font-bold text-white rounded-lg hover:bg-red-600 transition-all"
                                            )

                                            ui.button(
                                                "Hospital Info",
                                                icon="local_hospital"
                                            ).props("dense flat no-caps").classes(
                                                "flex-1 py-2 font-bold text-red-600 bg-red-100 hover:bg-red-200 rounded-lg transition-all"
                                            )

            donor_footer()
