from nicegui import ui, app
from pages.education.user_education import search_card
# components
from components.navbar import show_navbar
# from components.footer import show_footer # Keeping the show_footer definition if it's missing from components

app.add_static_files("/assets", "assets")


def create_resource_card(title: str, description: str, image_path: str, url: str):
    """
    Creates an educational resource card with a hover-revealed 'View' button.

    The card container is marked as a 'group' and the button overlay is
    absolutely positioned, transitioning opacity from 0 to 100 on hover.
    """
    # Card container: Add 'group' class to enable group-hover utilities on children.
    # Also added 'relative' for absolute positioning of the overlay.
    with ui.column().classes("group relative p-6 shadow-xl rounded-xl border border-gray-100 transform hover:scale-[1.02] transition-transform duration-300 overflow-hidden cursor-pointer"):
        # Image Container
        with ui.card().classes("w-full h-64 mb-4 rounded-lg flex items-center justify-center overflow-hidden"):
            ui.image(image_path).classes('w-full h-full object-cover')
            
        # Text Content
        ui.label(title).classes("text-xl md:text-2xl font-semibold text-red-600 mb-4")
        ui.label(description).classes('text-gray-600') # Removed fixed height as the overlay handles the space
        
        # Overlay/View Button
        # Absolute positioning, hidden by default (opacity-0), visible on group-hover.
        # This covers the entire card area.
        with ui.element('div').classes('absolute inset-0 bg-black/50 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300'):
            # The actual button
            ui.button("View Resource", on_click=lambda: ui.navigate.to(url, new_tab=True)).classes('bg-red-500 hover:bg-red text-white font-bold py-2 px-6 rounded-full shadow-lg transition duration-300').props('icon=open_in_new')


def create_accordion(title: str, content: str, default_open=False):
    """Creates a NiceGUI accordion (details/summary structure) for the FAQ section."""
    with ui.card().classes('w-full shadow-none p-0 border-b border-gray-200'):
        with ui.row().classes('w-full justify-between items-center cursor-pointer p-4 hover:bg-gray-50') as header:
            ui.label(title).classes('font-medium text-gray-800')
            icon = ui.icon('expand_more').classes('text-gray-600 transition-transform')
        
        content_container = ui.column().classes('hidden w-full p-4 pt-0 text-gray-600')
        with content_container:
            ui.label(content).classes('leading-relaxed')

        # Toggle behavior using JavaScript/NiceGUI
        def toggle_accordion():
            is_hidden = 'hidden' in content_container.classes
            if is_hidden:
                content_container.classes(remove='hidden')
                icon.classes(add='rotate-180')
            else:
                content_container.classes(add='hidden')
                icon.classes(remove='rotate-180')
        
        header.on('click', toggle_accordion)

def create_simple_accordion(question: str, answer: str):
    """Creates a NiceGUI accordion (expansion) for the simple FAQ section."""
    with ui.expansion(question).classes('w-full border-b border-gray-200 p-0 hover:bg-gray-50').props('expand-separator'):
        ui.label(answer).classes('text-gray-600 p-4 pt-0 leading-relaxed')

