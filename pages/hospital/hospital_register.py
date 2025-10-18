from nicegui import ui,app,run
import requests
from utils.api import base_url

app.add_static_files("/assets","assets")

_register_btn: ui.button = None

def _run_register(data):
    return requests.post(f"{base_url}/hospitals/register", data=data)


async def _register(data):
    _register_btn.props(add="disable loading")
    response = await run.cpu_bound(_run_register, data)
    print(response.status_code, response.content)
    _register_btn.props(remove="disable loading")
    if response.status_code == 201:
        return ui.navigate.to("/hospital/login")
    elif response.status_code == 409:
        return ui.notify(message="User already exits!", type="warning")


@ui.page("/hospital/register")
def hospital_signup_page():
    global _register_btn
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")
    with ui.element("main").classes("min-h-screen w-full flex flex-col"):
        # Navbar
        with ui.row().classes("flex flex-col md:flex-row items-center justify-between shadow-sm w-full px-3 md:px-7 py-1 border-b border-red-100"):
            with ui.row().classes("gap-0 items-center justify-center"):
                ui.image("/assets/logo.png").classes("w-12 h-12")
                ui.link("LifeLink GH","/").classes("no-underline text-xl font-bold text-gray-700")
            with ui.row().classes("gap-6 mt-3 md:mt-0"):
                ui.link("About","/about").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("How it works").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("Contact").classes("no-underline text-gray-700 hover:text-red-500 transition")
            with ui.row().classes("gap-3 mt-3 md:mt-0"):
                ui.button("Hospital Login",on_click=lambda: ui.navigate.to("/hospital/login")).props("no-caps flat dense").classes("bg-pink-200 text-red hover:bg-red-200 rounded-md px-4")
        # Signup form 
        with ui.element("section").classes("flex-grow flex items-center justify-center w-full px-4 md:mt-5"):
            with ui.card().classes("w-full md:w-[60%] lg:w-[40%] p-6 bg-white shadow-md items-center rounded-md"):
                ui.label("Register as Hospital").classes("text-xl md:text-2xl font-bold text-center")
                with ui.row().classes("items-center justify-center text-sm space-x-1 gap-0 m-0 p-0"):
                    ui.label("Already have an account?")
                    ui.link("Log in", "/hospital/login").classes("no-underline text-red-600")

                with ui.element("div").classes("flex flex-col w-full pt-5 pb-2 text-gray-700"):
                    ui.label("Hospital Name").classes("text-sm text-left")
                    hospital_name = ui.input(placeholder="Your Name").props("flat outlined dense").classes("rounded-sm bg-white text-xs")

                with ui.element("div").classes("flex flex-col w-full text-gray-700"):
                    ui.label("Location").classes("text-sm text-left ")
                    location = ui.input(placeholder="Your Location").props("flat outlined dense").classes("bg-white text-xs")


                with ui.element("div").classes("flex flex-col w-full text-gray-700"):
                    ui.label("Email Address").classes("text-sm text-left ")
                    email = ui.input(placeholder="Your Email").props("flat outlined dense").classes("bg-white text-xs")
                
                with ui.element("div").classes("flex flex-col w-full py-2 text-gray-700"):
                    ui.label("Password").classes("text-sm text-left")
                    password = ui.input(placeholder="Your Password",password=True,
                        password_toggle_button=True,).props("flat outlined dense").classes("bg-white text-xs")
                    _register_btn = (ui.button("Submit",on_click=lambda: _register(
                            {
                                "hospital_name": hospital_name.value,
                                "location_address": location.value,
                                "email": email.value,
                                "password": password.value,
                            }
                        ),
                        ).props("no-caps flat dense").classes("bg-red-600 text-white hover:bg-red-500 rounded-md my-4 py-2 px-4"))
                    
                    # Terms & Privacy notice
                    ui.label().classes("text-sm text-center text-gray-700")
                    ui.html(
                        content=(
                            'By signing up, you agree to our '
                            '<span class="text-red-600">Terms of Service</span> and '
                            '<span class="text-red-600">Privacy Policy</span>.'
                        ), sanitize=False
                    ).classes("text-sm text-center")

        # Footer 
        with ui.row().classes("flex flex-col md:flex-row items-center justify-center px-7 w-full bg-gray-50 py-4 text-sm md:mt-5 text-gray-700 border-t border-red-100"):
            ui.label("© 2025 LifeLink. All rights reserved.").classes("mb-3 md:mb-0")
