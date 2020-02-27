=============================
Scrape URL to find dead links
=============================

.. image:: https://travis-ci.com/EnTeQuAk/next-scraper.png?branch=master
    :target: https://travis-ci.com/EnTeQuAk/next-scraper
    :alt: Travis build status


Installation
------------

We are relying on docker and docker-compose to setup the development and test
environment. So please make sure you have both installed.

.. code-block:: bash

    $ # Clone repository
    $ git clone git@github.com:EnTeQuAk/next_scraper.git

    $ # Startup all services
    $ docke-compose up -d

    $ # Install and initialize the database
    $ make initialize-docker

    $ # run tests
    $ make test


Resources
---------

* `Bug Tracker <https://github.com/EnTeQuAk/next_scraper/issues>`_
* `Code <https://github.com/EnTeQuAk/next_scraper>`_
