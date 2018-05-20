# Item Catalog App

This app is a project for the Full Stack Web Developer Nanodegree at Udacity.

* ### Introduction

    *  **Backend**

       This app uses Flask and displays a list of items as well as their sub-categories. The users can add/modify/delete the items/categories, as well as register themselves up using the included Google OAuth 2.0.

    *  **Frontend**

       This app uses Material Design Bootstrap Library and Material Icons Libraries to follow the Material Design Guidelines.

* ### About

   The repo here contains several files, their usages being as follows:

    1. [app.py](app.py): This is used to run the project.
    2. [database_setup.py](database_setup.py): Use this to initialize the sqlite database if you haven't already.
    3. [populate_catalog.py](populate_catalog.py): Use this to fill dummy data into the database.
    4. [static](static): This contains the static files (img/js/css) files needed for the the html pages to render and function properly.
    5. [templates](templates): This directory contains the HTML templates for the Flask Engine to render.

* ### Dependencies

    1. [Vagrant](https://www.vagrantup.com/ "Vagrant")
    2. [Udacity Vagrant File](https://github.com/udacity/fullstack-nanodegree-vm "Udacity's Vagrant Configuration File")
    3. [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

* ### Installation

    1. Install Vagrant & VirtualBox.
    2. Get the Udacity Vagrant Configuration File and navigate to the vagrant directory.
    3. Launch and _up_ the Vagrant VM. (`vagrant up, vagrant ssh`)
    4. Install `requests` module by issuing the command `sudo pip install requests`
    5. Set up the database by running the [database_setup.py](database_setup.py) file.
    6. Insert dummy data into the database by running [populate_catalog.py](populate_catalog.py) file.
    7. Run the [app.py](app.py) file.

* ### Usage

    You can access the webpage at [http://localhost:5000](http://localhost:5000 "Localhost at port 5000").
   - _Note: Don't run the server using `http://127.0.0.1:5000` as it can cause problems with the Google Sign In._

* ### API Endpoints
    * **Catalog Json**: `/catalog/json` _Display the whole catalog, including all categories and items._
    * **Categories Json**: `/categories/json` _Display the all categories present._
    * **Category Item Json**: `/<string:category_name>/<string:item_name>/json` _Display the JSON of a particular item in a category._
    * **Category Items Json**: `/category/items/json` _Display a particular category's items JSON._ 

* ### External Libraries Used
    1. JQuery: (<https://jquery.com/>)
    2. JQuery Toast Plugin (<https://github.com/kamranahmedse/jquery-toast-plugin>)
    3. Material Design for Bootstrap 4 (<https://mdbootstrap.com/>)
    4. Material Icons by Google: (<https://material.io/tools/icons/?style=baseline>)
    5. Font Awesome Icons: (<https://fontawesome.com/icons>)