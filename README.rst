Transactions Application
========================


This repository contains the backend and frontend code for maintaining transactions of a user

Deployment Link: - 

Admin: - http://backend-env.eba-ppi2dpjv.us-west-2.elasticbeanstalk.com/admin/

API: - http://backend-env.eba-ppi2dpjv.us-west-2.elasticbeanstalk.com/api

Sample postman API Link: - https://documenter.getpostman.com/view/2450865/UyxjF5qM


Enhancements:-
^^^^^^^^^^^^

1. Frontend and Backend repository should be separately maintained.

2. Need of more validations while accepting data via API.

3. Add tests for few more APIs.

4. Frontend is partially implemented and does not have the UI to mark transactions as paid.

5. No tests added for Vue frontend

6. Minimal UI is implemented and missing the line chart for showing data over time on the UI.

Requirements
^^^^^^^^^^^^

- Python 3.6 and above
- Django 4.0.4


Installation
^^^^^^^^^^^^

- Installing system requirements
      
      
      **Debian/Ubuntu**
          
      ::
       
          $ sudo apt-get install python3-dev default-libmysqlclient-dev
      
      
      **Centos/RedHat**
          
      ::
          
          $ sudo yum install python3-devel mysql-devel
  
  
-  Clone the repository

      ::

          $ git clone https://github.com/adityacp/transactions.git

-  Go to the project directory

      ::

          $ cd transactions/backend


- Installing project packages

      ::

          $ pip install -r requirements.txt


- Run migrations commands

      ::

          $ python manage.py makemigrations
          $ python manage.py migrate


- Create superuser

      ::

          $ python manage.py createsuperuser


- Run server Locally
      
      ::

          $ python manage.py runserver
