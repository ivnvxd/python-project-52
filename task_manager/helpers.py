import json
import os
from django.test import modify_settings, override_settings


test_english = override_settings(
    LANGUAGE_CODE='en-US',
    LANGUAGES=(('en', 'English'),),
)

remove_rollbar = modify_settings(
    MIDDLEWARE={
        'remove':
            ['rollbar.contrib.django.middleware.RollbarNotifierMiddleware', ]
    }
)


def load_data(path):
    with open(os.path.abspath(f'task_manager/fixtures/{path}'), 'r') as file:
        return json.loads(file.read())
