# Requirements

 - Python  3.10 
 - Chrome or Firefow browser
 - Webdriver needed in /data/drivers/
# Installation

virtualenv

    pip install virtualenv

Enter app floder

    cd twitter_automated_search_cli
  
create env

    virtualenv my_env

activate env

    source my_env/bin/activate

activate env windows version

     .\my_env\Scripts\activate



install other requirements

    pip install -r requirements.txt

# Launch

    python process.py TWXT_output=/path/to/twxt/jsonfiles/ output=path/to/output/data/ n_branches=1
example

    python process.py TWXT_output=C:\Users\pc_tintou\Desktop\data\twitter_livraison\data\ output=C:\Users\pc_tintou\Desktop\data\twitter_livraison\data\output\ n_branches=3
