from nicegui import ui,app

# components
from components.navbar import show_navbar
from components.footer import show_footer

@ui.page("/")
def home_page():
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")
    with ui.element("main").classes("min-h-screen w-full flex flex-col"):
        # Navbar
        show_navbar()
        # Hero
        with ui.element("hero").classes("flex items-center justify-center w-full text-white bg-[url('/assets/hero.png')] bg-cover bg-center bg-black/60 bg-blend-overlay"):
            with ui.column().classes("items-center w-full max-w-screen-lg text-center py-35 px-5"):
                ui.label("Connecting Donors, Saving Lives.").classes("text-2xl md:text-6xl font-bold")
                ui.html(
                    content=(
                        "Lifelink is a platform dedicated to connecting blood donors with hospitals in <br>"
                        "need, while also providing education about sickle cell disease. Our mission is to<br>"
                        "ensure timely access to life-saving blood for patients, especially those with<br>"
                        "sickle cell disease, by building a robust network of donors and providing critical<br>"
                        "information"
                    ), sanitize=False).classes("text-base md:text-lg leading-relaxed")
                with ui.row().classes("gap-4 mt-6"):
                    ui.button("Volunteer Signup").props("no-caps flat dense").classes("bg-red-600 text-white px-4 rounded-md hover:bg-red-500 transition")
                    ui.button("Learn About Sickle Cell", on_click=lambda: ui.navigate.to("/sicklecell_education")).props("no-caps flat dense").classes("bg-[rgba(255,255,255,0.3)] text-white rounded-md px-4 hover:bg-[rgba(255,255,255,0.5)] transition")
        # Stats Section
        with ui.row().classes("grid grid-cols-1 md:grid-cols-3 gap-6 w-full px-3 md:px-7 py-10 max-w-screen-lg mx-auto"):
            with ui.card().classes("flex flex-col items-center p-6 shadow rounded-md"):
                ui.label("12,500+").classes("text-2xl md:text-4xl font-bold text-red-500")
                ui.label("Donors Registered").classes("text-sm md:text-base text-gray-700 font-bold")
            with ui.card().classes("flex flex-col items-center p-6 shadow rounded-md"):
                ui.label("250+").classes("text-2xl md:text-4xl font-bold text-red-500")
                ui.label("Hospitals Onboarded").classes("text-sm md:text-base text-gray-700 font-bold")
            with ui.card().classes("flex flex-col items-center p-6 shadow rounded-md"):
                ui.label("5,000+").classes("text-2xl md:text-4xl font-bold text-red-500")
                ui.label("Successful Matches").classes("text-sm md:text-base text-gray-700 font-bold")
        # Footer
        show_footer()
        