from nicegui import ui,app

app.add_static_files("/assets","assets")


@ui.page("/volunteer_signup")
def volunteer_signup_page():
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")

    with ui.element("main").classes("min-h-screen w-full flex flex-col"):
        # Navbar
        with ui.row().classes(
            "flex flex-col md:flex-row items-center justify-between shadow-md w-full px-3 md:px-7 py-1"
        ):
            with ui.row().classes("gap-0 items-center justify-center"):
                ui.image("/assets/logo.png").classes("w-12 h-12")
                ui.label("LifeLink").classes("text-xl font-bold text-gray-700")
            with ui.row().classes("gap-6 mt-3 md:mt-0"):
                ui.link("About","/about").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("How it works").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("Contact").classes("no-underline text-gray-700 hover:text-red-500 transition")
            with ui.row().classes("gap-3 mt-3 md:mt-0"):
                ui.button("Register").props("no-caps flat dense").classes("bg-red-600 text-white hover:bg-red-500 rounded-md px-4")
                ui.button("Login").props("no-caps flat dense").classes("bg-pink-200 text-red hover:bg-red-500 rounded-md px-4")
        # Signup form 
        with ui.element("section").classes("flex-grow flex items-center justify-center w-full px-4"):
            with ui.card().classes("w-full md:w-[60%] lg:w-[50%] p-6 bg-white text-gray-700 rounded-md items-center my-3 shadow-none border-none"):
                ui.label("Become a Volunteer").classes("text-2xl font-bold text-center m-0 p-0 text-black")
                ui.label("Join our community and make a difference. Your help is vital.").classes("text-sm text-center text-gray-700 mb-4")

                # Full Name
                with ui.element("div").classes("flex flex-col w-full mb-2"):
                    ui.label("Full Name").classes("text-sm text-left")
                    ui.input(placeholder="Enter your full name").props("flat outlined border-red dense").classes("rounded-sm bg-white text-xs")

                # Location
                with ui.element("div").classes("flex flex-col w-full mb-2"):
                    ui.label("Location").classes("text-sm text-left")
                    ui.input(placeholder="eg., City, State").props("flat outlined dense").classes("rounded-sm bg-white text-xs border-red-600")

                # Skills / Interests
                with ui.element("div").classes("flex flex-col w-full mb-2"):
                    ui.label("Skills / Interests").classes("text-sm text-left")
                    ui.label("Choose the areas where you'd like to contribute.").classes("text-xs text-gray-600 mb-2")
                    with ui.row().classes("gap-6"):
                        ui.checkbox("Awareness Campaigns").props("color=red").classes("text-sm")
                        ui.checkbox("Education & Outreach").props("color=red").classes("text-sm")
                        ui.checkbox("Event Organization").props("color=red").classes("text-sm")

                # Contact Number
                with ui.element("div").classes("flex flex-col w-full mb-2"):
                    ui.label("Contact Number").classes("text-sm text-left")
                    ui.input(placeholder="Enter your phone number").props("flat outlined dense").classes("rounded-sm bg-white text-xs border-red-600")

                # Email Address
                with ui.element("div").classes("flex flex-col w-full mb-2"):
                    ui.label("Email Address").classes("text-sm text-left")
                    ui.input(placeholder="you@example.com").props("flat outlined dense").classes("rounded-sm bg-white text-xs border-red-600")

                # Register button
                ui.button("Register Now").props("no-caps flat dense").classes(
                    "bg-red-600 text-white hover:bg-red-500 rounded-md my-4 py-2 px-4 w-full"
                )

        # Footer 
        with ui.element("div").classes("flex flex-col items-center justify-center px-7 w-full bg-gray-50 py-4 text-sm mt-auto text-gray-700"):
            
            # Links row (top)
            with ui.row().classes("gap-6 justify-center mb-2"):
                ui.link("Home").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("About",).classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("Campaigns").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("Education").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("Contact").classes("no-underline text-gray-700 hover:text-red-500 transition")
            
            # Copyright row (separate from links)
            with ui.row().classes("justify-center w-full"):
                ui.label("© 2025 LifeLink. All rights reserved.").classes("text-gray-500 text-center")
