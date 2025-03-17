# dockertestpackage

This project is for testing a Dockerized Django application, it is a Django Production application deployed on Azure App Services. Followed best production practices in deploying the application. Used github actions to CI and App Services for CD. 

Mention the below variables for production:
![image](https://github.com/user-attachments/assets/3f74e797-ae16-476a-a82f-76a04a055b43)

I used key-vault services to fetch Azure SQL Database Connection String
ALLOWED_HOSTS: It should be the website name, ex: testdockerazure.azurewebsites.net
Regoster an App in Azure EnrtraID and the below 
AZURE_CLIENT_ID: xxxxxxxxxxxxxxxxxxxxx 
AZURE_CLIENT_SECRET: xxxxxxxxxxxxxxxxxxx
AZURE_TENANT_ID: xxxxxxxxxxxxxxxxxxxxxx
CSRF_TRUSTED_ORIGINS: App Serice Name or domain name etc
![image](https://github.com/user-attachments/assets/9d77439a-0b1e-4ec6-ad76-f72248f7c017)
DEBUG: True (For Dev), False for Prod
SECRET_KEY: Unquie key for Prod
SECURE_SSL_REDIRECT: True or False

In connections strings you can give Azure SQL Credentials as well
![image](https://github.com/user-attachments/assets/ac619851-c8b2-45c9-8dc5-7b8ac806ad04)
SQL Connection String
![image](https://github.com/user-attachments/assets/11aa0df9-028f-4321-8a56-9c6061f78581)

Lastly, I created a Docker image that runs both Nginx as a reverse proxy and Gunicorn as an application server using Supervisord to manage these processes. The image includes all necessary system dependencies including ODBC drivers for SQL Server connectivity, creating a production-ready containerized Django application that can handle static files efficiently while properly connecting to Azure SQL Database.


