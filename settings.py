import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SQLITE_DB_PATH = os.environ.get(
    'SQLITE_TEST_DB_PATH',
    'sqlite:////{}/test_app.db'.format(PROJECT_ROOT)
)

sys.path.append(PROJECT_ROOT)
