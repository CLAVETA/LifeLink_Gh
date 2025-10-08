from nicegui import ui, app

@ui.page("/about")
def about_page():
    ui.add_head_html('<script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>')
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")
    with ui.element("main").classes("min-h-screen w-full flex flex-col"):
        # Navbar
        with ui.row().classes("flex flex-col md:flex-row items-center justify-between shadow-md w-full px-3 md:px-7 py-3"):
            with ui.row().classes("gap-0 space-x-0 items-center justify-center"):
                ui.image("/assets/logo.png").classes("w-12 h-12")
                ui.label("LifeLink").classes("text-xl font-bold text-gray-700")
            with ui.row().classes("gap-6 mt-3 md:mt-0"):
                ui.link("Home","/").classes("no-underline text-gray-700 hover:text-red-600 transition")
                ui.link("About","/about").classes("no-underline text-red-600 hover:text-red-500 transition")
                ui.link("Contact").classes("no-underline text-gray-700 hover:text-red-600 transition")
            with ui.row().classes("gap-3 mt-3 md:mt-0"):
                ui.button("Donate Now").props("no-caps flat dense").classes("bg-red-600 text-white rounded-md px-4")
        
        # Hero Section (About LifeLink)
        with ui.element("section").classes("flex flex-col items-center justify-center w-full py-10 px-5 text-center"):
            ui.label("About LifeLink").classes("text-2xl md:text-4xl font-bold text-gray-800 mb-4")
            ui.html(
                content=(
                    "Connecting donors, saving lives. We are dedicated to ensuring a stable blood supply for<br>"
                    "those in need and raising awareness about sickle cell disease<br>"
                )).classes("text-base md:text-lg text-gray-500")

        # Mission & Vision
        with ui.row().classes("px-5 md:px-20 py-12 grid grid-cols-1 md:grid-cols-2 gap-10 items-start"):
            with ui.column().classes("text-center md:text-left"):
                ui.label("Our Mission").classes("text-xl md:text-2xl font-semibold text-gray-800 mb-2")
                ui.html(
                    content=(
                        "To bridge the gap between blood donors and<br>"
                        "hospitals, ensuring timely access to life-saving blood<br>"
                        "for patients in need, especially those with sickle cell<br>"
                        "disease. We aim to educate the public about blood<br>"
                        "donation and sickle cell disease, fostering a<br>"
                        "community of informed and active donors<br>"
                    )).classes("text-base md:text-lg text-gray-500")
            with ui.column().classes("text-center md:text-left"):
                ui.label("Our Vision").classes("text-xl md:text-2xl font-semibold text-gray-800 mb-2")
                ui.html(
                    content=(
                        "To create a world where every patient has access to<br>"
                        "the blood they need, regardless of their location or<br>"
                        "circumstances. We envision a future where sickle cell<br>"
                        "disease is effectively managed through early<br>"
                        "diagnosis, comprehensive care, and readily available<br>"
                        "blood transfusions.<br>"
                    )).classes("text-base md:text-lg text-gray-500")

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
        with ui.element("section").classes("w-full py-16 px-5 md:px-20"):
            ui.label("Our Team").classes("text-xl md:text-3xl font-bold text-gray-800 mb-8 text-center")
            with ui.row().classes("grid grid-cols-1 md:grid-cols-3 gap-8 max-w-screen-lg mx-auto"):
                for member in [
                    {"name": "Elizabeth Nuoma", "role": "Founder & Data Scientist", "img": "/assets/team1.jpg"},
                    {"name": "Kwame Mensah", "role": "Project Manager", "img": "/assets/team2.jpg"},
                    {"name": "Ama Serwaa", "role": "Frontend Developer", "img": "/assets/team3.jpg"},
                ]:
                    with ui.column().classes("items-center text-center"):
                        ui.image(member["img"]).classes("w-32 h-32 object-cover rounded-full shadow-md mb-3")
                        ui.label(member["name"]).classes("font-semibold text-gray-800")
                        ui.label(member["role"]).classes("text-sm text-gray-500")

        # Our Partners
        with ui.element("section").classes("w-full py-16 bg-gray-50 px-5 md:px-20"):
            ui.label("Our Partners").classes("text-xl md:text-3xl font-bold text-gray-800 mb-8 text-center")
            with ui.row().classes("grid grid-cols-2 md:grid-cols-4 gap-6 max-w-screen-lg mx-auto items-center"):
                for partner in [
                    "/assets/partner1.png",
                    "/assets/partner2.png",
                    "/assets/partner3.png",
                    "/assets/partner4.png",
                ]:
                    ui.image(partner).classes("w-32 h-16 object-contain mx-auto")

        # Contact Section
        with ui.element("section").classes("w-full py-16 px-5 md:px-20"):
            with ui.card().classes("md:mx-[25%] flex flex-col items-center justify-center px-5 bg-gray-40"):
                ui.label("Contact Us").classes("text-xl md:text-3xl font-bold py-1")
                with ui.element("div").classes("flex flex-col w-full py-2 md:px-[15%]"):
                    ui.label("Name").classes("text-xs text-left py-2")
                    ui.input(placeholder="Your Name").props("flat outlined dense").classes("rounded-sm bg-white text-xs")  
                with ui.element("div").classes("flex flex-col w-full  md:px-[15%]"):
                    ui.label("Email").classes("text-xs text-left py-2") 
                    ui.input(placeholder="Your Email").props("flat dense no-caps outlined").classes("bg-white")
                with ui.element("div").classes("flex flex-col w-full md:px-[15%]"):
                    ui.label("Message")
                    ui.textarea(placeholder="Type here...").props("outlined").classes("w-full")
                ui.button("Send Message").props("no-caps flat dense").classes("bg-red-600 text-white rounded-md px-4 mt-4")
        
        # Footer
        with ui.row().classes("flex flex-col md:flex-row items-center justify-between px-7 w-full bg-gray-50 py-5 text-sm mt-auto text-red-300"):
            ui.label("© 2025 LifeLink. All rights reserved.").classes("mb-3 md:mb-0")
            with ui.row().classes("gap-6"):
                ui.html('<i class="fa-brands fa-square-linkedin"></i>')
                ui.html('<i class="fa-brands fa-instagram"></i>')
                ui.html('<i class="fa-brands fa-facebook"></i>')
