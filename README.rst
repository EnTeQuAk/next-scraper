=============================
Scrape URL to find dead links
=============================

.. image:: https://travis-ci.com/EnTeQuAk/next-scraper.png?branch=master
    :target: https://travis-ci.com/EnTeQuAk/next-scraper
    :alt: Travis build status


This application allows analysis on a specific page, e.g to find broken links or to find out
if there's a login form on that page.

The application has been developed with Django, Celery and Django-Rest-Framework.

The (local) deployment has been done with Docker and supervisord to manage the processes. See more documentation
below.


Documentation
-------------

/api/start/
===========

Start a scraping process for a specific URL. It returns with ``201 CREATED`` in case of
successfully starting the process.

You can look at the ``/api/report/`` endpoint to see the results.

Arguments:

* **url**: The URL you want to scrape.

/api/report/
============

See the result of a scraping process.

    * **broken_links**: The amount of broken or unreachable links.
    * **created**: The date this scraping process got started
    * **external_links**: The amount of external links, leaving the base domain.
    * **internal_links**: The amount of internal links, staying in the realms of the same domain.
    * **headings**: An object documenting the count of all headings on the page.
    * **html_version**: The detected HTML version.
    * **id**: The internal ID
    * **may_contain_login_form**: Boolean determining if the page may or may not have a login form.
    * **original_url**: The URL this scraping process got requested for.
    * **state**: The state of this process. ``2`` is running, ``4`` completed and ``3`` means it failed for some reason and got aborted.
    * **status_code**: The HTTP status code we received for the requested URL.
    * **title**: The page title.


If the scraping process is still in progress you'll see the ``state`` be set to ``2`` and not all information
be filled in. Usually getting the final numbers of ``broken_links`` takes some additional time.

Please note that reports are bein cleaned up when older than 24 hours. During that time we do not scrape the URL again.


Installation
------------

We are relying on docker and docker-compose to setup the development and test
environment. So please make sure you have both installed.

.. code-block:: bash

    $ # Clone repository
    $ git clone git@github.com:EnTeQuAk/next-scraper.git

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
