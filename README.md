# tripmate_ibm
IBM Project semester 8

----------------------------------------
**Notes**
----------------------------------------
1. for design the pages of landing pages, please use "landing_layout.html".
2. To run the application use app.py
3. for design the customer pages use "user_layout.html"
4. In the **static** folder put your all static files ( ex. css,js etc)
5. in the **templates** folder put your all html files

------------------------------------------
DEPLOY APP ON HEROKU 
------------------------------------------
Step 1: Register on Heroku.com and Download Heroku CLI

Step 2: Go in to your Project directory and activate your virtual Environment

Step 3: **pip install gunicorn** - package for initialize our app as web app

Step 4: Create **Procfile** and inside it write below oneline code
        - web: gunicorn app: < your application .py name > (ex. here filename is app.py so app:app )
        
Step 5: **pip freeze > requirements.txt** - it makes list of all required packages in **requirements.txt** file

Step 6: **git init** -to initialize empty git repository for project as master branch

Step 7: **git add .** - to add all files in empty git repository

Step 8: **git commit -m "< appropriate message>"** - to commit the changes

Step 9: **heroku login** - to login in heroku web

Step 10: **heroku create** - for creating a app on heroku

Step 11: **heroku rename your_app_name** - for rename heroku app

Step 12: **git push heroku master** - to push the whole project on heroku master branch

Step 13: At the end of whole above process whatever URL will generate, put it into Browser and run
