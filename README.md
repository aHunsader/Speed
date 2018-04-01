# How to run website:
1. download all requirements in requirements.txt
In separate terminal tabs:
2. redis-server --daemonize yes
3. ./manage.py runserver
4. celery -A speed.celeryconfig worker -l info --concurrency=1
Optional (for testing purposes):
5. ./client.py



# Speed
Web &amp; android applications to help a parent monitor his/her childrens' driving

## Inspiration
This application was inspired by the vast amounts of car crashes that occur in the United States every day because of reckless driving. 

## What it does
This system allows parents to see where their children are when they are driving along with their speed, the speed limit, the acceleration, etc. It works by having the child open the app on their phone whenever they start driving. The phone then takes measurements that can be used to see whether the child is safe. For example, when the driver is more than 10 mph over the speed limit, the parent is notified with a text message. In addition, when the acceleration is very high, a crash could have occurred, which also warrants an precautionary text message.

## How we built it
A celery server was created behind the web application to accept connections and data (coordinates, acceleration, username, etc.). This data was then processed (finding velocity, sending twilio texts, etc.) and sent to the front-end (html, javascript) via django-channels websockets. These websockets allowed parents to receive only the data from their own children. At the front-end, the data was displayed real-time and updated a google maps frame so a parent could see the location of the currently driving children.

In the android application, the login process was done via comparing username/password hashes with those stored in amazon rds (from the django models). Once logged in, the android application opened a client connection to the celery server where it sent data periodically.

## Challenges we ran into
We had much difficulty getting the geographical coordinates and acceleration measurements from the android phone. We also had difficulty using the google maps api to display a map in the android application.

## Accomplishments that we're proud of
We created a fully functioning web application with an almost-complete android application. All of the real-time data and socket implementations were completed.

## What we learned
We learned about real-time notifications with django, google-maps api use, and android mobile application development.
## What's next for Speed
We want to extend this idea by adding features that look for swerving and other dangerous driving patterns to help parents keep their children and other drivers safe on the road. We also plan to develop an iOS application for non-android users.

