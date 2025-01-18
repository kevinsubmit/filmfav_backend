

project steps:

init

1. git clone https://github.com/kevinsubmit/filmfav_backend.git
2. git checkout -b yourbranch
3. pipenv shell
   

database env

   make sure your local have the file create-database.sql
4. psql -f create-database.sql

   the below two commands can make 200 fake movies datas in your local databases 
5. pip install Faker
6. python manage.py generate_movies

