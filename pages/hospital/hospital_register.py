from nicegui import ui,app

app.add_static_files("/assets","assets")


@ui.page("/hospital_signup")
def hospital_signup_page():
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")
    with ui.element("main").classes("min-h-screen w-full flex flex-col"):
        # Navbar
        with ui.row().classes("flex flex-col md:flex-row items-center justify-between shadow-md w-full px-3 md:px-7 py-3"):
            with ui.row().classes("gap-0 items-center justify-center"):
                ui.image("/assets/logo.png").classes("w-12 h-12")
                ui.label("LifeLink").classes("text-xl font-bold text-gray-700")
            with ui.row().classes("gap-6 mt-3 md:mt-0"):
                ui.link("About","/about").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("How it works").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("Contact").classes("no-underline text-gray-700 hover:text-red-500 transition")
            with ui.row().classes("gap-3 mt-3 md:mt-0"):
                ui.button("Signup").props("no-caps flat dense").classes("bg-red-600 text-white hover:bg-red-500 rounded-md px-4")
        # Signup form 
        with ui.element("section").classes("flex-grow flex items-center justify-center w-full px-4 md:mt-5"):
            with ui.card().classes("w-full md:w-1/2 lg:w-1/3 p-6 bg-white shadow-md items-center rounded-md"):
                ui.label("Hospital Signup").classes("text-xl md:text-2xl font-bold py-1 text-center")

                with ui.element("div").classes("flex flex-col w-full py-2 text-gray-700"):
                    ui.label("Hospital Name").classes("text-sm text-left")
                    ui.input(placeholder="Your Name").props("flat outlined dense").classes("rounded-sm bg-white text-xs")

                with ui.element("div").classes("flex flex-col w-full text-gray-700"):
                    ui.label("Email Address").classes("text-sm text-left ")
                    ui.input(placeholder="Your Email").props("flat outlined dense").classes("bg-white text-xs")

                with ui.element("div").classes("flex flex-col w-full py-2 text-gray-700"):
                    ui.label("Password").classes("text-sm text-left")
                    ui.input(placeholder="Your Password").props("flat outlined dense").classes("bg-white text-xs")
                    ui.button("Submit").props("no-caps flat dense").classes("bg-red-600 text-white hover:bg-red-500 rounded-md my-4 py-2 px-4")
                    
                    # Terms & Privacy notice
                    ui.label().classes("text-sm text-center text-gray-700")
                    ui.html(
                        content=(
                            'By signing up, you agree to our '
                            '<span class="text-red-600">Terms of Service</span> and '
                            '<span class="text-red-600">Privacy Policy</span>.'
                        )
                    ).classes("text-sm text-center")

        # Footer 
        with ui.row().classes("flex flex-col md:flex-row items-center justify-center px-7 w-full bg-gray-50 py-4 text-sm md:mt-5 text-gray-700"):
            ui.label("© 2025 LifeLink. All rights reserved.").classes("mb-3 md:mb-0")
