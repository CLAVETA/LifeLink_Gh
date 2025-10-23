from nicegui import ui

def donor_footer():
    with ui.row().classes("flex flex-col md:flex-row items-center justify-between px-7 w-full bg-gray-50 py-5 text-sm mt-auto text-gray-500"):
            ui.image("/assets/logo.png").classes("w-24 h-20") 
            ui.label("© 2025 LifeLink. All rights reserved.").classes("mb-3 md:mb-0 text-xl hover:text-red")
            with ui.row().classes("gap-3"):
                ui.link("About","/about").classes("no-underline text-gray-700 hover:text-red transition text-xl")
                ui.link("Contact","/about#contact").classes("no-underline hover:text-red text-gray-700 text-xl transition")
                ui.link("Privacy Policy").classes("no-underline text-gray-700 hover:text-red transition text-xl")            
            with ui.row().classes("gap-6"):
                ui.html('<i class="fa-brands fa-square-linkedin text-xl hover:text-red-600 transition"></i>', sanitize=False)
                ui.html('<i class="fa-brands fa-instagram text-xl hover:text-red-600 transition"></i>', sanitize=False)
                ui.html('<i class="fa-brands fa-facebook text-xl hover:text-red-600 transition"></i>', sanitize=False)
