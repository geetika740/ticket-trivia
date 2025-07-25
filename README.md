# 🎟️ Ticket Trivia

Ticket Trivia is a Django-based web application for booking tickets to national monuments, museums, and parks in India. It provides users with a smooth interface to browse, filter, and book tickets, along with payment integration and chatbot support.

## 🚀 Features

- 🏛️ Browse and search monuments by category (Monuments, Museums, Parks)
- 🎫 Book tickets and view booking history
- 💬 Chatbot support for common queries (powered by Dialogflow)
- 🧾 OTP verification during user registration
- 🔐 Secure Stripe-based payment integration
- 📄 About and Contact pages for user engagement
- 🔍 Admin dashboard to manage monuments and bookings

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS (Django Templates), Bootstrap
- **Database**: SQLite3 (development)
- **Chatbot**: Google Dialogflow API
- **Payment Gateway**: Stripe
- **Deployment**: [Optional - Docker/Heroku/etc.]

## 📂 Project Structure

ticket-trivia/
├── ticket_trivia/ # Main Django project directory
├── templates/ # HTML Templates
├── static/ # CSS, JS, images
├── manage.py # Django management script
├── dialogflow_test.py # Dialogflow integration test script
├── dialogflow_key.json # [EXCLUDED: Store securely using .env]
├── .env # Environment variables

## 🔐 Environment Variables

Create a `.env` file with the following variables:

GOOGLE_APPLICATION_CREDENTIALS=dialogflow_key.json
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key

> ⚠️ **Never commit your `.env` or `dialogflow_key.json` to GitHub**. They are already added to `.gitignore`.

## 🧪 Running the Project Locally

git clone https://github.com/geetika740/ticket-trivia.git
cd ticket-trivia
python -m venv venv
source venv/bin/activate    # or venv\Scripts\activate (Windows)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Built with ❤️ by Geetika Kakkar

## 🧑‍💻 Future Improvements

React frontend for better UX
Multi-language chatbot
Role-based access for staff/admin
Email notifications

## 🧾 License
This project is licensed under the MIT License.
