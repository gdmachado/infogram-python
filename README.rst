infogram-python
======

    Unofficial Python library for infogr.am API

Installation
------------

::

        $ pip install infogram

Usage
-----

::

    from infogram import Infogram

    # Initialize connection with the api, providing api_key and api_secret
    client = Infogram(api_key, api_secret)

    client.themes_list()

    client.infographics_create({
        "content": [{"type":"h1","text":"Hello infogr.am"}],
        "publish": False,
        "theme_id": 45,
        "title": "Hello",
    })

API Methods
------------

Themes
-----

::

    client.themes_list()

Infographics
-----

::

    client.infographics_list()
    client.infographics_get(infographic_id)
    client.infographics_create(params)
    client.infographics_update(infographic_id, params)
    client.infographics_destroy(infographic_id)

Users
-----

::

    client.users_get(user_id)
    client.users_get_infographics(user_id)
