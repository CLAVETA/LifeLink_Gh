from nicegui import ui

def donor_header():
    # with ui.row().classes("flex flex-col md:flex-row items-center justify-between shadow-md w-full px-3 md:px-7 py-3"):
            with ui.row().classes("gap-0 space-x-0 items-center justify-center"):
                ui.image("/assets/logo.png").classes("w-12 h-12")
                # ui.label("LifeLink GH").classes("text-xl font-bold text-gray-700")
                ui.link("LifeLink GH","/").classes("no-underline text-xl font-bold text-gray-700")
            ui.space()
            with ui.row().classes("gap-6 mt-3 md:mt-0"):
                # ui.link("Home","/").classes("no-underline text-gray-700 hover:text-red transition")
                ui.link("About","/about").classes("no-underline text-gray-700 hover:text-red transition")
                ui.link("Education","/education").classes("no-underline text-gray-700 hover:text-red transition")
                ui.link("Contact", "/contact").classes("no-underline text-gray-700 hover:text-red transition")
                ui.link("FAQs", "/").classes("no-underline text-gray-700 hover:text-red transition")
            ui.space()
            ui.button("Donate Now", on_click=lambda: ui.navigate.to("/donor/dashboard")).props("no-caps flat dense").classes("bg-red-600 text-white hover:bg-red-500 rounded-md px-4")
            with ui.button(icon='person', color='primary').props('flat round'):
                with ui.menu():
                    ui.menu_item('Dashboard', on_click=lambda: ui.navigate.to("/donor/dashboard")).props('icon=dashboard')
                    ui.menu_item('Find a Drive', on_click=lambda: ui.navigate.to("/donor/dashboard")).props('icon=search')
                    ui.menu_item('My Impact', on_click=lambda: ui.navigate.to("/donor/dashboard")).props('icon=heart') # Placeholder
                    ui.menu_item('My Profile', on_click=lambda: ui.navigate.to("/donor/profile")).props('icon=account_circle')
                    ui.menu_item('Logout', on_click=lambda: ui.navigate.to("/donor/login")).props('icon=logout')
                    ui.menu_item('Settings').props('icon=settings')
                        # ui.menu_item('Theme', on_click=dark_mode.toggle).props('icon=lightbulb')
         
    