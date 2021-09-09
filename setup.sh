# bash

if [[ ! -e settings_local.py ]]; then
    echo 'Creating settings_local.py'
    touch settings_local.py
    echo 'from settings_base import *' > settings_local.py
fi

python3 -m venv venv && \
    source venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt
