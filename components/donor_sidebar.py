from nicegui import ui

def donor_sidebar():
    """Responsive, collapsible donor sidebar with icons, tooltips, and navigation links."""

    # State variable for collapse toggle
    sidebar_state = {"collapsed": False}

    def toggle_sidebar():
        """Collapse or expand the sidebar."""
        sidebar_state["collapsed"] = not sidebar_state["collapsed"]
        sidebar.refresh()

    @ui.refreshable
    def sidebar():
        collapsed = sidebar_state["collapsed"]

        with ui.column().classes(
            f"bg-white shadow-xl h-full p-4 transition-all duration-300 ease-in-out "
            f"{'w-20' if collapsed else 'w-64'} "
            "rounded-xl overflow-hidden"
        ):
            # Top Section: Logo & Toggle
            with ui.row().classes("items-center justify-between mb-6 w-full"):
                if not collapsed:
                    ui.label("LifeLink").classes("text-2xl font-bold text-red-600")
                ui.button(icon="menu", on_click=toggle_sidebar) \
                    .props("flat round dense") \
                    .classes("text-gray-600 hover:text-red-600")

            # Navigation Buttons (icon + tooltip)
            nav_items = [
                ("dashboard", "Dashboard", "/donor/dashboard"),
                ("favorite", "Donation Requests", "/donor/donation_request"),
                ("notifications_active", "Alerts", "/donor/alerts"),
                ("menu_book", "Donor Education", "/education/user"),
                ("info", "About LifeLink", "/about"),
            ]

            for icon_name, label, route in nav_items:
                with ui.tooltip(label):
                    ui.button(
                        icon=icon_name if collapsed else None,
                        text=None if collapsed else label,
                        on_click=lambda r=route: ui.navigate.to(r),
                    ).classes(
                        f"w-full justify-start text-left "
                        f"{'bg-red-600 text-white' if route == '/donor/dashboard' else 'bg-red-50 text-red-700'} "
                        f"hover:bg-red-100 font-semibold rounded-lg transition-all duration-200 py-2 px-3"
                    ).props("no-caps")

            ui.separator().classes("my-4")

            # Logout button
            with ui.tooltip("Logout"):
                ui.button(
                    icon="logout" if collapsed else None,
                    text=None if collapsed else "Logout",
                    on_click=lambda: ui.navigate.to("/donor/login"),
                ).classes(
                    "w-full bg-gray-100 text-gray-700 hover:bg-gray-200 "
                    "font-semibold rounded-lg transition-all duration-200 py-2 px-3"
                ).props("no-caps")

    # Responsive layout: hide sidebar on very small screens
    with ui.row().classes("w-full h-full"):
        with ui.element("div").classes(
            "hidden sm:block h-full"
        ):  # Sidebar visible only on small+ screens
            sidebar()

        with ui.column().classes("flex-1 p-4 overflow-auto"):
            ui.label("Main Content Area").classes("text-gray-600 text-center mt-10")
