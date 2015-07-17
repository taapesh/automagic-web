cd $1
heroku create
git push heroku master
heroku run python manage.py migrate
heroku ps:scale web=1
heroku ps
heroku pg:info
heroku config