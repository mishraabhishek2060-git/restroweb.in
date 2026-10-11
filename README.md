# Gokul Sweet & Restaurant

A Django website for a restaurant, with Home, Menu, About, and Contact pages. Menu entries and contact messages are stored in Django's database and can be managed through the admin site.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run `python manage.py migrate`.
4. Create an admin account with `python manage.py createsuperuser`.
5. Start the development server with `python manage.py runserver`.

Open `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/` to manage menu items and messages.

Add menu items in the admin and set both the half-plate and full-plate prices. Half plates stay unavailable until a half-plate price is entered. Orders are saved in the admin and each customer receives a printable bill with a WhatsApp message link.

The restaurant WhatsApp number is configured in `restro_project/settings.py` and can be overridden with the `RESTAURANT_WHATSAPP_NUMBER` environment variable. Before deployment, set `DJANGO_SECRET_KEY` to a private value and configure production `DEBUG` and `ALLOWED_HOSTS` settings.

## Deploy on Render

This repository includes a Render Blueprint (`render.yaml`). In Render, create a new Blueprint from this GitHub repository and apply the listed services. The web service is configured to use the free plan, deploy automatically after changes to the default GitHub branch, and run database migrations on each build. After the first deploy, add menu items and half/full prices in `/admin/` before accepting orders.

Free hosting is suitable for a public preview, with limits: Render sleeps the web service after 15 minutes without traffic, and free Postgres databases expire 30 days after creation. Free web services also lose uploaded files on restarts/redeploys. Move to persistent paid storage before relying on it for ongoing restaurant orders or admin-uploaded menu photos. The Render URL is separate from the `restroweb.in` domain; connecting that custom domain requires access to its DNS settings and a Render plan that supports custom domains.

