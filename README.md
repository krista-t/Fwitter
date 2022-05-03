# Fwitter
Twitter like clone with Pyhon, Sqlite, JS, and TailwindCSS

# validator.js
Vanilla JS validation made by Santiago Donoso, and changed slightly to fit into this project

# starting the project
python3 -m venv /path/to/new/virtual/environment

source /path/to/new/venv/bin/activate

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


