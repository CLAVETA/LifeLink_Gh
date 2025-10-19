from nicegui import ui,app,run
from utils.api import base_url
import requests

app.add_static_files("/assets","assets")


_register_btn: ui.button = None

def _run_register(data):
    return requests.post(f"{base_url}/volunteers/register", data=data)


async def _register(data):
    _register_btn.props(add="disable loading")
    response = await run.cpu_bound(_run_register, data)
    print(response.status_code, response.content)
    _register_btn.props(remove="disable loading")
    if response.status_code == 201:
        return ui.navigate.to("/volunteer/login")
    elif response.status_code == 409:
        return ui.notify(message="User already exits!", type="warning")


@ui.page("/volunteer_signup")
def volunteer_signup_page():
    global _register_btn
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")

    with ui.element("main").classes("min-h-screen w-full flex flex-col"):
        # Navbar
        with ui.row().classes(
            "flex flex-col md:flex-row items-center justify-between shadow-sm w-full px-3 md:px-7 py-1 border-b border-red-100"
        ):
            with ui.row().classes("gap-0 items-center justify-center"):
                ui.image("/assets/logo.png").classes("w-12 h-12")
                ui.link("LifeLink GH","/").classes("no-underline text-xl font-bold text-gray-700")
            with ui.row().classes("gap-6 mt-3 md:mt-0"):
                ui.link("About","/about").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("How it works").classes("no-underline text-gray-700 hover:text-red-500 transition")
                ui.link("Contact","/about#contact").classes("no-underline text-gray-700 hover:text-red-500 transition")
            with ui.row().classes("gap-3 mt-3 md:mt-0"):
                ui.button("Register",on_click=lambda: ui.navigate.to("/volunteer_signup")).props("no-caps flat dense").classes("bg-red-600 text-white hover:bg-red-500 rounded-md px-4")
                ui.button("Login",on_click=lambda:ui.navigate.to("/volunteer/login")).props("no-caps flat dense").classes("bg-pink-200 text-red hover:bg-pink-300 rounded-md px-4")
        # Signup form 
        with ui.element("section").classes("flex-grow flex items-center justify-center w-full px-4"):
            with ui.card().classes("w-full md:w-[60%] lg:w-[50%] p-6 bg-white text-gray-700 rounded-md items-center my-3 shadow-none border-none"):
                ui.label("Become a Volunteer").classes("text-2xl font-bold text-center m-0 p-0 text-black")
                ui.label("Join our community and make a difference. Your help is vital.").classes("text-sm text-center text-gray-700 mb-4")

                # Full Name
                with ui.element("div").classes("flex flex-col w-full mb-2"):
                    ui.label("Full Name").classes("text-sm text-left")
                    fullname = ui.input(placeholder="Enter your full name").props("flat outlined border-red dense").classes("rounded-sm bg-white text-xs")

                # Location
                with ui.element("div").classes("flex flex-col w-full mb-2"):
                    ui.label("Location").classes("text-sm text-left")
                    location = ui.input(placeholder="eg., City, State").props("flat outlined dense").classes("rounded-sm bg-white text-xs border-red-600")

                # Skills / Interests
                with ui.element("div").classes("flex flex-col w-full mb-2"):
                    ui.label("Skills / Interests").classes("text-sm text-left")
                    ui.label("Choose the areas where you'd like to contribute.").classes("text-xs text-gray-600 mb-2")
                    with ui.row().classes("gap-6"):
                        skills = ui.select(
                            options=["Awareness Campaigns", "Education & Outreach", "Event Organization"],
                            label="Areas of Involvement",
                        ).props("color=red").classes("text-sm w-72")


                # Contact Number
                with ui.element("div").classes("flex flex-col w-full mb-2"):
                    ui.label("Contact Number").classes("text-sm text-left")
                    phone_number = ui.input(placeholder="Enter your phone number").props("flat outlined dense").classes("rounded-sm bg-white text-xs border-red-600")

                # Email Address
                with ui.element("div").classes("flex flex-col w-full mb-2"):
                    ui.label("Email Address").classes("text-sm text-left")
                    email = ui.input(placeholder="you@example.com").props("flat outlined dense").classes("rounded-sm bg-white text-xs border-red-600")
                
                # Password
                with ui.element("div").classes("flex flex-col w-full mb-2"):
                    ui.label("Password").classes("text-sm text-left")
                    password = ui.input(placeholder="Your Password",password=True,
                        password_toggle_button=True,).props("flat outlined dense").classes("rounded-sm bg-white text-xs border-red-600")

                _register_btn = (ui.button("Register Now", on_click=lambda: _register(
                            {
                                "full_name": fullname.value,
                                "email": email.value,
                                "password": password.value,
                                "location": location.value,
                                "contact_number": phone_number.value,
                                "skills": skills.value,
                            }))).props("no-caps flat dense").classes(
                    "bg-red-600 text-white hover:bg-red-500 rounded-md my-4 py-2 px-4 w-full"
                )

        # Footer 
        with ui.element("div").classes("flex flex-col items-center justify-center px-7 w-full bg-gray-50 py-4 text-sm mt-auto text-gray-700 border-t border-red-100"):
            
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
