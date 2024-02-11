# Requirements

 - Python 3
 - Chrome or Firefow browser

# Installation

virtualenv

    pip install virtualenv

Enter app floder

    cd twitter_config_ui
  
create env

    virtualenv my_env

activate env

    source my_env/bin/activate

activate env windows version

     .\my_env\Scripts\activate


install app requirements

    pip install -r requirements.txt

Start app

    FLASK_APP=app
    flask run

Start app windows version

    set FLASK_APP=app
    flask run

Now visit url http://127.0.0.1:5000/ on your browser