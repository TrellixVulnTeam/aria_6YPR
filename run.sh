#!/bin/bash
cd /var/lib/jenkins/workspace/python_api
/usr/local/python3/bin/pipenv run pytest tests/test_B_add_people_into_company.py
python3 utils/send_email.py