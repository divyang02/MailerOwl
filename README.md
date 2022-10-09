<h1 align="center">
  MailerOwl - All in one Email Marketing Solution 
  
  [![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/) 
  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7172676.svg)](https://doi.org/10.5281/zenodo.7172676)

</h1>

<!--Badges-->
<div align="center">

[![CircleCI](https://circleci.com/gh/divyang02/MailerOwl.svg?style=svg)](https://circleci.com/gh/divyang02/MailerOwl)
[![codecov](https://codecov.io/gh/divyang02/MailerOwl/branch/main/graph/badge.svg?token=O8AVQ0MZLR)](https://codecov.io/gh/divyang02/MailerOwl)
[![Python Style Checker](https://github.com/divyang02/MailerOwl/actions/workflows/style_checker.yml/badge.svg)](https://github.com/divyang02/MailerOwl/actions/workflows/style_checker.yml)
[![Formatting python code](https://github.com/divyang02/MailerOwl/actions/workflows/code_formatter.yml/badge.svg)](https://github.com/divyang02/MailerOwl/actions/workflows/code_formatter.yml)
[![Lint Python](https://github.com/divyang02/MailerOwl/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/divyang02/MailerOwl/actions/workflows/main.yml)

</div>

<p align="center">
<a href="https://github.com/divyang02/MailerOwl/blob/main/LICENSE" target="blank">
<img src="https://img.shields.io/github/license/divyang02/MailerOwl?style=for-the-badge" alt="MailerOwl license" />
</a>
<a href="https://github.com/divyang02/MailerOwl/fork" target="blank">
<img src="https://img.shields.io/github/forks/divyang02/MailerOwl?style=for-the-badge" alt="MailerOwl forks"/>
</a>
<a href="https://github.com/divyang02/MailerOwl/stargazers" target="blank">
<img src="https://img.shields.io/github/stars/divyang02/MailerOwl?style=for-the-badge" alt="MailerOwl stars"/>
</a>
<a href="https://github.com/divyang02/MailerOwl/issues" target="blank">
<img src="https://img.shields.io/github/issues/divyang02/MailerOwl?style=for-the-badge" alt="MailerOwl issues"/>
</a>
<a href="https://github.com/divyang02/MailerOwl/issues" target="blank">
<img src="https://img.shields.io/github/issues-closed/divyang02/MailerOwl?style=for-the-badge&label=issues%20closed" alt="MailerOwl issues-closed"/>
</a>
<a href="https://github.com/divyang02/MailerOwl/pulls" target="blank">
<img src="https://img.shields.io/github/issues-pr/divyang02/MailerOwl?style=for-the-badge" alt="MailerOwl pull-requests"/>
</a>
<a href="https://github.com/divyang02/MailerOwl/graphs/contributors" alt="MailerOwl Contributors">
<img src="https://img.shields.io/github/contributors/divyang02/MailerOwl?style=for-the-badge" /></a>
</a>
<a href="https://github.com/divyang02/MailerOwl/graphs/commit-activity" alt="MailerOwl commit activity">
<img src="https://img.shields.io/github/commit-activity/w/divyang02/MailerOwl?style=for-the-badge" /></a> 
</a>
<a href="https://img.shields.io/github/repo-size/divyang02/MailerOwl" alt="MailerOwl repo size">
<img src="https://img.shields.io/github/repo-size/divyang02/MailerOwl?style=for-the-badge" /></a>
</a>
<a href="https://img.shields.io/tokei/lines/github/divyang02/MailerOwl" alt="MailerOwl total lines">
<img src="https://img.shields.io/tokei/lines/github/divyang02/MailerOwl?style=for-the-badge" /></a> 
</a>
</p>

<p align="center">
    <a href="https://github.com/divyang02/MailerOwl/issues/new/choose">Report Bug</a>
    ·
    <a href="https://github.com/divyang02/MailerOwl/issues/new/choose">Request Feature</a>
</p>

<p>MailerOwl provides user functionality to schedule, send instant or recurring emails. User can also check the status of the emails from admin panel. Through our application, a user can schedule recurring emails to be sent over a particular duration that can be decided by the user. This product can be used by marketing teams to advertise their products and promotions to daily customers over a regular period of time.</p>

<h1>🏆 Features</h1>

<ul>
  <li>Sending Email</li>
  <li>Email Scheduling</li>
  <li>Send Recurring Email</li>
  <li>Check Email Logs</li>
</ul>

<h1>🚀 Demo</h1>



<h1>📖 Documentation</h1>
The detailed documentation for the code can be found at - <a href="https://divyang02.github.io/MailerOwl/">MailerOwl Docs</a>

<h1>🛠  Installation Guide</h1>

  1. Install <a href="https://www.docker.com/">Docker</a> on your operating system.
  2. Clone the github repository at a preferable location in your system.
  ```
  git clone https://github.com/divyang02/MailerOwl.git
  cd MailerOwl
  ```
  3. Create your account on <a href="https://www.mailjet.com/">MailJet</a> and generate an API Key and API Secret Token.
  4. Copy the content of mail_sender.settings.py and make a new file local_settings.py in the same folder.
  5. Update MAILJET_API_KEY and MAILJET_API_SECRET fields in the local_settings.py.
  6. In local_settings.py update NAME, PASSWORD and USER fields as per your database config as written in docker-compose file in DATABASES dictionary
  7. Go to apps/email_scheduler/constants.py and update DEFAULT_FROM_EMAIL.
  8. Run ```docker compose up``` in a new terminal.
  9. Open another terminal and run the command ```docker exec -it mail_sender sh ```.
  10. In this terminal run the command ``` python manage.py createsuperuser --settings=mail_sender.local_settings```.
  11. Open your browser and go to 0.0.0.0:8000/admin.
  12. Login with your login credentials and enjoy the application.

<h1>TroubleShooting and Help Guide</h1>

 1. For any issues faced while using the application, please email the detailed description and steps to reproduce the error at mailerowl@proton.me .
 2. If you are a developer, please raise an issue on github with steps to reproduce and possible source of error.
 3. Our email is monitored 24x7 and we usually respond within 1 hour. Happy Emailing :).

<h1>🎯 Plan of Action</h1>

<h2>Phase 1</h2>

1. Implement user registration and login functionality.
2. UI for user login and registration.
2. Implement simple email sending feature using Mailjet API.
3. Add feature to allow users to schedule emails.
4. Add recurring email functionality.
5. Include application logging to monitor status of the emails.
5. Dockerize the application
6. Deploying applicatin on server

<h1>🍰 Contributing</h1>

Please contribute using [GitHub Flow](https://guides.github.com/introduction/flow). Create a branch, add commits, and [open a pull request](https://github.com/divyang02/MailerOwl/pulls).

Please read [`CONTRIBUTING`](CONTRIBUTING.md) for details on our [`CODE OF CONDUCT`](CODE_OF_CONDUCT.md), and the process for submitting pull requests to us.



<h1> 👥 Contributors <a name="Contributors"></a> </h1>

### Group 46

<table>
  <tr>
    <td align="center"><a href="https://github.com/divyang02"><img src="https://avatars.githubusercontent.com/u/23277855?v=4" width="75px;" alt=""/><br /><sub><b>Divyang Doshi</b></sub></a></td>
    <td align="center"><a href="https://github.com/gargpriyam21"><img src="https://avatars.githubusercontent.com/u/32238511?v=4" width="75px;" alt=""/><br /><sub><b>Priyam Garg</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/bhansaliyash"><img src="https://avatars.githubusercontent.com/u/21220880?v=4" width="75px;" alt=""/><br /><sub><b>Yash Bhansali</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/devmehta1999"><img src="https://avatars.githubusercontent.com/u/48157574?v=4" width="75px;" alt=""/><br /><sub><b>Dev Mehta</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/manognapc"><img src="https://avatars.githubusercontent.com/u/112452957?v=4" width="75px;" alt=""/><br /><sub><b>Manogna Choudary Potluri</b></sub></a><br /></td>
  </tr>
</table>
