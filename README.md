# 📰 OnlineMag E-commerce Django Project

OnlineMag is a Django-based e-commerce platform featuring:
- Custom user roles (`admin`, `owner`, `user`)
- Product management and promotions
- Messaging system with threaded replies
- Basket and order system
- Owner dashboard and transport settings
- Stripe payment integration

---

## 🚀 Project Setup Instructions

### ⚙️ Requirements

- Python 3.9+
- Django 4.x
- pip
- SQLite (default) or PostgreSQL (optional)
- Stripe account (for Owner)

---

## 📁 Project Structure

Main apps:
- `users` – Custom user model
- `products` – Product & promotion system
- `basket` – Cart and order logic
- `messages_app` – Threaded messaging between users and owner
- `owner` – Owner dashboard functionality
- `core` – Global settings (e.g., homepage content, themes)

---

## 🧱 Step-by-Step Setup

### 1. Clone the project

```bash
git clone https://github.com/your_username/onlinemag.git
cd onlinemag
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
pip install -r requirements.txt
create .env file that whould contains :
DJANGO_SECRET_KEY=your_django_secret_key_here
DEBUG=True ----if in debug mode 

STRIPE_PUBLIC_KEY=your_stripe_public_key_here
STRIPE_SECRET_KEY=your_stripe_secret_key_here
# First migrate the basket app
#there is a dependancy and needs to be migrated first
python manage.py makemigrations basket
python manage.py migrate basket

# Then migrate the other apps
python manage.py makemigrations users products messages_app owner core
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
then in the adnmin panel create an owner  for the site
