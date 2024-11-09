# Run Project
1. git clone https://git.wmi.amu.edu.pl/s426206/SushiBar.git in terminal/git bash
2. (recomended via virtualenv) pip install -r requirements.txt
2.1 - pip uninstall django-suit
2.2 - pip install https://github.com/darklow/django-suit/tarball/v2
3. python manage.py makemigrations
4. python manage.py migrate
5. python manage.py createsuperuser
6. python manage.py runserver

# Using virtualenv
1. pip install virtualenv
2. virtualenv [name]
3. [name]\Scripts\activate
4. deactivate (close virtualenv)
suggested name: pri (already in .gitignore)

# Install django-suit
pip uninstall django-suit
pip install https://github.com/darklow/django-suit/tarball/v2