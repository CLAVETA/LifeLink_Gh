from nicegui import ui, app

# components
from components.navbar import show_navbar
# from components.footer import show_footer


app.add_static_files("/assets", "assets")

def search_card():
    with ui.element("div").classes("flex items-center justify-center w-full px-4 -mt-10 relative z-10"):
        with ui.row().classes("bg-red-500 w-full text-white rounded-xl p-4 shadow-xl gap-4 items-end flex-wrap"):
            with ui.column().classes("w-full flex-1"):
                ui.label("Search for topics").classes("text-xs text-white mb-1")
                ui.select({"blood": "Blood Donation", "sickle cell": "Understanding sickle cell disease", "crisis": "Sickle cell management"}, with_input=True, value=None)\
                    .props("placeholder=Choose topic dense")\
                    .classes("w-full bg-white text-black rounded-md h-10")
            ui.button(icon="search", on_click=lambda: ui.notify("Searching topics..."))\
                .classes("h-10 w-10 rounded-md flex items-center justify-center text-white bg-red")\
                .style("background:#7C4DFF;")                

@ui.page("/user_education")
def education_page():
    # Setup for responsive design and removing default NiceGUI margins
    ui.add_head_html('<script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>')
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")
    
    with ui.element("main").classes("min-h-screen w-full flex flex-col"):
        
        # 1. Navbar: Highlight the 'Education' link
        show_navbar()
        
        # 2. Educational Banner Section
        # Uses the uploaded image path for the background
        with ui.element("section").classes("flex items-center justify-center w-full text-white bg-[url('/assets/educational_resources.png')] bg-cover bg-center bg-black/60 bg-blend-overlay"):
            with ui.column().classes("items-center w-full max-w-screen-lg text-center py-20 px-5"):
                ui.label("Educational Resources Hub").classes("text-3xl md:text-5xl font-bold mb-4")
                ui.label("Your Comprehensive centre for understanding blood donation and sickle cell disease").classes("text-base md:text-xl leading-relaxed")
        with ui.column().classes("flex items-center justify-center w-full"):
            search_card()


        # 3. Main Content Section (Expand Your Knowledge)
        with ui.element("section").classes("w-full py-16 px-5 md:px-20 max-w-screen-xl mx-auto"):
            # Sub-heading
            ui.label("Expand Your Knowledge").classes("text-2xl md:text-4xl font-bold text-gray-800 mb-12 text-center w-full")

            # Grid for two main topics, exactly matching the UI layout
            with ui.row().classes("grid grid-cols-1 lg:grid-cols-2 gap-10"):
                
                # A. Blood Donation Facts Card
                with ui.column().classes("w-full"):
                    with ui.card().classes('p-6 shadow-lg rounded-xl flex justify-center border border-gray-200 transform hover:scale-[1.02] transition-transform duration-300'):
                        ui.label("Blood Donation: What You Need To Know").classes("text-xl md:text-2xl font-semibold text-red-600 mb-4")
                        ui.image('/assets/edu_donation.png').classes('w-full h-1/2 object-cover rounded-md mb-4')
                                                    
        
                    # Key Facts
                        ui.label("Key Facts and Benefits:").classes("font-bold text-gray-800 mb-3")
                        for fact in [
                            "Eligibility criteria for donors (age, weight, health).",
                            "The entire process takes about an hour.",
                            "One donation can save up to three lives.",
                            "Blood is constantly needed as it has a short shelf life.",
                            "It's a free health check-up (blood pressure, hemoglobin, etc.)."
                        ]:
                            # Use Font Awesome for bullet points to match style
                            ui.html(f'<i class="fa-solid fa-circle-check text-red-500 mr-2"></i>{fact}', sanitize=False).classes("text-base text-gray-600 mb-2 flex items-start")
                        
                        ui.button("Find Donation Centers", on_click=lambda: ui.navigate.to('/donor_registration')).props("no-caps").classes("mt-6 w-full bg-red text-white rounded-md px-4 py-2 hover:bg-red transition")
                        ui.button("Get Comprehensive Guide", on_click=lambda: ui.navigate.to('/blooddonation_education')).props("no-caps").classes("mt-6 w-full bg-red text-white rounded-md px-4 py-2 hover:bg-red transition")

                # B. Sickle Cell Disease (SCD) Education Card
                with ui.column().classes("w-full"):
                    with ui.card().classes('p-6 shadow-lg rounded-xl flex justify-center border border-gray-200 transform hover:scale-[1.02] transition-transform duration-300'):
                        ui.label("Understanding Sickle Cell Disease").classes("text-xl md:text-2xl font-semibold text-red-600 mb-4")
                        ui.image('/assets/educational_resources.png').classes('md:w-full h-64 md:h-auto object-cover rounded-md mb-4')                                                    
                        
                                     
                        # Key Information
                        ui.label("What is SCD?").classes("font-bold text-gray-800 mb-2")
                        ui.label("Sickle cell disease is an inherited group of disorders where red blood cells are misshapen (sickle-shaped). These cells break down easily, leading to anemia, pain, and other complications.").classes("text-base text-gray-600 mb-4")
                        
                        ui.label("Treatment and Management:").classes("font-bold text-gray-800 mb-2")
                        for treatment in [
                            "Blood transfusions are crucial for managing severe anemia and complications.",
                            "Pain management and preventative care.",
                            "Bone marrow transplants (in some cases).",
                        ]:
                            # Use Font Awesome for bullet points
                            ui.html(f'<i class="fa-solid fa-square-poll-vertical text-red-500 mr-2"></i>{treatment}', sanitize=False).classes("text-base text-gray-600 mb-2 flex items-start")
                            
                        ui.button("Get Comprehensive Guide", on_click=lambda: ui.navigate.to('/sicklecell_education')).props("no-caps").classes("mt-6 w-full bg-red text-white rounded-md px-4 py-2 hover:bg-red-500 transition")

            ui.button("Load more resources", on_click=lambda: ui.notify("Loading more topics...")).props("no-caps").classes("mt-6 w-full bg-red text-white rounded-md px-4 py-2 hover:bg-gray-500 transition")        


        # 4. Footer (Consistent with the style used in the other pages)
        with ui.row().classes("flex flex-col md:flex-row items-center justify-between px-7 w-full bg-gray-50 py-5 text-sm mt-auto text-gray-500"):
            ui.label("© 2025 LifeLink. All rights reserved.").classes("mb-3 md:mb-0")
            with ui.row().classes("gap-6"):
                ui.html('<i class="fa-brands fa-square-linkedin text-xl hover:text-red-600 transition"></i>', sanitize=False)
                ui.html('<i class="fa-brands fa-instagram text-xl hover:text-red-600 transition"></i>', sanitize=False)
                ui.html('<i class="fa-brands fa-facebook text-xl hover:text-red-600 transition"></i>', sanitize=False)
