# Location

Hi. (I thought that keeping the socket program in a seperate branch and working on the Django project in the master branch would be more appropriate.)

Simply git-clone the project and then run 'python3 manage.py runserver' inside Location folder(if you have Django installed). You should be able to see the list of maps at 'http://127.0.0.1:8000/eventmap/' .

(I used the 'websocket hack' that OTS had provided to implement watchArea.)

You might have to install 'websockets' library:
sudo pip3 install websockets

Then, run this inside Location folder :
LocationBasedEvents/wsnotifier.py 127.0.0.1:9999 0.0.0.0:5678

When a new notification has arrived, user sees it at the top of the page.
