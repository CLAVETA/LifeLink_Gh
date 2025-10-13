from nicegui import ui, app

@ui.page("/about")
def about_page():
    ui.add_head_html('<script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>')
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")
    with ui.element("main").classes("min-h-screen w-full flex flex-col"):
        # Navbar
        with ui.row().classes("flex flex-col md:flex-row items-center justify-between shadow-md w-full px-3 md:px-7 py-1"):
            with ui.row().classes("gap-0 space-x-0 items-center justify-center"):
                ui.image("/assets/logo.png").classes("w-12 h-12")
                ui.link("LifeLink GH","/").classes("no-underline text-xl font-bold text-gray-700")
            with ui.row().classes("gap-6 mt-3 md:mt-0"):
                ui.link("Home","/").classes("no-underline text-gray-700 hover:text-red-600 transition")
                ui.link("About","/about").classes("no-underline text-red-600 hover:text-red-500 transition")
                ui.link("Contact").classes("no-underline text-gray-700 hover:text-red-600 transition")
            with ui.row().classes("gap-3 mt-3 md:mt-0"):
                ui.button("Donate Now", on_click=lambda: ui.navigate.to("/donor_registration")).props("no-caps flat dense").classes("bg-red-600 text-white rounded-md px-4")
        
        # Hero Section (About LifeLink)
        with ui.element("section").classes("flex flex-col items-center justify-center w-full py-10 px-5 text-center"):
            ui.label("About LifeLink").classes("text-2xl md:text-4xl font-bold text-gray-800 mb-4")
            ui.html(
                content=(
                    "Connecting donors, saving lives. We are dedicated to ensuring a stable blood supply for<br>"
                    "those in need and raising awareness about sickle cell disease<br>"
                ), sanitize=False).classes("text-base md:text-lg text-gray-500")

       # Mission & Vision 
            with ui.row().classes("px-5 py-12 md:mx-20 grid grid-cols-1 md:grid-cols-2 gap-10 items-start text-center justify-center"):
                with ui.column().classes("text-left flex flex-col md:items-start"):
                    ui.label("Our Mission").classes("text-xl md:text-2xl font-semibold text-gray-800 mb-2")
                    ui.html(
                        content=(
                            "To bridge the gap between blood donors and<br>"
                            "hospitals, ensuring timely access to life-saving blood<br>"
                            "for patients in need, especially those with sickle cell<br>"
                            "disease. We aim to educate the public about blood<br>"
                            "donation and sickle cell disease, fostering a<br>"
                            "community of informed and active donors<br>"
                        ),
                        sanitize=False,
                    ).classes("text-base md:text-lg text-gray-500 md:text-left")

                with ui.column().classes("text-left flex flex-col md:items-start"):
                    ui.label("Our Vision").classes("text-xl md:text-2xl font-semibold text-gray-800 mb-2")
                    ui.html(
                        content=(
                            "To create a world where every patient has access to<br>"
                            "the blood they need, regardless of their location or<br>"
                            "circumstances. We envision a future where sickle cell<br>"
                            "disease is effectively managed through early<br>"
                            "diagnosis, comprehensive care, and readily available<br>"
                            "blood transfusions.<br>"
                        ),
                        sanitize=False,
                    ).classes("text-base md:text-lg text-gray-500  md:text-left")

        # Stats Section
        with ui.column().classes("w-full items-center py-16 bg-gray-50"):
            ui.label("Our Impact").classes("text-xl md:text-3xl font-bold text-gray-800 mb-8 text-center")
            with ui.row().classes("grid grid-cols-1 md:grid-cols-3 gap-6 w-full px-5 md:px-7 max-w-screen-lg mx-auto"):
                with ui.card().classes("flex flex-col items-center p-6 shadow rounded-md"):
                    ui.label("1,500+").classes("text-2xl md:text-4xl font-bold text-red-500")
                    ui.label("Lives Saved").classes("text-sm md:text-base text-gray-500")
                with ui.card().classes("flex flex-col items-center p-6 shadow rounded-md"):
                    ui.label("5,000+").classes("text-2xl md:text-4xl font-bold text-red-500")
                    ui.label("Blood Units Donated").classes("text-sm md:text-base text-gray-500")
                with ui.card().classes("flex flex-col items-center p-6 shadow rounded-md"):
                    ui.label("20+").classes("text-2xl md:text-4xl font-bold text-red-500")
                    ui.label("Hospitals Supported").classes("text-sm md:text-base text-gray-500")

        # Our Team
        with ui.element("section").classes("w-full py-16 px-5 md:px-15"):
            ui.label("Our Team").classes("text-xl md:text-3xl font-bold text-gray-800 mb-8 text-center")
            with ui.row().classes("grid grid-cols-1 md:grid-cols-3 gap-8 max-w-screen-lg mx-auto"):
                for member in [
                    {"name": "Elizabeth N. Akossey", "role": "Frontend Developer", "img": "/assets/Elizabeth.jpg"},
                    {"name": "Shammah Akua Agyare", "role": "Frontend Developer", "img": "/assets/Akua.png"},
                    {"name": "Victoria Ewusiwaa Wilson Sey", "role": "Backend Developer", "img": "/assets/Victoria.png"},
                    {"name": "Claudia Agyeere", "role": "Backend Developer", "img": "/assets/Claudia.png"},
                    {"name": "Mary Worde", "role": "Backend Developer", "img": "/assets/Mary.png"},
                    {"name": "Rachael Kuranchie", "role": "Supervisor", "img": "/assets/Rachael.png"}
                ]:
                    with ui.column().classes("items-center text-center"):
                        ui.image(member["img"]).classes("w-35 h-35 object-cover rounded-full shadow-md mb-3")
                        ui.label(member["name"]).classes("font-semibold text-gray-800")
                        ui.label(member["role"]).classes("text-sm text-gray-500")

        # Our Partners
        with ui.element("section").classes("w-full py-16 bg-gray-50 px-5 md:px-20"):
            ui.label("Our Partners").classes("text-xl md:text-3xl font-bold text-gray-800 mb-8 text-center")
            with ui.row().classes("grid grid-cols-2 md:grid-cols-4 gap-6 max-w-screen-lg mx-auto items-center"):
                for partner in [
                    "/assets/GHS.jpg",
                    "/assets/bloodbank.jpg",
                    "/assets/ridgehospital.jpg",
                    "/assets/korlebu.jpg",
                ]:
                    ui.image(partner).classes("w-32 h-37 object-contain mx-auto")

       # Contact Section
        with ui.element("section").classes("w-full py-20 px-10 md:px-20 bg-white"):
            with ui.row().classes("w-full flex flex-col md:flex-row justify-center items-start gap-10 md:gap-20"):
                
                # --- Left Side: Text Content ---
                with ui.column().classes("w-full md:w-5/12 text-left md:pl-10"):
                    ui.label("GET IN TOUCH").classes("text-xl md:text-3xl font-extrabold text-gray-900 tracking-wide")
                    ui.element("div").classes("w-20 h-1 bg-red-600 my-3")
                    ui.label(
                        "We’d love to hear from you. Whether you’re a donor, hospital, or volunteer, reach out to us — together, we can save lives."
                    ).classes("text-gray-600 text-sm md:text-base leading-relaxed mb-2")
                    
                    ui.label(
                        "Your questions, feedback, or support can make a real difference. Drop us a message, and our team will get back to you soon."
                    ).classes("text-gray-500 text-sm md:text-base leading-relaxed")

                # --- Right Side: Form ---
                with ui.column().classes("w-full md:w-6/12 bg-white shadow-sm rounded-md items-center p-8"):
                    ui.input(placeholder="Name").props("outlined dense").classes("w-full mb-2 text-sm")

                    ui.input(placeholder="Email").props("outlined dense").classes("w-full mb-2 text-sm")

                    ui.input(placeholder="Phone Number").props("outlined dense").classes("w-full mb-2 text-sm")

                    ui.textarea(placeholder="Type your message here...").props("outlined").classes("w-full h-20 mb-3 text-sm")

                    ui.button("SEND MESSAGE").props("no-caps dense flat").classes(
                        "bg-red-600 hover:bg-red-700 text-white font-semibold text-sm px-6 py-2 rounded-md transition mt-10"
                    )

        
        # Footer
        with ui.row().classes("flex flex-col md:flex-row items-center justify-between px-7 w-full bg-gray-50 py-5 text-sm mt-auto text-red-300"):
            ui.label("© 2025 LifeLink. All rights reserved.").classes("mb-3 md:mb-0")
            with ui.row().classes("gap-6"):
                ui.html('<i class="fa-brands fa-square-linkedin"></i>', sanitize=False)
                ui.html('<i class="fa-brands fa-instagram"></i>', sanitize=False)
                ui.html('<i class="fa-brands fa-facebook"></i>', sanitize=False)
