# Mexico City Water Quality Application

Sabah Pirani

[Link to this repository](<https://github.com/Sabah-pirani/Mexico_City_Chlorine_Levels_Application>)

---

## Project Description

The water infrastructure department of the Mexican government (Sistmas de Aguas de Cuidad de Mexico) provides data on the chlorine levels of water samples it collects throughout Mexico City. The data is hosted online at: http://data.sacmex.cdmx.gob.mx/aplicaciones/calidadagua/ . While the database being used includes dates of sample collection this data isn't displayed on the website, but you are allowed to query the data by date. Furthermore the data is organized such that you must pick a region, then a neighborhood to view the data for ~10 samples and then go back to view any data from a different neighborhood or region. Ultimately, the User interface for the data is poorly designed making it nearly impossible for researchers to make use of this data that is being collected by the government. 

This application includes a script to query the data from the site and store the data with a date and full information about the location (region, neighborhood and street) in a database. The application provides a very simplistic User Interface to query the data and conduct exploratory data analysis. 

The project will be expanded to include visual mapping of the regions with the ability to download CSV files of the data that one is interested in, in the future. 

## How to run

1. There are two ways in which this application is intended to be used:

   1. The database file provided in the repository has data from XX-XX-XX until 4-16-2019. If you simply wish to query the data provided within the provided database file you may simply run the main_app.py file on your command line, using the runserver command proceeding the python main_app.py command to allow the application to run on your local computer. Then open any web browser and navigate to your local server address (often ` http://localhost:5000/`). This page will have an introduction and links to other pages that allow you to query the database and view visualizations. The code for the command line would look as follows: 

      `python main_app.py runserver`

   2. If you are trying to update the db file to include the data from 4-17-2019 onward. You first must edit the 'start_date', and 'end_date' variables on line XX and XX of the scrape_data_populate_db.py file. Save the file and run the scrape_data_populate_db.py file on your command line with the following command: 

      `python scrape_data_populate_db.py`

## How to use

1. A useful instruction goes here
2. A useful second step here
3. (Optional): Markdown syntax to include an screenshot/image: ![alt text](image.jpg)

## Routes in this application
- `/home` -> this is the home page
- `/form` -> this route has a form for user input
- `/result` -> this route is where the form sends the result...
- `/newuser/<username>` -> this route also takes input of a name and shows you a greeting

## How to run tests
1. First... (e.g. access a certain directory if necessary)
2. Second (e.g. any other setup necessary)
3. etc (e.g. run the specific test file)
NOTE: Need not have 3 steps, but should have as many as are appropriate!

## In this repository:

- README.md

- main_app.py

- scrape_data_populate_db.py

- calidad_agua.db

- requirements.txt

- database_schema.png

  

---
## Acknowledgments

This project was built in part for SI507 class and a great deal of support was provided by the class' instructional team. Some configuration settings among other smaller snippets of code are directly copied from examples used in SI507 and are attributed to Jackie Cohen (jczetta). The graduate student instructors provided help in debugging and conceptualizing the relationships between different parts of the project which was also immensely helpful. 

## Code Requirements for Grading

Please check the requirements you have accomplished in your code as demonstrated.
- [x] This is a completed requirement.
- [ ] This is an incomplete requirement.

Below is a list of the requirements listed in the rubric for you to copy and paste.  See rubric on Canvas for more details.

### General
- [x] Project is submitted as a Github repository
- [ ] Project includes a working Flask application that runs locally on a computer
- [ ] Project includes at least 1 test suite file with reasonable tests in it.
- [x] Includes a `requirements.txt` file containing all required modules to run program
- [x] Includes a clear and readable README.md that follows this template
- [x] Includes a sample .sqlite/.db file
- [x] Includes a diagram of your database schema
- [x] Includes EVERY file needed in order to run the project
- [ ] Includes screenshots and/or clear descriptions of what your project should look like when it is working

### Flask Application
- [ ] Includes at least 3 different routes
- [ ] View/s a user can see when the application runs that are understandable/legible for someone who has NOT taken this course
- [ ] Interactions with a database that has at least 2 tables
- [x] At least 1 relationship between 2 tables in database
- [ ] Information stored in the database is viewed or interacted with in some way

### Additional Components (at least 6 required)
- [ ] Use of a new module
- [ ] Use of a second new module
- [ ] Object definitions using inheritance (indicate if this counts for 2 or 3 of the six requirements in a parenthetical)
- [ ] A many-to-many relationship in your database structure
- [ ] At least one form in your Flask application
- [ ] Templating in your Flask application
- [ ] Inclusion of JavaScript files in the application
- [ ] Links in the views of Flask application page/s
- [ ] Relevant use of `itertools` and/or `collections`
- [x] Sourcing of data using web scraping
- [ ] Sourcing of data using web REST API requests
- [ ] Sourcing of data using user input and/or a downloaded .csv or .json dataset
- [x] Caching of data you continually retrieve from the internet in some way

### Submission
- [ ] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)
- [ ] I included a summary of my project and how I thought it went **in my Canvas submission**!
