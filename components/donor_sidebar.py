from nicegui import ui


def donor_sidebar():
    with ui.column().classes("w-full bg-white shadow-xl rounded-xl p-4 space-y-2"):
                        with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white"):
                            ui.label("My Information").classes("text-xl font-semibold text-gray-800 mb-4")
                            
                            # Blood Group
                            with ui.row().classes("w-full items-center space-x-4 mb-4"):
                                ui.icon("water_drop").classes("text-4xl text-red-600")
                                with ui.column().classes("gap-0"):
                                    ui.label("Blood Group").classes("text-sm text-gray-500")
                                    ui.label("O+").classes("text-3xl font-bold text-red-600")
                                    
                            
                            ui.separator().classes("my-4")
                            
                            # Quick Actions (Matches bottom right of screen.png)
                            with ui.column().classes("w-full space-y-3"):
                                ui.button("Edit Profile", icon="edit").props("outline no-caps").classes("w-full text-gray-700 border-gray-300 hover:bg-gray-100").on("click", lambda: ui.navigate.to("/donor/profile"))
                                ui.button("Update Availability", icon="schedule").props("no-caps").classes("w-full bg-red-100 text-red-600 hover:bg-red-200")
                                ui.button("View Medical History", icon="medical_services").props("flat no-caps").classes("w-full text-red-600 hover:bg-red-100").on("click", lambda: ui.navigate.to("/donor/profile"))
            

        # Dashboard Link
        # dashboard_classes, dashboard_icon_classes = get_link_classes("Dashboard")
        # with ui.link("Dashboard", "/donor/dashboard").classes():
        #     ui.icon("dashboard").classes()
        #     ui.label("Dashboard")
