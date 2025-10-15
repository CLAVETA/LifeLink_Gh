from nicegui import ui,app,run
import requests
from utils.api import base_url

app.add_static_files("/assets","assets")


_login_btn: ui.button = None


def _run_login(data):
    return requests.post(f"{base_url}/users/login", data=data)


async def _login(data):
    # print(data)
    _login_btn.props(add="disable loading")
    response = await run.cpu_bound(_run_login, data)
    print(response.status_code, response.content)
    _login_btn.props(remove="disable loading")
    if response.status_code == 200:
        json_data = response.json()
        # app.storage.user["access_token"] = json_data["access_token"]
        ui.notify("Login successful!", color="positive")
        return ui.navigate.to("/donor/dashboard")


@ui.page("/donor/login")
def donor_login_page():
    global _login_btn
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")
    with ui.element("main").classes("min-h-screen w-full flex flex-col"):
        # Navbar
        with ui.row().classes("flex flex-col md:flex-row items-center justify-between shadow-md w-full px-3 md:px-7 py-1"):
            with ui.row().classes("gap-0 items-center justify-center"):
                ui.image("/assets/logo.png").classes("w-12 h-12")
                ui.link("LifeLink GH","/").classes("no-underline text-xl font-bold text-gray-700")
            with ui.row().classes("gap-6 mt-3 md:mt-0"):
                ui.link("About","/about").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("How it works").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("Contact").classes("no-underline text-gray-700 hover:text-red-500 transition")
            with ui.row().classes("gap-3 mt-3 md:mt-0"):
                ui.button("Donor Login").props("no-caps flat dense").classes("bg-red-600 text-white hover:bg-red-500 rounded-md px-4")
        # Signin form 
        with ui.element("section").classes("flex-grow flex items-center justify-center w-full px-4 md:mt-5"):
            with ui.card().classes("w-full md:w-[60%] lg:w-[50%] p-6 bg-white shadow-md items-center rounded-md"):
                ui.label("Sign in to your account").classes("text-xl md:text-2xl font-bold text-center")

                with ui.element("div").classes("flex flex-col w-full pt-5 pb-2 text-gray-700"):
                    ui.label("Donor Name").classes("text-sm text-left")
                    ui.input(placeholder="Your Name").props("flat outlined dense").classes("rounded-sm bg-white text-xs")


                with ui.element("div").classes("flex flex-col w-full text-gray-700"):
                    ui.label("Email Address").classes("text-sm text-left ")
                    email = ui.input(placeholder="Your Email").props("flat outlined dense").classes("bg-white text-xs")
                
                with ui.element("div").classes("flex flex-col w-full py-2 text-gray-700"):
                    ui.label("Password").classes("text-sm text-left")
                    password = ui.input(placeholder="Your Password",password=True,
                        password_toggle_button=True,).props("flat outlined dense").classes("bg-white text-xs")
                    _login_btn = (ui.button("Login as donor",on_click=lambda:_login(data={"email": email.value,"password": password.value })).props("no-caps flat dense").classes("bg-red-600 text-white hover:bg-red-500 rounded-md my-4 py-2 px-4"))
                    
                    # Sign up link
                    with ui.row().classes("items-center justify-center space-x-1 gap-0 m-0 p-0"):
                        ui.label("Don't have an account?")
                        ui.link("Sign up", "/donor/register").classes("no-underline text-red-600")

        # Footer 
        with ui.row().classes("flex flex-col md:flex-row items-center justify-center px-7 w-full bg-gray-50 py-4 text-sm md:mt-5 text-gray-700"):
            ui.label("© 2025 LifeLink. All rights reserved.").classes("mb-3 md:mb-0")