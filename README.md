# Comment Reviewer

[![Build Status](https://travis-ci.org/pennlabs/pcr-reviewer.svg?branch=master)](https://travis-ci.org/pennlabs/pcr-reviewer)

An internal tool used to review student comments for Penn Course Review.

## Installing

```bash
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py runserver
```

### Importing Comments

To import comments from a raw Oracle sql file, you can run `./manage.py load_comments <input filename>`.

### Exporting Comments

To export reviewed comments to json format, you can run `./manage.py export_comments <output filename>`.

Sample Output Format:
```json
[
    {
        "comments": [
            "This is an example comment!",
            "This is another example comment!"
        ],
        "instructor": {
            "id": 00000000,
            "name": "LASTNAME,FIRSTNAME"
        },
        "section": "DEPT000111",
        "tags": [
            "tag1",
            "tag2"
        ],
        "term": "2017A"
    },
    ...
]
```
