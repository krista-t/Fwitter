# Fwitter

Twitter clone made with Pyhon, Sqlite, JS, and TailwindCSS. Make an account, post tweet, images, upload profile photo, and edit or delete your tweets. Authentication done via JWT. Once you sign up, make sure to login with the same credentials on home page. App is deployed on PythonAnywhere, and can be found at https://twtterclone.eu.pythonanywhere.com/
FTweet away! 

# validator.js

Vanilla JS validation made by Santiago Donoso, and changed to fit into this project

# starting the project

python3 -m venv/path/to/new/virtual/environment

source/path/to/new/venv/bin/activate

pip install bottle, paste, pyjwt

npm install -d tailwindcss@latest postcss@latest autoprefixer@latest (you shoud have node.js already installed)

# running for development

from tailwindcss folder:
npx tailwindcss -i tailwind.css -o ../app.css --watch

python3 app.py


