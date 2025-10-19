from nicegui import ui, app

# components
from components.navbar import show_navbar
from components.footer import show_footer

app.add_static_files("/assets", "assets")
                

@ui.page("/sicklecell_education")
def sicklecell_page():
    # Setup for responsive design and removing default NiceGUI margins
    ui.add_head_html('<script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>')
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")
    
    with ui.element("main").classes("min-h-screen w-full flex flex-col"):
        
        # 1. Navbar: Highlight the 'Education' link
        show_navbar()
        
        # 2. Educational Banner Section
        # Uses the uploaded image path for the background
        with ui.element("section").classes("flex items-center justify-center w-full text-white bg-[url('/assets/educational_resources.jpg')] bg-cover bg-center bg-black/60 bg-blend-overlay"):
            with ui.column().classes("items-center w-full max-w-screen-lg text-center py-20 px-5"):
                ui.label("Sicklecell Education").classes("text-3xl md:text-5xl font-bold mb-4")
                ui.label("Your Comprehensive guide for understanding and managing sickle cell disease").classes("text-base md:text-xl leading-relaxed")
        with ui.column().classes("flex items-center justify-center w-full"):

        # 3. Main Content Section (Expand Your Knowledge)
            with ui.element("section").classes("w-full py-16 px-5 md:px-20 max-w-screen-xl mx-auto"):
                # Sub-heading
                ui.label("Living with sicklecell").classes("text-2xl md:text-4xl font-bold text-gray-800 mb-12 text-center w-full")

            # Grid for two main topics, exactly matching the UI layout
            with ui.row().classes("grid grid-cols-1 lg:grid-cols-2 gap-10"):
                
               
                with ui.column().classes("p-6 shadow-xl rounded-xl border border-gray-100 transform hover:scale-[1.02] transition-transform duration-300"):
                    ui.label("Crisis Management").classes("text-xl md:text-2xl font-semibold text-red-600 mb-4")
                    
                    # Image Placeholder
                    with ui.card().classes("w-full h-48 mb-4 bg-gray-200 rounded-lg flex items-center justify-center"):
                         ui.label("Placeholder: sicklecell Image").classes("text-gray-500 text-lg")

                   
                    ui.label("Step-by-step Guidance:").classes("font-bold text-gray-800 mb-3")
                    ui.label("Immediate actions to take during a sicklecell crisis")
                    

                # B. Sickle Cell Disease (SCD) Education Card
                with ui.column().classes("p-6 shadow-xl rounded-xl border border-gray-100 transform hover:scale-[1.02] transition-transform duration-300"):
                    ui.label("Healthy Lifestyle").classes("text-xl md:text-2xl font-semibold text-red-600 mb-4")
                    
                    # Image Placeholder for Sickle Cell
                    with ui.card().classes("w-full h-48 mb-4 bg-gray-200 rounded-lg flex items-center justify-center"):
                        ui.label("Placeholder: Sickle Cell Image").classes("text-gray-500 text-lg")
                        
                    # Key Information
                    ui.label("Tips for Daily Life").classes("font-bold text-gray-800 mb-2")
                    ui.label("Practical advice for managing sickle cell symptons and maintaining a good quality life.").classes("text-base text-gray-600 mb-4")
                    
                    # ui.label(":").classes("font-bold text-gray-800 mb-2")
                    # for treatment in [
                    #     "Blood transfusions are crucial for managing severe anemia and complications.",
                    #     "Pain management and preventative care.",
                    #     "Bone marrow transplants (in some cases).",
                    # ]:
                    #      # Use Font Awesome for bullet points
                    #     ui.html(f'<i class="fa-solid fa-square-poll-vertical text-red-500 mr-2"></i>{treatment}', sanitize=False).classes("text-base text-gray-600 mb-2 flex items-start")
                        
                    # ui.button("Get Comprehensive Guide", on_click=lambda: ui.navigate.to('/sicklecell_education')).props("no-caps").classes("mt-6 w-full bg-red-500 text-white rounded-md px-4 py-2 hover:bg-red-500 transition")

            ui.button("Load more resources", on_click=lambda: ui.notify("Loading more topics...")).props("no-caps").classes("mt-6 w-1/2 bg-red-500 text-white rounded-md px-4 py-2 hover:bg-gray-500 transition")

            ui.label("Additional Resources").classes("text-xl mt-20 md:text-2xl font-semibold text-red-600 mb-4")       
            with ui.row().classes("grid grid-cols-1 lg:grid-cols-3 gap-8 mb-40"):
                with ui.column().classes("p-6 shadow-xl rounded-xl border border-gray-100 transform hover:scale-[1.02] transition-transform duration-300"):
                    
                    # Image Placeholder
                    with ui.card().classes("w-full h-48 mb-4 bg-gray-200 rounded-lg flex items-center justify-center"):
                         ui.label("Placeholder: sicklecell Image").classes("text-gray-500 text-lg")
                    
                    ui.label("Medication Adherence").classes("text-xl md:text-2xl font-semibold text-red-600 mb-4")
                    
                with ui.column().classes("p-6 shadow-xl rounded-xl border border-gray-100 transform hover:scale-[1.02] transition-transform duration-300"):
                                        
                    # Image Placeholder
                    with ui.card().classes("w-full h-48 mb-4 bg-gray-200 rounded-lg flex items-center justify-center"):
                         ui.label("Placeholder: sicklecell Image").classes("text-gray-500 text-lg")

                    ui.label("Downloadable Guides").classes("text-xl md:text-2xl font-semibold text-red-600 mb-4")

                with ui.column().classes("p-6 shadow-xl rounded-xl border border-gray-100 transform hover:scale-[1.02] transition-transform duration-300"):
                    
                    # Image Placeholder
                    with ui.card().classes("w-full h-48 mb-4 bg-gray-200 rounded-lg flex items-center justify-center"):
                         ui.label("Placeholder: sicklecell Image").classes("text-gray-500 text-lg")

                    ui.label("Audiovisuals & Articles").classes("text-xl md:text-2xl font-semibold text-red-600 mb-4")
                         


        # 4. Footer (Consistent with the style used in the other pages)
        show_footer()