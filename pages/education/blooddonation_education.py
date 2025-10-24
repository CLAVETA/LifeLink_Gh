from nicegui import ui, app
from pages.education.user_education import search_card

# components
from components.navbar import show_navbar

app.add_static_files("/assets", "assets")

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
        
            # Frequently Asked Questions
            with ui.column().classes('w-full mt-8'):
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



@ui.page("/blooddonation_education")
def blooddonation_page():
    # Setup for responsive design and removing default NiceGUI margins
    ui.add_head_html('<script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>')
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")
    
    with ui.element("main").classes("min-h-screen w-full flex flex-col"):
        
        # 1. Navbar: Highlight the 'Education' link
        show_navbar()

        # 2. Main Content Container
        with ui.column().classes('w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-16'):
            
            # Header
            with ui.element("section").classes("flex items-center justify-center w-full text-white bg-[url('/assets/educational_resources.png')] bg-cover bg-center bg-white/20 bg-blend-overlay"):
                with ui.column().classes("items-center w-full max-w-screen-lg text-center py-20 px-5"):
                    ui.label("Blood Donation Education").classes("text-4xl md:text-5xl font-bold text-gray-900 mb-4")
                    ui.label("Your comprehensive resource for insights on the importance and process of blood donation").classes("text-lg text-gray-900 max-w-3xl mx-auto md:text-xl leading-relaxed")
            with ui.column().classes("flex items-center justify-center w-full"):
                filtered_resources_container = ui.column().classes("w-full mt-10 px-10 md:px-20")
                search_card(filtered_resources_container)

            # with ui.column().classes('text-center space-y-2'):
            #     ui.label('Blood Donation Education').classes('text-4xl md:text-5xl font-bold text-gray-900')
            #     ui.label('Your comprehensive resource for understanding the importance and process of blood donation.').classes('text-lg text-gray-600 max-w-3xl mx-auto')
            #     with ui.element('div').classes('mt-8 max-w-xl mx-auto w-full'):
            #         with ui.input(placeholder='Search for topics...').classes('w-full').props('outlined'):
            #             ui.icon('search').classes('text-gray-400')
            
            # The Donation Journey
            with ui.column().classes('w-full'):
                ui.label('The Donation Journey').classes('text-3xl font-bold text-gray-900 mb-8')
                with ui.card().classes('w-full p-0 shadow-lg rounded-xl overflow-hidden'):
                    with ui.row().classes('flex flex-col md:flex-row w-full'):
                        # Text/FAQ Column
                        with ui.column().classes('p-8 md:w-1/2 space-y-4'):
                            ui.label('Tips for a Successful Donation').classes('text-2xl font-semibold text-gray-800')
                            ui.label('Find practical advice for preparing for your donation, what to expect during the process, and post-donation care to ensure a positive experience.').classes('text-gray-600 mb-6')
                            
                            # Accordions
                            create_accordion(
                                title='Why Donate Blood?',
                                content='Your donation is vital to your community, ensuring the local blood supply is always strong.' \
                                'A single donation can save up to three lives. Every two seconds, someone in the U.S. requires a blood transfusion. Whether it’s for accident victims, patients undergoing surgery, or individuals battling chronic diseases, the need for blood is constant. One single donation can save up to three lives. Beyond saving lives, donating blood also helps hospitals manage their inventory better, ensuring a ready supply during emergencies, and ultimately, serving more people and improving the quality of life for those in need.'
                            )
                            create_accordion(
                                title='Am I Eligible to Donate?',
                                content='General eligibility criteria include being in good health, being at least 18 years old (or 16 with parental consent in some areas), and weighing at least 110 lbs. ' \
                                'However, certain medications, medical conditions, and recent travel to specific areas may affect your eligibility. We encourage you to review the full eligibility guidelines or contact us with any questions prior to your visit.'
                            )
                            create_accordion(
                                title='The Donation Process',
                                content='Donating blood is a safe and straightforward process, typically taking about one hour from start to finish.' \
                                "The process includes registration, a mini-physical and health history screening, the donation itself takes about 8-10 minutes only. Afterwards, you\'ll rest and enjoy refreshments before resuming your day. The entire process is designed for your comfort and safety in mind, ensuring a positive and rewarding experience."
                            )
                        
                        # Image Column
                        ui.image('assets\edu_donation2.PNG').classes('rounded-md mb-4 md:w-120 h-100 object-cover')
            
            # Impact & Healthy Lifestyle
            with ui.row().classes('grid grid-cols-1 md:grid-cols-2 gap-8 w-full'):
                # Impact of Your Donation
                with ui.card().classes('p-6 shadow-lg rounded-xl'):
                    ui.label('Impact of Your Donation').classes('text-2xl font-bold text-gray-900 mb-4')
                    ui.image('assets\donation_impact.PNG').classes('w-full h-48 object-cover rounded-md mb-4')
                    ui.label('Saving Lives').classes('text-xl font-semibold mb-2 text-gray-800')
                    ui.label('Learn about the different components of blood (red cells, platelets, plasma) and how each part is used to treat patients with various medical needs.').classes('text-gray-600')
                
                # Healthy Lifestyle for Donors
                with ui.card().classes('p-6 shadow-lg rounded-xl'):
                    ui.label('Healthy Lifestyle for Donors').classes('text-2xl font-bold text-gray-900 mb-4')
                    ui.image('assets\healthy_lifestyle.PNG').classes('w-full h-48 object-cover rounded-md mb-4')
                    ui.label('Diet and Hydration').classes('text-xl font-semibold mb-2 text-gray-800')
                    ui.label('Discover the best foods and hydration tips to prepare your body for donation and to help it recover quickly afterwards. Iron-rich foods are especially important.').classes('text-gray-600')

            # Resources Section
            with ui.column().classes('w-full'):
                ui.label('Resources').classes('text-3xl font-bold text-gray-900 mb-8')
                with ui.row().classes('grid grid-cols-1 md:grid-cols-3 gap-8 w-full'):
                    # Donor Stories
                    with ui.card().classes('p-6 shadow-lg rounded-xl text-center'):
                        ui.image('assets\sickle_resource2.JPG').classes('w-24 h-24 object-cover rounded-full mx-auto mb-4')
                        ui.label('Donor Stories').classes('text-xl text-center font-semibold mb-2 text-gray-800')
                        ui.label('Read inspiring stories from both blood donors and recipients. Understand the real-world impact of your selfless act.').classes('text-gray-600')
                    
                    # Downloadable Guides
                    with ui.card().classes('p-6 shadow-lg rounded-xl text-center'):
                        ui.image('assets\sickle_resource3.JPG').classes('w-24 h-24 object-cover rounded-full mx-auto mb-4')
                        ui.label('Downloadable Guides').classes('text-xl text-center font-semibold mb-2 text-gray-800')
                        ui.label('Access informative guides on various aspects of blood donation, including FAQs and post-donation care, available for download.').classes('text-gray-600')

                    # Videos and Articles
                    with ui.card().classes('p-6 shadow-lg rounded-xl text-center'):
                        with ui.element('div').classes('relative w-24 h-24 mx-auto mb-4'):
                            ui.image('assets\sickle_resource4.JPG').classes('w-full h-full object-cover rounded-full')
                            ui.icon('play_circle_outline', size='4xl').classes('absolute inset-0 m-auto text-white text-opacity-80')
                        ui.label('Videos and Articles').classes('text-center text-xl font-semibold mb-2 text-gray-800')
                        ui.label('Explore educational videos and articles covering a range of topics related to blood donation and its importance.').classes('text-gray-600')

            # Donor Portal Section (Red Block)
            with ui.element('div').classes('bg-red-600 text-white p-8 md:p-12 rounded-xl shadow-lg relative w-full h-96 rounded-lg overflow-hidden'):
            # with ui.element('div').classes('relative w-full h-96 rounded-lg overflow-hidden'):
                ui.image('assets\edu_donation3.PNG').classes('w-full h-full bg-cover rounded-xl').style('filter: brightness(0.8);')
                with ui.element('div').classes('absolute inset-0 flex flex-col items-center justify-center text-white text-center p-8'):
                    ui.label('Give the Gift of Life').classes('text-4xl md:text-5xl font-bold mb-4')
                    ui.label('Your blood donation can save lives. Learn how you can make a real difference.').classes('text-lg mb-8')
                    ui.button('Find a Donation Center', on_click=lambda: ui.navigate.to('/donor_registration')).classes('bg-white text-red px-8 py-3 font-semibold hover:bg-red-700 transition-colors')
            
        show_footer()
