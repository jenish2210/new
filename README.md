# Django Ecommerce Starter

How to use:
1. Create a virtualenv and install: `pip install -r requirements.txt`
2. Run `python manage.py migrate`
3. Create a superuser: `python manage.py createsuperuser`
4. Run server: `python manage.py runserver`
5. Upload product images via admin and test the shop.

Features included:
- Product model with image (media) handling
- Session-based shopping cart (add/remove)
- Simple checkout that creates an Order and OrderItems (marks paid=True)
- User signup and Django's auth for login/logout
- Order history page (requires login)

Notes:
- This is a starter scaffold. For production, add payment gateway, address forms, validation, stock checks, CSRF, and security settings.
