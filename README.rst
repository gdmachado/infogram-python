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
