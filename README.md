# willdorff.us

## Setup

```sh
python -m venv venv
source venv/bin/activate
pip install -r dev_requirements.txt
./manage.py migrate
./manage.py dev_init # create dummy data
```
