from nicegui import ui,app,run
from components.footer import show_footer
from utils.api import base_url
import requests

app.add_static_files("/assets","assets")

_register_btn: ui.button = None

def _run_register(data):
    return requests.post(f"{base_url}/donors/register", data=data)


async def _register(data):
    _register_btn.props(add="disable loading")
    response = await run.cpu_bound(_run_register, data)
    print(response.status_code, response.content)
    _register_btn.props(remove="disable loading")
    if response.status_code == 201:
        return ui.navigate.to("/donor/login")
    elif response.status_code == 409:
        return ui.notify(message="User already exits!", type="warning")


@ui.page("/donor_registration")
def donor_registration_page():
    global _register_btn
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")
    with ui.element("main").classes("min-h-screen w-full flex flex-col"):
        # Navbar
        with ui.row().classes(
            "flex flex-col md:flex-row items-center justify-between shadow-md w-full px-3 md:px-7 py-1"
        ):
            with ui.row().classes("gap-0 items-center justify-center"):
                ui.image("/assets/logo.png").classes("w-12 h-12")
                ui.link("LifeLink GH","/").classes("no-underline text-xl font-bold text-gray-700")
            with ui.row().classes("gap-6 mt-3 md:mt-0"):
                ui.link("About","/about").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("Education","/education").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("Contact","/about#contact").classes("no-underline text-gray-700 hover:text-red-500 transition")
            with ui.row().classes("gap-3 mt-3 md:mt-0"):
                ui.button("Hospital Login", on_click=lambda: ui.navigate.to("/hospital/login")).props("no-caps flat dense").classes("bg-pink-200 text-red hover:bg-pink-300 rounded-md px-4")
        # Signup form 
        with ui.element("section").classes("flex-grow flex items-center justify-center w-full px-4"):
            with ui.card().classes("w-full md:w-[60%] lg:w-[50%] p-6 bg-white shadow-md text-gray-700 rounded-md items-center my-3 border border-red-100"):
                ui.label("Register and Become a Lifesaver").classes("text-2xl font-bold text-center m-0 text-black")
                ui.label("Register as a blood donor and help save lives in your community").classes("text-sm text-center text-gray-700")
                with ui.row().classes("items-center justify-center text-sm space-x-1 gap-0 m-0 p-0"):
                    ui.label("Already have an account?")
                    ui.link("Log in", "/donor/login").classes("no-underline text-red-600")

                with ui.element("div").classes("grid grid-cols-1 md:grid-cols-1 gap-4 w-full"):
                    with ui.element("div").classes("flex flex-col w-full"):
                        ui.label("Full Name").classes("text-sm text-left")
                        fullname = ui.input().props("flat outlined dense").classes("rounded-sm bg-white text-xs")

                with ui.element("div").classes("grid grid-cols-1 md:grid-cols-2 gap-4 w-full"):
                    with ui.element("div").classes("flex flex-col w-full text-gray-700"):
                        ui.label("Email Address").classes("text-sm text-left")
                        email = ui.input().props("flat outlined dense").classes("bg-white text-xs")
                    
                    with ui.element("div").classes("flex flex-col w-full text-gray-700"):
                        ui.label("Password").classes("text-sm text-left")
                        password = ui.input(placeholder="Your Password",password=True,
                        password_toggle_button=True,).props("flat outlined dense").classes("bg-white text-xs")

                with ui.element("div").classes("grid grid-cols-1 md:grid-cols-2 gap-4 w-full py-2"):
                    with ui.element("div").classes("flex flex-col w-full"):
                        ui.label("Phone Number").classes("text-sm text-left")
                        phone_number = ui.input().props("flat outlined dense").classes("bg-white text-xs")

                    with ui.element("div").classes("flex flex-col w-full"):
                        ui.label("Blood Type").classes("text-sm text-left")
                        blood_type = ui.select(
                            ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                            value="A+",
                        ).props("outlined dense").classes("bg-white text-xs")

                with ui.element("div").classes("grid grid-cols-1 md:grid-cols-2 gap-4 w-full py-2"):
                    with ui.element("div").classes("flex flex-col w-full"):
                        ui.label("Date of Birth").classes("text-sm text-left")
                        dob = ui.input().props("type=date flat outlined dense").classes("bg-white text-xs")

                    with ui.element("div").classes("flex flex-col w-full"):
                        ui.label("City/Town").classes("text-sm text-left")
                        location = ui.input().props("flat outlined dense").classes("bg-white text-xs")

                # Register button
                _register_btn = (ui.button("Register Now", on_click=lambda: _register(
                            {
                                "full_name": fullname.value,
                                "email": email.value,
                                "password": password.value,
                                "phone_number": phone_number.value,
                                "blood_type": blood_type.value,
                                "date_of_birth": dob.value,
                                "location": location.value,
                            }))).props("no-caps flat dense").classes(
                    "bg-red-600 text-white hover:bg-red-500 rounded-md my-4 py-2 px-4 w-full"
                )

                # Terms & Privacy notice
                ui.html(
                    content=(
                        'By signing up, you agree to our '
                        '<span class="text-red-600">Terms of Service</span> and '
                        '<span class="text-red-600">Privacy Policy</span>.'
                    ), sanitize= False
                ).classes("text-sm text-center text-gray-700")


        # # Footer 
        show_footer()
        # with ui.row().classes("flex flex-col md:flex-row items-center justify-center px-7 w-full bg-gray-50 py-4 text-sm mt-auto text-gray-700"):
        #     ui.label("© 2025 LifeLink. All rights reserved.").classes("mb-3 md:mb-0")
