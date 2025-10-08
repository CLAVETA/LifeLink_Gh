from nicegui import ui


def show_navbar():
    with ui.row().classes("flex flex-col md:flex-row items-center justify-between shadow-md w-full px-3 md:px-7 py-1"):
            with ui.row().classes("gap-0 space-x-0 items-center justify-center"):
                ui.image("/assets/logo.png").classes("w-12 h-12")
                ui.label("LifeLink").classes("text-xl font-bold text-gray-700")
            with ui.row().classes("gap-6 mt-3 md:mt-0"):
                ui.link("About","/about").classes("no-underline text-gray-700 hover:text-red transition")
                ui.link("Contact").classes("no-underline text-gray-700 hover:text-red transition")
                ui.link("FAQs").classes("no-underline text-gray-700 hover:text-red transition")
            with ui.row().classes("gap-3 mt-3 md:mt-0"):
                ui.button("Register as Donor").props("no-caps flat dense").classes("bg-red-600 text-white hover:bg-red-500 rounded-md px-4")
                ui.button("Hospital Login").props("no-caps flat dense").classes("bg-pink-200 text-red rounded-md px-4")
        