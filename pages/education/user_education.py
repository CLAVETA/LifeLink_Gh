from nicegui import ui, app
import random

# components
from components.navbar import show_navbar

app.add_static_files("/assets", "assets")

# -------------------------
# Dummy Resource Data
# -------------------------
RESOURCES = {
    "blood": [
        {
            "title": "Understanding Blood Donation",
            "description": "Learn who can donate blood, what to expect, and why it’s important.",
            "link": "/blooddonation_education",
        },
        {
            "title": "Benefits of Donating Blood",
            "description": "Each donation can save up to three lives and provides a free health check-up.",
            "link": "/blooddonation_education",
        },
    ],
    "sickle cell": [
        {
            "title": "Understanding Sickle Cell Disease",
            "description": "A guide to symptoms, treatments, and preventive care for SCD.",
            "link": "/sicklecell_education",
        },
        {
            "title": "Sickle Cell Management and Care",
            "description": "Best practices for managing crises and improving quality of life.",
            "link": "/sicklecell_education",
        },
    ],
    "crisis": [
        {
            "title": "Managing Sickle Cell Crisis",
            "description": "Tips and support for handling pain episodes effectively.",
            "link": "/sicklecell_education",
        }
    ],
}


# -------------------------
# Search Card Section
# -------------------------
def search_card(filtered_resources_container):
    selected_topic = ui.select(
        {
            "blood": "Blood Donation",
            "sickle cell": "Understanding Sickle Cell",
            "crisis": "Sickle Cell Management",
        },
        with_input=True,
        value=None,
        on_change=lambda e: update_resources_view(e.value, filtered_resources_container),
    ).props("placeholder=Choose topic dense").classes(
        "w-full bg-white text-black rounded-md h-10"
    )

    with ui.row().classes("bg-red-500 w-full text-white rounded-xl p-4 shadow-xl gap-4 items-end flex-wrap justify-between"):
        with ui.column().classes("flex-1"):
            ui.label("Search for topics").classes("text-xs text-white mb-1")
            selected_topic
        ui.button(icon="search", on_click=lambda: ui.notify("Select a topic to view resources")).classes(
            "h-10 w-10 rounded-md flex items-center justify-center text-white bg-purple-700"
        )


# -------------------------
# Resource Display Function
# -------------------------
def update_resources_view(selected_category, container):
    container.clear()
    if not selected_category:
        ui.notify("Please select a category.", color="red")
        return

    category_resources = RESOURCES.get(selected_category.lower(), [])

    if not category_resources:
        ui.label("No resources found for this category.").classes("text-gray-600 italic p-4")
        return

    for res in category_resources:
        with container:
            with ui.card().classes(
                "p-5 mb-5 shadow-lg rounded-xl border border-gray-200 hover:scale-[1.01] transition-transform duration-200"
            ):
                ui.label(res["title"]).classes("text-xl font-semibold text-red-600 mb-2")
                ui.label(res["description"]).classes("text-base text-gray-600 mb-3")
                ui.link("View Resource →", res["link"]).classes(
                    "text-red font-semibold hover:underline"
                )


# -------------------------
# Local Chatbot Simulation
# -------------------------
def lifelink_geni_chatbot():
    def generate_fake_reply(prompt: str) -> str:
        """Simple offline chatbot logic"""
        replies = [
            "That’s a great question! Blood donation helps save lives every day.",
            "Sickle cell disease requires ongoing care and regular check-ups.",
            "You can find more information under the Education tab.",
            "Remember to stay hydrated and eat well before donating blood.",
            "Managing crises involves pain control, hydration, and rest.",
        ]
        return random.choice(replies)

    with ui.dialog().classes("p-0") as chatbot, ui.card().classes(
        "p-4 w-[350px] h-[480px] flex flex-col justify-between bg-white"
    ):
        ui.label("💬 Lifelink Geni").classes("text-xl font-bold text-center mb-2 text-red-600")

        chat_output = ui.textarea().props("readonly").classes(
            "flex-1 mb-3 text-sm bg-gray-100 rounded-lg"
        )
        user_input = ui.input(placeholder="Looking for something? Ask Geni...").classes(
            "w-full mb-3"
        )

        def send_message():
            user_text = user_input.value.strip()
            if not user_text:
                ui.notify("Type a message first!", color="red")
                return
            chat_output.value += f"🧑 You: {user_text}\n"
            ai_reply = generate_fake_reply(user_text)
            chat_output.value += f"🤖 Geni: {ai_reply}\n\n"
            user_input.value = ""

        ui.button("Send", on_click=send_message).classes("bg-red text-white w-full")

    # Floating chatbot button
    ui.button("🤖 Chat with LifeLink Geni", on_click=chatbot.open).classes(
        "fixed bottom-6 right-6 bg-red text-white rounded-full shadow-lg px-5 py-3 hover:bg-red-700"
    )


# -------------------------
# Main Page
# -------------------------
@ui.page("/user_education")
def education_page():
    ui.add_head_html(
        '<script src="https://kit.fontawesome.com/6704ceb212.js" crossorigin="anonymous"></script>'
    )
    ui.query(".nicegui-content").classes("m-0 p-0 gap-0")

    with ui.element("main").classes("min-h-screen w-full flex flex-col"):
        # Navbar
        show_navbar()

        # Banner
        with ui.element("section").classes(
            "flex items-center justify-center w-full text-white bg-[url('/assets/educational_resources.png')] bg-cover bg-center bg-black/60 bg-blend-overlay"
        ):
            with ui.column().classes(
                "items-center w-full max-w-screen-lg text-center py-20 px-5"
            ):
                ui.label("Educational Resources Hub").classes(
                    "text-3xl md:text-5xl font-bold mb-4"
                )
                ui.label(
                    "Your comprehensive centre for understanding blood donation and sickle cell disease."
                ).classes("text-base md:text-xl leading-relaxed")

        # Search Filter
        filtered_resources_container = ui.column().classes("w-full mt-10 px-10 md:px-20")
        search_card(filtered_resources_container)

        # Default Resources Section (initially empty)
        ui.label("Educational Resources").classes(
            "text-2xl md:text-4xl font-bold text-gray-800 my-8 text-center w-full"
        )
        with filtered_resources_container:
            ui.label("Select a category to view related resources.").classes(
                "text-gray-500 italic"
            )
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

        # Footer
        with ui.row().classes(
            "flex flex-col md:flex-row items-center justify-between px-7 w-full bg-gray-50 py-5 text-sm mt-auto text-gray-500"
        ):
            ui.image("/assets/logo.png").classes("w-24 h-20")
            ui.label("© 2025 LifeLink. All rights reserved.").classes(
                "mb-3 md:mb-0 text-xl"
            )
            with ui.row().classes("gap-3"):
                ui.link("About", "/about").classes(
                    "no-underline text-gray-700 hover:text-red text-xl"
                )
                ui.link("Contact", "/about#contact").classes(
                    "no-underline hover:text-red text-gray-700 text-xl"
                )
                ui.link("Privacy Policy").classes(
                    "no-underline text-gray-700 hover:text-red text-xl"
                )

    # Floating chatbot (always on top)
    lifelink_geni_chatbot()
