### Implementation of a flask server with the ability to accept applications for payment and redirect to payment systems depending on the selected currency

## Technology
***
- Python
- Flask
- SQLite

## Install
***
Run the following commands to bootstrap your environment
```   
git clone https://github.com/YaroslavOvchinnikov/test_task_involve
cd test_task_involve
pip install -r requirements.txt
```

The project uses a SQLite database if you don't have this database installed, you can download it from https://www.sqlite.org/

Run the following command
```
pip install sqlite3
```

## Start application
***
Run the following command
```
python app.py
```



## Project content
***
app.py - contains the main functionality of the project.

FDataBase.py - the file contains the code for working with the database.

Static - folder with styles for site pages.

Templates - folder with html files.
