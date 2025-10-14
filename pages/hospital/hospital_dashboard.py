from nicegui import ui,app

app.add_static_files("/assets","assets")

@ui.page("/hospital/dashboard")
def hospital_dashboard_page():
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")
    with ui.element("main").classes("min-h-screen w-full flex flex-col"):
        # Navbar
        with ui.row().classes("flex flex-col md:flex-row items-center justify-between shadow-md w-full px-3 md:px-7 py-1"):
            with ui.row().classes("gap-2 items-center justify-center"):
                ui.image("/assets/logo.png").classes("w-12 h-12")
                ui.link("LifeLink GH","/").classes("no-underline text-xl font-bold text-gray-700")
            with ui.row().classes("gap-6 mt-3 md:mt-0"):
                ui.link("About","/about").classes("no-underline text-gray-700 hover:text-red transition")
                ui.link("Education","/education").classes("no-underline text-gray-700 hover:text-red transition")
                ui.link("Contact").classes("no-underline text-gray-700 hover:text-red transition")
                ui.link("FAQs").classes("no-underline text-gray-700 hover:text-red transition")
            with ui.row().classes("gap-4 items-center"):
                ui.icon("notifications").classes("text-gray-700 text-2xl cursor-pointer")
                ui.image("/assets/hero2.png").classes("w-10 h-10 rounded-full object-cover")

        # main for request and donor matches
        with ui.row().classes("flex flex-col md:flex-row justify-center gap-6 w-full px-2 py-6"):
            # Blood Request Form Card 
            with ui.card().classes("w-full md:w-1/4 p-6 bg-white shadow-md rounded-md"):
                ui.label("Blood Request Form").classes("text-xl font-bold text-gray-700 mb-2")

                # Blood Type selector
                with ui.element("div").classes("flex flex-col mb-2 w-full"):
                    ui.label("Blood Type").classes("text-sm text-left")
                    ui.select(
                        ["Select Blood Type","A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                        value="Select Blood Type"
                    ).props("outlined dense").classes("bg-red-50 text-xs")

                # Urgency selector
                with ui.element("div").classes("flex flex-col mb-2 w-full"):
                    ui.label("Urgency").classes("text-sm text-left")
                    ui.select(
                        ["Urgent", "Not Urgent"],
                        value="Urgent"
                    ).props("outlined dense").classes("bg-red-50 text-xs")

                # Quantity
                with ui.element("div").classes("flex flex-col mb-2 w-full"):
                    ui.label("Quantity (Units)").classes("text-sm text-left")
                    ui.input(placeholder="Enter Quantity").props("flat outlined dense").classes("bg-red-50 text-xs")

                # Patient Condition textarea
                with ui.element("div").classes("flex flex-col mb-2 w-full"):
                    ui.label("Patient Condition").classes("text-sm text-left")
                    ui.textarea(placeholder="Describe Patient Condition").props("outlined").classes("bg-red-50 rounded-md text-xs")

                # Broadcast Button
                ui.button("Broadcast Request").props("no-caps flat dense").classes("bg-red-600 text-white hover:bg-red-500 rounded-md py-2 px-4 w-full")
            
            # Donor Matches Card (Left, wider card ~60%)
            with ui.card().classes("w-full md:w-3/5 p-6 bg-white shadow-md rounded-md"):
                ui.label("Donor Matches").classes("text-xl font-bold text-gray-700 mb-2")

                # Search, Blood Type, Distance row
                with ui.row().classes("grid grid-cols-1 md:grid-cols-5 gap-4 w-full"):
                    with ui.element("div").classes("flex flex-col col-span-3"):
                        ui.label("Search").classes("text-sm text-left")
                        ui.input(placeholder="🔍 Search donors by name, location").props("flat outlined dense").classes("bg-red-50 text-xs rounded-md")

                    # Blood Type filter (smaller, equal size)
                    with ui.element("div").classes("flex flex-col col-span-1"):
                        ui.label("Blood Type").classes("text-sm text-left")
                        ui.select(
                            ["All", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                            value="All"
                        ).props("outlined dense").classes("bg-red-50 text-xs rounded-md")

                    # Distance filter (smaller, equal size)
                    with ui.element("div").classes("flex flex-col col-span-1"):
                        ui.label("Distance").classes("text-sm text-left")
                        ui.input(placeholder="Enter distance (km)").props("flat outlined dense").classes("bg-red-50 text-xs rounded-md")

                # Header row for donor table
                with ui.row().classes("grid grid-cols-5 gap-4 w-full bg-red-50 text-gray-700 font-semibold text-sm mt-3 p-2"):
                    ui.label("DONOR NAME").classes("text-center")
                    ui.label("BLOOD TYPE").classes("text-center")
                    ui.label("DISTANCE").classes("text-center")
                    ui.label("AVAILABILITY").classes("text-center")
                    ui.label("PROFILE").classes("text-center")

        # Map & Request History
        with ui.row().classes("flex flex-col md:flex-row justify-center gap-6 w-full px-4 py-6"):
            # Blood Request Form Card 
            with ui.card().classes("w-full md:w-1/4 p-6 bg-white shadow-md rounded-md"):
                ui.label("Nearby Donors").classes("text-xl font-bold text-gray-700 mb-2")
                ui.html(
                    """
                    <iframe
                        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3915.40477804116!2d-0.195!3d5.55!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2z5L2c5ZOB5aSn!5e0!3m2!1sen!2sgh!4v1633871595096!5m2!1sen!2sgh"
                        width="100%" height="200" style="border:0; border-radius: 12px;" allowfullscreen=""
                        loading="lazy"
                    ></iframe>
                    """, sanitize=False
                ).classes("w-full h-50 rounded-md overflow-hidden")
            with ui.card().classes("w-full md:w-3/5 p-6 bg-white shadow-md rounded-md"):
                ui.label("Request History").classes("text-xl font-bold text-gray-700 mb-2")
                with ui.row().classes("grid grid-cols-5 gap-2 w-full bg-red-50 text-gray-800 font-semibold rounded-md px-2 py-2 text-sm"):
                    ui.label("REQUEST ID").classes("text-center")
                    ui.label("BLOOD TYPE").classes("text-center")
                    ui.label("QUANTITY").classes("text-center")
                    ui.label("STATUS").classes("text-center")
                    ui.label("DATE").classes("text-center")
        
        # Footer
        with ui.row().classes("flex flex-col md:flex-row items-center justify-between px-7 w-full bg-gray-50 py-5 text-sm text-gray-700 mt-auto"):
            ui.label("© 2025 LifeLink. All rights reserved.").classes("mb-3 md:mb-0")
            with ui.row().classes("gap-6"):
                ui.link("About").classes("no-underline text-gray-700 transition")
                ui.link("Contact").classes("no-underline hover:text-white text-gray-700 transition")
                ui.link("Privacy Policy").classes("no-underline text-gray-700 transition")
                


