==============
Django Maslow
==============

Django Maslow -- Providing the base layer for all Django apps on their journey to self actualisation.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "maslow" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'maslow',
    ]

2. Include the polls URLconf in your project urls.py like this::

    url(r'^maslow/', include('maslow.urls')),

3. Run `python manage.py migrate` to create the maslow models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/maslow/ to see it in action.
