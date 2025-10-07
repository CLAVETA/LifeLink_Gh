from nicegui import ui


def show_footer():
    with ui.row().classes("flex flex-col md:flex-row items-center justify-between px-7 w-full bg-gray-50 py-5 text-sm text-gray-700 mt-auto"):
            ui.label("© 2025 LifeLink. All rights reserved.").classes("mb-3 md:mb-0")
            with ui.row().classes("gap-6"):
                ui.link("About").classes("no-underline text-gray-700 transition")
                ui.link("Contact").classes("no-underline hover:text-white text-gray-700 transition")
                ui.link("Privacy Policy").classes("no-underline text-gray-700 transition")
                ui.link("FAQs").classes("no-underline text-gray-700 transition")