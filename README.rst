Transactions Application
========================


This repository contains the backend and frontend code for maintaining transactions of a user

Sample postman API Link: - https://documenter.getpostman.com/view/2450865/UyxjF5qM

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