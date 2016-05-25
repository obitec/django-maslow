.. Django FactBook documentation master file, created by
   sphinx-quickstart on Sun May 22 17:34:01 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django Maslow's documentation!
=========================================

Contents:

.. toctree::
   :maxdepth: 2

   contributing
   modules/models

========
Overview
========

Django Maslow -- Providing the base layer for all Django apps on their journey to self actualisation.

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

5. Visit http://127.0.0.1:8000/maslow/ to get an overview.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

