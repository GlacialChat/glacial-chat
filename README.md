Glacial Chat
---

This is a personal app developed by Zihao Xu. (Sorry, this is not an open
project, and we are not looking for active contributions). 

This `django` application utilizes
`dropbox` api to store files, and `heroku` to deploy the app.


Before you start, I would highly recommend creating a visual environment.

    pip install virtualenv
    virtualenv venv
If you're using Windows:

    venv\Scripts\activate

If not:

    source venv/bin/activate

----

 1. To begin, clone this `git` repository by using the following command:
 

In terminal:

    $ cd venv
    $ git clone https://github.com/GlacialChat/glacial-chat.git
    $ cd Chat
    $ pip install -r requirements.txt
 
 2. After successfully cloning the repository, you will need to set a few environment variables:
 
Environment variables:

     DATABASE_URL:         # A heroku postgresql database url to connecting to the database
     DROPBOX_OAUTH2_TOKEN: # The AUTH TOKEN for your DropBox api
     DROPBOX_ROOT_PATH:    # THe root path to store the files in the DropBox
 
 3. Create a `heroku` account, you may register a free account at [heroku login][1].
 
 4. You will need to install [heroku CLI][3] to use the command-line interface, which will make your life a lot
 easier.
 
 5. If you're still having issues with`heroku`, you might want to check `heroku`'s introduction deploying
 with [python and django framework][4].
 
 6. Create a DropBox API access token [here][5].
 7. After you have everything setup, go in terminal type in the following commands (starts with `$`):
 
 
In terminal:
 
    $ git init
    ...
    $ git add .
    $ git commit -m "initial commit"
    ...
    $ heroku login
    Enter your Heroku credentials.
    ...
    $ heroku create
    Creating intense-falls-9163... done, stack is cedar
    http://intense-falls-9163.herokuapp.com/ | git@heroku.com:intense-falls-9163.git
    Git remote heroku added
    $ heroku addons:create heroku-postgresql:hobby-dev 
    $ git push heroku master
    ...
    -----> Python app detected
    ...
    -----> Launching... done, v7
           https://intense-falls-9163.herokuapp.com/ deployed to Heroku
    ...
    $ heroku run python manage.py createsuperuser
    Follow the onscreen prompt
    ...
 8. You're all set! type `heroku open` to view your app in a browser.
 
 If you ever want to run a test server on your local computer, you can do so by typing
 the following in the terminal:
     
 In terminal:
     
     $ heroku local web
 
  [1]: https://id.heroku.com/login
  [2]: https://dashboard.heroku.com/
  [3]: https://devcenter.heroku.com/articles/heroku-cli
  [4]: https://devcenter.heroku.com/articles/deploying-python
  [5]: https://www.dropbox.com/developers/apps/create