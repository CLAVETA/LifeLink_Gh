from nicegui import ui, app
# components
from components.donor_header import donor_header

# Define your app's color theme
PRIMARY_COLOR = "#ec1313"
BACKGROUND_LIGHT = "#f8f6f6"
TEXT_DARK = "#221010"

@ui.page("/donor/donation_request")
def donation_request_page():

    # # ---------- HEADER ----------
    # with ui.header().classes("bg-white shadow-md px-6 py-3 flex justify-between items-center sticky top-0 z-50"):
    #     with ui.row().classes("items-center gap-2"):
    #         ui.icon("favorite").classes("text-red-600 text-3xl")
    #         ui.label("LiveLink").classes("text-2xl font-bold text-gray-900")

    #     with ui.row().classes("hidden md:flex items-center gap-6"):
    #         ui.link("Home", "#").classes("text-gray-700 hover:text-red-600 transition-colors")
    #         ui.link("About", "#").classes("text-gray-700 hover:text-red-600 transition-colors")
    #         ui.link("Contact","/about#contact").classes("text-gray-700 hover:text-red-600 transition-colors")

    #     with ui.row().classes("items-center gap-3"):
    #         ui.button("Donate Now", color=PRIMARY_COLOR).classes(
    #             "text-white font-semibold rounded-lg hover:bg-red-700 transition-all"
    #         )
    #         with ui.button(icon="notifications").classes(
    #             "relative bg-white text-black rounded-full hover:bg-gray-100 transition"
    #         ):
    #             with ui.element("span").classes("absolute top-0 right-0 flex h-3 w-3").props(
    #     "style='transform: translate(25%, -25%)'"
    # ):
    #                 ui.html("""
    #                     <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-75"></span>
    #                     <span class="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
    #                 """, sanitize=False)
    with ui.header(elevated=True).classes('bg-white dark:bg-gray-800 text-black dark:text-white'):
        donor_header()
    # ---------- MAIN CONTENT ----------
    with ui.row().classes("justify-center items-center py-12 px-4"):
        with ui.card().classes("w-full md:mx-[20%] shadow-2xl rounded-xl overflow-hidden"):
            with ui.column().classes("p-8 items-center text-center"):
                ui.label("Urgent Blood Request").classes("text-3xl font-extrabold text-gray-900")
                ui.label("Your help is needed immediately.").classes("text-gray-600 mb-4")

                # Background image with overlay
                with ui.element("div").classes("relative w-full h-64 rounded-lg overflow-hidden mb-6"):
                    ui.html(
                        """
                        <div class="absolute inset-0 bg-cover bg-center" 
                             style="background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuDWRPy7APasZW2cau2jCTn7BUrxgIiWGFSisR4dcHoE99YqTtdEWMomYqofW1aUwhSCg7pcnhvZ4UF4nDs5oLTuExmex_D0-GWBu4rLJXYBLUJ4JR5fXGdRhIZfXJpkK32O7bX8GpDvruvo80sh6o5giVJhGOUaS01Hu6BvE9_vVLt5pK_NNvr7jGz1biqupLu9b3ND4Ngyb917JA5RfBIRWHJKsY1nbfTqludgESHr_RJ21TIAC7qReWkpC-62PAFyWZ_hI7cAMg');">
                        </div>
                        <div class="absolute inset-0 bg-black/50"></div>
                        """, sanitize = False
                    ).classes("absolute inset-0")
                    with ui.column().classes("absolute inset-0 text-white justify-center items-left pl-5"):
                        ui.label("Blood Type Needed").classes("uppercase text-sm font-semibold text-red-400 tracking-wider")
                        ui.label("O-").classes("text-5xl font-black mb-4")
                        ui.label("Location").classes("uppercase text-sm font-semibold text-red-400 tracking-wider")
                        ui.label("City General Hospital").classes("text-lg font-medium")
                        ui.label("123 Main Street, Anytown").classes("text-gray-300")

                ui.label(
                    "This request is marked as URGENT. Please respond as soon as possible if you are an eligible donor."
                ).classes("text-gray-700 text-base px-4")

                with ui.row().classes("mt-8 w-full grid grid-cols-1 sm:grid-cols-2 gap-4"):
                    ui.button("Respond to Request", icon="bloodtype", color=PRIMARY_COLOR).props("dense flat no-caps").classes(
                        "w-full py-3 font-bold text-white hover:bg-red-600 transition transform hover:scale-105"
                    )
                    ui.button("View Hospital Info", icon="local_hospital").props("dense flat no-caps").classes(
                        "w-full py-3 font-bold text-red-600 bg-red-100 hover:bg-red-200 transition transform hover:scale-105"
                    )

    # ---------- FOOTER ----------
    with ui.footer().classes("bg-white border-t border-red-100 text-center py-4 text-gray-600"):
        ui.label("© 2025 LiveLink. All rights reserved.")
