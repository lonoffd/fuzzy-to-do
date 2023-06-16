# Fuzzy To-Do List

A to-do list powered by flask with tasks that should be done no sooner than a certain amount of time, and no later than another amount of time.

It can only be run locally right now.

## Setup

1. Create virtual environment (or use your favorite virtual environment manager)
```
python3 -m venv venv
source venv/bin/activate
```
2. Install dependencies
```
pip install -r requirements.txt
```

3. Initialize database
```
python db_create.py
```

4. Run the app
```
python fuzzytodo.py
```
