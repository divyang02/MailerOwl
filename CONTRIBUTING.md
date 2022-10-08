# WELCOME TO CONTRIBUTING :)
If you would want to contribute to this repository, e-mail the repository's owner first with your suggested changes.
Please abide by the code of conduct that is mentioned in our repository. Additionally, closely adhere to our table of contents and make the necessary adjustments. 

# Pull Request Process
1. Pass all the test cases that we have developed in the tests folder.
2. Add any new installatiuon dependencies in the requirements.txt file.
3. Add unnecessary build files to the .gitignore file.
4. Update README.md with the changes you have made.

# Committing Changes
1. Create an issue on the project kanban board and move the issue to In Progress.
2. Clone the repository in your local system. 
3. Create your personal branch. Switch to your branch using git checkout.
4. Make the required changes and commit to your personal branch.
5. Create a new pull request.

# Our Table Of Contents

```
── CODE_OF_CONDUCT.md
├── Dockerfile
├── LICENSE
├── README.md
├── CONTRIBUTING.md
├── apps
│   ├── __init__.py
│   ├── email_scheduler
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── constants.py
│   │   ├── email_sender
│   │   │   ├── __init__.py
│   │   │   ├── abstract_email_sender.py
│   │   │   └── mailjet_email_sender.py
│   │   ├── exceptions.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── services.py
│   │   ├── tasks.py
│   │   └── tests
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_services.py
│   │       └── test_tasks.py
│   └── registration
│       ├── __init__.py
│       ├── apps.py
│       ├── forms.py
│       ├── migrations
│       │   └── __init__.py
│       ├── templates
│       │   └── registration
│       │       ├── home.html
│       │       ├── login.html
│       │       └── user_registration.html
│       ├── tests
│       │   ├── __init__.py
│       │   ├── test_forms.py
│       │   └── test_views.py
│       ├── urls.py
│       └── views.py
├── docker-compose.yml
├── mail_sender
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── test_settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── templates
    └── base.html
```

## Code of Conduct
This project and everyone participating in it is governed by the [Code of Conduct](https://github.com/divyang02/MailerOwl/blob/main/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to gargpriyam21@gmail.com.

# Attribution
Code of Conduct was adapted from [Contributor Covenant][homepage],
version 2.0, available at
https://www.contributor-covenant.org/version/2/0/code_of_conduct.html.
