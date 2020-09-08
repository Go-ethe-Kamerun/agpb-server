# African German Phrase Book Server

This is (so far) the server application for [The AGPB application](https://www.goethe.de/ins/cm/en/kul/sup/agp.html) .

## Quick start guide

1. From the root of the project, run the following to install requirments
```
pip install -r requirements.txt
```

2. Create the file agpb/config.yaml with the following contents:
```
SECRET_KEY: '$(python -c "import os; print repr(os.urandom(24))")'
SQLALCHEMY_DATABASE_URI: 'mysql://<username>:<password>@<servername>/<dbname>'
SQLALCHEMY_POOL_RECYCLE: 90

```
3. Run the following commands in the python shell in the root of the proejct to create tables for the database tables:
```
>>> from agpb.models import <tables ...>
>>> from mdvt import db
>>> db.create_all()

```
4. Run the project  with `python app.py`

## Extracting data into database
1. Run the followin on python command line
```
>>> from agpb import db
>>> from agpb.db.extract_data import extract_category_data, naviagate_folder, extract_languages
```

2. To get category data use run the following
```
>>> cat_data = extract_category_data('path/to/category_list.csv')
```

3. To extract the languages, run the following
```
>>> folder_list = naviagate_folder('/Path/to/content_folder')
>>> lang_data = extract_languages(folder_list)
```

4. Inserting the data into the database requires adding them into session first then commiting
by running the following
```
    >>> for data in cat_data:
    ...     db.session.add(data)
    >>> db.session.commit()
```
