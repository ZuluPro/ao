Ao - Cloud mocker
=================

This project aims to mock out Clouds' APIs at different level:

- As standalone server 
- HTTP proxy
- Python mock


Quick usage
-----------

Here's a quick example of how to deal with `Azure ARM`_ and standalone server:

#. Create SSL keys
#. Add Nginx configuration
#. Run server Django


Under the hood
--------------

Ao is built on top of `Django framework`_, it mimics HTTP APIs and stores
actions in database. There are 3 main behavior:

- `strict`: Try to act strictly as the provider
- `cool`: Release complicated constraints like authentication
- `free`: Most data are created on-the-fly to ease setup work

.. _`Azure ARM`: https://docs.microsoft.com/en-us/rest/api/resources/
.. _`Django framework`: https://www.djangoproject.com/
