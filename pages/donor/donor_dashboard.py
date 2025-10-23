from nicegui import ui
from components.donor_header import donor_header
from components.donor_sidebar import donor_sidebar


# ---------------- FOOTER ----------------
def footer():
    with ui.row().classes(
        "flex flex-col md:flex-row items-center justify-between px-7 w-full bg-gray-50 py-5 text-sm mt-auto text-gray-500"
    ):
        ui.image("/assets/logo.png").classes("w-24 h-20")
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
    """Render donation history section without data or backend connection."""

    # Define empty columns (no data yet)
    COLUMNS = [
        {'name': 'id', 'label': 'ID', 'field': 'id', 'align': 'left'},
        {'name': 'donation_date', 'label': 'DATE', 'field': 'donation_date', 'align': 'left'},
        {'name': 'location', 'label': 'LOCATION', 'field': 'location', 'align': 'left'},
        {'name': 'recipient_info', 'label': 'RECIPIENT INFO', 'field': 'recipient_info', 'align': 'left'},
        {'name': 'status', 'label': 'STATUS', 'field': 'status', 'align': 'center'},
    ]

    view_mode = ui.label('table').props('hidden')
    history_container = ui.column().classes("w-full mt-4")

    def render_list_view():
        """Empty table layout."""
        with history_container:
            ui.table(columns=COLUMNS, rows=[], row_key='id') \
                .props('flat bordered dense') \
                .classes('w-full rounded-lg overflow-hidden') \
                .tooltip("No donation history records found.")

    def render_grid_view():
        """Empty grid placeholder."""
        with history_container:
            ui.label("No donation history available.").classes(
                "text-gray-500 italic text-center py-8 w-full"
            )

    def update_history_view():
        history_container.clear()
        if view_mode.text == 'table':
            render_list_view()
        else:
            render_grid_view()

    def toggle_view(mode):
        view_mode.set_text(mode)
        update_icons()
        update_history_view()

    def update_icons():
        if view_mode.text == 'table':
            list_btn.props('flat color=red')
            grid_btn.props('flat color=gray')
        else:
            list_btn.props('flat color=gray')
            grid_btn.props('flat color=red')

    # Layout
    with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white mt-6"):
        with ui.row().classes("w-full justify-between items-center mb-4 border-b pb-4"):
            ui.label("Donation History").classes("text-xl font-semibold text-gray-800")
            with ui.row().classes("items-center gap-2"):
                list_btn = ui.button(
                    icon="fa-solid fa-list", on_click=lambda: toggle_view('table')
                ).props('flat round dense')
                grid_btn = ui.button(
                    icon="fa-solid fa-grip", on_click=lambda: toggle_view('grid')
                ).props('flat round dense')
                update_icons()

        update_history_view()


# ---------------- DASHBOARD PAGE ----------------
@ui.page("/donor/dashboard")
def donor_dashboard_page():
    """Frontend-only donor dashboard with sidebar, header, and footer."""
    ui.add_head_html('<script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>')
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")

    # Layout container
    with ui.row().classes("min-h-screen w-full bg-gray-50 overflow-hidden"):
        # Fixed Sidebar
        with ui.element("div").classes(
            "fixed left-0 top-0 bottom-0 w-64 bg-white border-r border-gray-200 hidden md:flex"
        ):
            donor_sidebar()

        # Main content area
        with ui.column().classes(
            "flex-1 p-6 ml-0 md:ml-64 w-full min-h-screen overflow-auto"
        ):
            # Header
            with ui.header(elevated=True).classes(
                "bg-white dark:text-white shadow-md px-6 py-3 flex justify-between items-center sticky top-0 z-50"
            ):
                donor_header()

            # Dashboard Body
            with ui.column().classes("p-6 md:px-[8%] items-center"):        
                ui.label("🩸 Welcome to your Donor Dashboard").classes(
                    "text-4xl font-extrabold text-gray-900 mb-4 text-center"
                )
                ui.label("Track your blood donation activity and responses here.").classes(
                    "text-lg text-gray-600 mb-8 text-center"
                )

                # Donation History Table / Grid Placeholder
                donation_history_section()

            # Footer
            footer()
