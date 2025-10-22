from nicegui import ui


def show_navbar():
    with ui.row().classes("flex flex-col md:flex-row items-center justify-between shadow-md w-full px-3 md:px-7 py-1 border-b border-red-100"):
            with ui.row().classes("gap-0 space-x-0 items-center justify-center"):
                ui.image("/assets/logo.png").classes("w-12 h-12")
                ui.link("LifeLink GH", "/").classes("text-xl font-bold text-gray-700 no-underline")
            with ui.row().classes("gap-6 mt-3 md:mt-0"):
                ui.link("About","/about").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("Education","/user_education").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("Contact","/about#contact").classes("no-underline text-gray-700 hover:text-red-500 transition")
            with ui.row().classes("gap-3 mt-3 md:mt-0"):
                ui.button("Register as Donor", on_click=lambda: ui.navigate.to("/donor_registration")).props("no-caps flat dense").classes("bg-red-600 text-white hover:bg-red-500 rounded-md px-4")
                ui.button("Register as Hospital",on_click=lambda: ui.navigate.to("/hospital/register")).props("no-caps flat dense").classes("bg-pink-200 text-red rounded-md px-4")
        