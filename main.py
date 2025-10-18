from nicegui import ui

# importing pages
from pages.home import *
from pages.about import *
from pages.education.user_education import *
from pages.education.sicklecell_education import *
from pages.education.blooddonation_education import *


# hospital
from pages.hospital.hospital_dashboard import *
from pages.hospital.hospital_register import *
from pages.hospital.hospital_login import *

# donor
from pages.donor.donor_register import *
from pages.donor.donor_login import *
from pages.donor.donor_dashboard import *
from pages.donor.donor_profile import *
from pages.donor.donor_alerts import *

# volunteer
from pages.volunteer.volunteer_register import *



#exposing static files
app.add_static_files("/assets", "assets")

# fonts


def show_homepage():
    home_page()


def show_about():
    about_page()


def show_hospital_dashboard():
    hospital_dashboard_page()

def show_hospital_signup():
    hospital_signup_page()

def show_hospital_login():
    hospital_login_page()
    
def show_donor_registration_page():
    donor_registration_page()    

def show_donor_login():
    donor_login_page()

def show_donor_alerts():
    donation_request_page()

def show_volunteer_signup_page():
    volunteer_signup_page()

def show_education_page():
    education_page()

def show_sicklecell_page():
    sicklecell_page()

def show_blooddonation_page():
    blooddonation_page()

ui.run(storage_secret="akualizzy!akualizzy!", port=5050)
