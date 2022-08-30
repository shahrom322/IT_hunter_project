# JUMANDJI
Site for job search, with the possibility of registration, compiling your resume and vacancies. Additional libraries: django-crispy-forms for displaying almost all the main forms on the site, django-debug-toolbar for debugging the development stage (controlling requests to the database), flake8 for controlling the code style. Also detailed the documentation. The site was deployed on heroku.
https://github.com/shahrom322/IT_hunter_project

Short description:<br>
:white_check_mark:Possibility of user registration.<br>
:white_check_mark:Registration of user company and vacancies.<br>
:white_check_mark:Ability to leave a response to a vacancy.<br>
:white_check_mark:Search for all vacancies on the site.<br>
:white_check_mark:Possibility of registering a user's resume<br>


![site](https://sun9-36.userapi.com/impf/_60rSgouv4lxo8F-ZgUqd-bIAAKyfayK9FpRag/DFd5s83IOv4.jpg?size=1919x1037&quality=96&sign=a9d67302bb672dbc54a89a5c361db160&type=album "site")

### Installation:
First of all you should create your own enviroment with python3.9:

    python3.9 -m venv venv
Activate your enviroment:

    source venv/bin/activate
Then you should to install all dependencies:

    pip install -r requirements.txt
Now we need populate database. Execute next command:

    python manage.py db_dump
You can create a superuser simply with this command:

    python manage.py makesuperuser
Then just run server:

    python manage.py runserver
<hr>
It is also possible to choose a configuration (production or development). When starting production mode, you need to create a PostgresQL user and add the necessary data to the environment variable.<br>

![gif example](https://media.giphy.com/media/9m5Qu3NWQ5NLwWBKUC/giphy.gif)
<hr>

### Or you can just:

    docker-compose up
Server will be start in http://localhost:1337/