def show_footer():
    with ui.row().classes("flex flex-col md:flex-row items-center justify-between px-7 w-full bg-gray-50 py-5 text-sm text-gray-700 mt-auto border-t border-red-100"):
            ui.label("© 2025 LifeLink. All rights reserved.").classes("mb-3 md:mb-0")
            with ui.row().classes("gap-6"):
                ui.link("About","/about").classes("no-underline text-gray-700 transition")
                ui.link("Contact").classes("no-underline hover:text-white text-gray-700 transition")
                ui.link("Privacy Policy").classes("no-underline text-gray-700 transition")
        

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
        with ui.element("section").classes("flex items-center justify-center w-full text-white bg-[url('/assets/sickle_edu2.JPG')] bg-cover bg-center bg-black/60 bg-blend-overlay"):
            with ui.column().classes("items-center w-full max-w-screen-lg text-center py-20 px-5"):
                ui.label("Sicklecell Education").classes("text-3xl md:text-5xl font-bold mb-4")
                ui.label("Your Comprehensive guide for understanding and managing sickle cell disease").classes("text-base md:text-xl leading-relaxed")
        with ui.column().classes("flex items-center justify-center w-full"):
                filtered_resources_container = ui.column().classes("w-full mt-10 px-10 md:px-20")
                search_card(filtered_resources_container)
            
        with ui.element("section").classes("w-full"):
                # Sub-heading
                ui.label("Living with sicklecell").classes("text-3xl md:text-4xl font-bold text-gray-800 mb-12 mt-8 text-center w-full")

        with ui.card().classes('w-full p-6 shadow-lg rounded-xl justify-center overflow-hidden mr-10'):
            with ui.row().classes('flex flex-col md:flex-row w-full'):
                # Text Column
                with ui.column().classes('p-8 md:w-1/2 space-y-4'):
                    ui.label('Tips for Maintaining Quality Life').classes('text-2xl font-semibold text-gray-800')
                    ui.label('Find practical advice for managing sickle cell symptons, and maintaining a good daily life.').classes('text-gray-600 mb-6')
                    
                    # Accordions
                    create_accordion(
                        title='What is sickle cell disease?',
                        content='Your donation is vital to your community, ensuring the local blood supply is always strong.' \
                                'A single donation can save up to three lives. Every two seconds, someone in the U.S. requires a blood transfusion. Whether it’s for accident victims, patients undergoing surgery, or individuals battling chronic diseases, the need for blood is constant. One single donation can save up to three lives. Beyond saving lives, donating blood also helps hospitals manage their inventory better, ensuring a ready supply during emergencies, and ultimately, serving more people and improving the quality of life for those in need.'
                    )
                    create_accordion(
                        title='Common Symptons',
                        content='General eligibility criteria include being in good health, being at least 18 years old (or 16 with parental consent in some areas), and weighing at least 110 lbs. ' \
                                'However, certain medications, medical conditions, and recent travel to specific areas may affect your eligibility. We encourage you to review the full eligibility guidelines or contact us with any questions prior to your visit.'
                    )
                    create_accordion(
                        title='Managing Pain',
                        content='Donating blood is a safe and straightforward process, typically taking about one hour from start to finish.' \
                                "The process includes registration, a mini-physical and health history screening, the donation itself takes about 8-10 minutes only. Afterwards, you\'ll rest and enjoy refreshments before resuming your day. The entire process is designed for your comfort and safety in mind, ensuring a positive and rewarding experience."
                    )
                
                # Image Column
                ui.image(r'assets\sickle_resource1.JPG').classes('p-10 rounded-md mb-4 md:w-120 h-100 object-cover ml-8')
            
        # Grid for two main topics, exactly matching the UI layout
        with ui.row().classes('grid grid-cols-1 md:grid-cols-2 gap-10 mt-12 p-6'):
                # Crisis Management 
                # with ui.card().classes('p-6 shadow-lg rounded-xl mb-4 justify-center ml-10'):
                #     ui.label('SCD Crisis Management').classes('mb-4 text-xl md:text-2xl font-semibold text-red-600')
                #     ui.image(r'assets\sickle_edu1.JPG').classes('w-full h-64 object-cover rounded-md mb-4')
                #     ui.label('Step-by-step Guidance').classes('text-xl font-semibold mb-2 text-gray-800')
                #     ui.label('Immediate actions to take during a sicklecell crisis').classes('text-gray-600')

                create_resource_card(
                     title='SCD Crisis Management',
                     description='Step-by-step Guidance : Immediate actions to take during a sicklecell crisis',
                     image_path=r'assets\sickle_edu1.JPG',
                     url='https://www.cdc.gov/ncbddd/sicklecell/documents/crisis-management.html' # External link added
                )

                create_resource_card(
                     title='Healthy Lifestyle for SCD Carriers',
                     description='Diet and Hydration: Nutritional advice and hydration tips to support overall health and manage SCD symptoms',
                     image_path=r'assets\sickle_edu5.jpg',
                     url='https://www.cdc.gov/ncbddd/sicklecell/documents/crisis-management.html' # External link added
                )
        # Divider before resources section
        ui.element('hr').classes('my-16 border-t border-gray-300 w-full')
        # Resources Section - UPDATED TO USE create_resource_card
        ui.label("Additional Resources").classes("text-xl mt-20 md:text-2xl font-semibold text-red-600 mb-4")       
        with ui.row().classes("grid grid-cols-1 lg:grid-cols-3 gap-8 mb-40"):
            create_resource_card(
                title="Medication Adherence",
                description='Importance of following prescribed medication schedules. Tips for managing medications.',
                image_path=r'assets\sickle_edu6.webp',
                url='https://www.cdc.gov/sickle-cell/index.html/' # Placeholder external link
            )
            create_resource_card(
                title="Downloadable Guides",
                description='Informative guides on various aspects of sickle cell management, available for download.',
                image_path=r'assets\sickle_resource3.JPG',
                url='https://www.sparksicklecellchange.com/sickle-cell-support-groups-organizations/resources' # Placeholder external link
            )
            create_resource_card(
                title="Audiovisuals & Articles",
                description='Explore educational videos and articles covering a range of topics related to sickle cell disease.',
                image_path=r'assets\sickle_resource4.JPG',
                url='https://www.cdc.gov/sickle-cell/communication-resources/videos-and-podcasts.html' # Placeholder external link
            )


        with ui.column().classes('w-full mt-1'):
                ui.label('Frequently Asked Questions').classes('text-3xl font-bold text-gray-900 mb-4')
                with ui.column().classes('w-full border-t border-gray-200'):
                    create_simple_accordion(
                        'How often can I donate blood?',
                        'The standard time interval between whole blood donations is 56 days (8 weeks). This allows your body enough time to replenish its iron and red blood cell stores.'
                    )
                    create_simple_accordion(
                        'What should I do before donating blood?',
                        'Ensure you eat a healthy meal and drink plenty of water (about 16 ounces) in the hours leading up to your donation appointment. Get a good night\'s sleep.'
                    )
                    create_simple_accordion(
                        'What happens to my body after I donate?',
                        'Your body immediately begins replacing the donated blood. You should rest for a few minutes, drink fluids, and avoid heavy lifting or strenuous exercise for the rest of the day.'
                    )         
        show_footer()
