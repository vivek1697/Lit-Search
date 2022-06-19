## Run locally

Working on containerizing the application for easier local runs. Until then, please follow instructions.
1. Clone the repository
```
git clone https://github.com/vivek1697/Lit-Search.git
```

2. Create and activate virtual environment
```
# Create
virtualenv venv --python=python3

# Activate
source venv/bin/activate (for mac)
venv\Scripts\activate (for win)
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Scrape data and create records in database
```
python web_scrapper.py
```

5. Run server
```
export FLASK_APP=app
flask run -p 5001
```