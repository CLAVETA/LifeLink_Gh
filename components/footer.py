from nicegui import ui


def show_footer():
    ui.add_head_html('<script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>')
    with ui.row().classes("flex flex-col md:flex-row items-center justify-between px-7 w-full bg-gray-50 py-5 text-sm text-gray-700 mt-auto"):
            ui.label("© 2025 LifeLink. All rights reserved.").classes("mb-3 md:mb-0")
            with ui.row().classes("gap-6"):
                ui.link("About","/about").classes("no-underline text-gray-700 transition")
                ui.link("Contact").classes("no-underline hover:text-white text-gray-700 transition")
                ui.link("Privacy Policy").classes("no-underline text-gray-700 transition")
                ui.link("FAQs").classes("no-underline text-gray-700 transition")
            # with ui.row().classes("gap-6"):
            #     ui.html('<i class="fa-brands fa-square-linkedin text-xl hover:text-red-600 transition"></i>', sanitize=False)
            #     ui.html('<i class="fa-brands fa-instagram text-xl hover:text-red-600 transition"></i>', sanitize=False)
            #     ui.html('<a href="https://facebookcom" target='_blank'><i class="fa-brands fa-facebook text-xl hover:text-red-600 transition"></i></a>', sanitize=False)
                # Social Media Icons
            with ui.row().classes("gap-4 text-xl"):
                with ui.link('https://www.linkedin.com', target='_blank').classes("text-red").style("text-decoration: none"):
                    ui.html('<i class="fa-brands fa-square-linkedin text-xl hover:text-red-600 transition"></i>', sanitize=False)
                with ui.link('https://www.instagram.com', target='_blank').classes("text-red").style("text-decoration: none"):
                    ui.html('<i class="fa-brands fa-instagram text-xl hover:text-red-600 transition"></i>', sanitize=False)
                with ui.link('https://www.facebook.com', target='_blank').classes("text-red").style("text-decoration: none"):
                    ui.html('<i class="fa-brands fa-facebook text-xl hover:text-red-600 transition"></i>', sanitize=False)          
                      