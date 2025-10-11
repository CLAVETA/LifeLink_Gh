from nicegui import ui, app

# components
from components.donor_sidebar import donor_sidebar
from components.donor_header import donor_header

@ui.page("/donor/profile")
def donor_profile_page():
    # Setup for responsive design and removing default NiceGUI margins
    ui.add_head_html('<script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>')
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")

    # with ui.element("main").classes("min-h-screen w-full bg-gray-50 p-4 sm:p-8"):
    with ui.header(elevated=True).classes('bg-white dark:bg-gray-800 text-black dark:text-white'):
        donor_header()       
    with ui.left_drawer(bordered=True).classes('bg-gray-100 dark:bg-gray-900'):
        donor_sidebar()    

    # with ui.element("main").classes("min-h-screen w-full bg-gray-50 p-4 sm:p-8"):
    #     # Main Portal Container (Sidebar + Content)
    #     with ui.row().classes("w-full max-w-screen-xl mx-auto flex flex-col lg:flex-row gap-6"):
            

            # Right Column (Profile Content)
    with ui.column().classes("flex-grow w-full"):
                
                ui.label("My Profile").classes("text-3xl font-bold text-gray-800 mb-2 mt-2 p-6 ml-4")
                
                # Profile Header (Image and Name)
                with ui.column().classes("w-full items-left bg-white p-6 shadow-lg rounded-xl mb-6"):
                    # Placeholder for profile image
                    ui.image("/assets/logo.png").classes("w-20 h-20")
                    ui.html('<div class="w-20 h-20 rounded-full bg-gray-200 flex items-center justify-center text-gray-500 text-3xl font-bold">JD</div>', sanitize=False).classes("flex-shrink-0")
                    
                    with ui.column().classes("ml-4 gap-0"):
                        ui.label("Jane Doe").classes("text-xl font-semibold text-gray-800")
                        ui.label("O+ Blood Type | Registered Donor").classes("text-sm text-red-600")
                    
                    # Action Button (top right)
                    ui.button("Edit Profile", icon="edit").props("flat no-caps").classes("ml-auto text-red-600 hover:bg-red-100")
                        
                # 1. Personal Information Card
                with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white mb-6"):
                    ui.label("Personal Information").classes("text-xl font-semibold text-gray-800 mb-4 border-b pb-2")
                    
                    # Grid for input fields
                    with ui.row().classes("grid grid-cols-1 md:grid-cols-2 gap-4 w-full mt-4"):
                        # Name
                        with ui.column().classes("w-full"):
                            ui.label("Full Name").classes("text-xs font-medium text-gray-500")
                            ui.input(value="Jane Doe").props("outlined dense readonly").classes("w-full bg-gray-50")
                        # Email
                        with ui.column().classes("w-full"):
                            ui.label("Email Address").classes("text-xs font-medium text-gray-500")
                            ui.input(value="jane.doe@example.com").props("outlined dense readonly").classes("w-full bg-gray-50")
                        # Phone
                        with ui.column().classes("w-full"):
                            ui.label("Phone Number").classes("text-xs font-medium text-gray-500")
                            ui.input(value="+233 24 000 0000").props("outlined dense readonly").classes("w-full bg-gray-50")
                        # Blood Type
                        with ui.column().classes("w-full"):
                            ui.label("Blood Type").classes("text-xs font-medium text-gray-500")
                            ui.input(value="O Positive (O+)").props("outlined dense readonly").classes("w-full bg-red-50 text-red-600 font-bold")
                            
                # 2. Address Information Card
                with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white mb-6"):
                    ui.label("Address Information").classes("text-xl font-semibold text-gray-800 mb-4 border-b pb-2")
                    
                    with ui.column().classes("w-full mt-4 space-y-3"):
                        # Street Address
                        ui.label("Street Address").classes("text-xs font-medium text-gray-500")
                        ui.input(value="456 Donor Lane").props("outlined dense readonly").classes("w-full bg-gray-50")
                        # City, Region, Postcode (3-column layout)
                        with ui.row().classes("grid grid-cols-1 sm:grid-cols-3 gap-4 w-full"):
                            with ui.column().classes("w-full"):
                                ui.label("City").classes("text-xs font-medium text-gray-500")
                                ui.input(value="Accra").props("outlined dense readonly").classes("w-full bg-gray-50")
                            with ui.column().classes("w-full"):
                                ui.label("Region").classes("text-xs font-medium text-gray-500")
                                ui.input(value="Greater Accra").props("outlined dense readonly").classes("w-full bg-gray-50")
                            with ui.column().classes("w-full"):
                                ui.label("Postcode").classes("text-xs font-medium text-gray-500")
                                ui.input(value="00233").props("outlined dense readonly").classes("w-full bg-gray-50")
                                
                # 3. Medical History & Settings Cards (Side-by-side)
                with ui.row().classes("grid grid-cols-1 md:grid-cols-2 gap-6 w-full"):
                    
                    # Medical History Card
                    with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white"):
                        ui.label("Medical History").classes("text-xl font-semibold text-gray-800 mb-4")
                        ui.label("Keep your medical records updated to ensure donation eligibility.").classes("text-sm text-gray-500 mb-4")
                        ui.button("View / Update Medical History", icon="history_edu").props("no-caps").classes("w-full bg-red-600 text-white hover:bg-red-500")

                    # Notification Settings Card
                    with ui.card().classes("w-full p-6 shadow-lg rounded-xl bg-white"):
                        ui.label("Notification Settings").classes("text-xl font-semibold text-gray-800 mb-4")
                        
                        with ui.column().classes("w-full space-y-4"):
                            # Email Notifications
                            with ui.row().classes("items-center justify-between w-full"):
                                ui.label("Email Notifications").classes("font-medium text-gray-800")
                                ui.switch().props("color=red")
                            ui.separator()
                            # SMS Alerts
                            with ui.row().classes("items-center justify-between w-full"):
                                ui.label("SMS Alerts for Urgent Need").classes("font-medium text-gray-800")
                                ui.switch(value=True).props("color=red")
                            ui.separator()    
                        
                            # App Status Updates
                            with ui.row().classes("items-center justify-between w-full"):
                                ui.label("App Status Updates").classes("font-medium text-gray-800")
                                ui.switch(value=True).props("color=red")
