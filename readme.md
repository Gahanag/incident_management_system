Incident Management System

Description

This project is a Django-based web application designed for managing incidents with a user-friendly interface. It utilizes Django REST Framework for API development and includes JWT authentication for secure access.

Features

- **User Management**: Register, log in, and manage user accounts.
- **Incident Management**: Create, view, and edit incidents.
- **Email Notifications**: Sends notifications via email using SMTP.
- **API Integration**: RESTful API endpoints with JWT authentication.

Technologies Used

- **Django**: Web framework for building the application.
- **Django REST Framework**: Toolkit for building Web APIs.
- **Django REST Framework SimpleJWT**: Provides JSON Web Token authentication.
- **SQLite**: Database for development (consider using PostgreSQL or MySQL for production).
- **Python Decouple**: Handles sensitive configurations through environment variables.

Installation

Follow these steps to set up the project locally:

1. **Clone the Repository**

   git clone repo
   cd repo

2. **Create a Virtual Environment**

   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install Dependencies**

   pip install -r requirements.txt

4. **Setup Environment Variables**

   Create a `.env` file in the root directory with the following content:

   SECRET_KEY=your-secret-key
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-email-password

5. **Apply Database Migrations**

   python manage.py migrate

6. **Create a Superuser**

   python manage.py createsuperuser

7. **Run the Development Server**

   python manage.py runserver

   Access the application at http://127.0.0.1:8000/.

Running the Application on Localhost

After completing the setup and running the development server, you can access the application in your web browser by navigating to:

- **Web Application**: http://127.0.0.1:8000/
- **Admin Interface**: http://127.0.0.1:8000/admin/

Log in using the superuser credentials created during setup to access the Django admin interface.

API Endpoints

- **/admin/**: Admin interface for managing the application.
- **/api/your-endpoint/**: Your custom API endpoints (replace `your-endpoint` with actual endpoints).

Testing Email Functionality

To test email notifications, use the Django shell:

python manage.py shell

Then run:

from django.core.mail import send_mail
send_mail('Test Subject', 'Test Message', 'from@example.com', ['to@example.com'], fail_silently=False)
#   i n c i d e n t _ m a n a g e m e n t _ s y s t e m  
 