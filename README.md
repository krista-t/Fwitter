# Fwitter

Twitter-like (not X) clone with Pyhon, Sqlite, JS, and TailwindCSS. You can make an account, post tweet with images, upload profile photo, and edit or delete your tweets. Authentication is done with JWT. Once you sign up, make sure to login with the same credentials on home page. App is deployed on PythonAnywhere, and can be found at https://twtterclone.eu.pythonanywhere.com/

FTweet away!

# validator.js

Vanilla JS validation made by Santiago Donoso, and changed to fit into this project

# starting the project

python3 -m venv/path/to/new/virtual/environment

source/path/to/new/venv/bin/activate

pip install bottle
pip install paste
pip install pyjwt

npm install -d tailwindcss@latest postcss@latest autoprefixer@latest (you shoud have node.js already installed)

# running for development

from tailwindcss folder:
npx tailwindcss -i tailwind.css -o ../app.css --watch

python3 app.py

# warning

be ware that any interaction with the app makes changes in database, this includes deleting data
