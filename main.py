from flask import Flask, render_template, request, redirect
import requests
from datetime import date

# TODO 
# add a function to check if the cookie is still valid


# All user data
session_id = '0'
user_id = 0
prefix = '0-0'

logged_in = True

app = Flask(__name__)

# check on each requst if user is logged in. 
@app.before_request
def check_login():
    global logged_in
    if not logged_in and request.endpoint not in ['login', 'static', 'faq']:
        return redirect('/login')

@app.route('/')
def index():
    # fetch classes for the current day
    try:
        response = requests.post(
            f'https://{prefix}.compass.education/Services/Calendar.svc/GetCalendarEventsByUser?sessionstate=readonly',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
                'Content-Type': 'application/json',
            }, 
            cookies={
                'ASP.NET_SessionId': session_id
            }, 
            json={
                "userId": user_id,
                "startDate": str(date.today()), # YYYY-MM-DD
                "endDate": str(date.today()), 
                "start": 0,
        }).json()['d']

        # Sort classes by start time
        sorted_events = sorted(response, key=lambda x: x['start']) 
    except:
        print("error in class fetch")
        sorted_events = []
    return render_template('index.html', sessions=sorted_events)


@app.route('/faq')  # New route for /faq
def faq():
    return render_template('faq.html')

@app.route('/news')
def news():
    try:
        news_data = requests.post(
            f'https://{prefix}.compass.education/Services/NewsFeed.svc/GetMyNewsFeedPaged?sessionstate=readonly',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
                'Content-Type': 'application/json',
            }, 
            cookies={
                'ASP.NET_SessionId': session_id
            }, 
            json={
                "userId": user_id,
                "start": 0,
        }).json()['d']['data']
    except:
        print("error in class fetch")
        news_data = []

    return render_template('news.html', news_data=news_data)

@app.route('/staff')
def staff():

    response = requests.post(
        f'https://{prefix}.compass.education/Services/User.svc/GetAllStaff',
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
            'Content-Type': 'application/json',
        }, cookies={
            'ASP.NET_SessionId': session_id
        },
        json={
            "userId": user_id,
        }
    )

    try:
        # Try to access the expected structure
        staff_data = response.json()['d']
    except KeyError:
        # If the expected structure is not found, handle it accordingly
        staff_data = []

    return render_template('staff.html', staff_data=staff_data)


@app.route('/tasks')
def tasks():

    response = requests.post(
        f'https://{prefix}.compass.education/Services/LearningTasks.svc/GetAllLearningTasksByUserId?sessionstate=readonly',
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
            'Content-Type': 'application/json',
        }, cookies={
            'ASP.NET_SessionId': session_id
        },
        json={
            "userId": user_id,
            "forceTaskId": 0, 
            "showHiddenTasks": False, 
            "page": 1, 
            "start": 0, 
            "limit": 100, 
        }
    )

    try:
        # Try to access the expected structure
        tasks = response.json()['d']['data']
    except KeyError:
        # If the expected structure is not found, handle it accordingly
        tasks = []

    return render_template('tasks.html', tasks=tasks)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # global session_id, prefix, user_id
        global logged_in
        session_id = request.form['session_id']
        prefix = request.form['school_prefix']
        user_id = request.form['user_id']
        logged_in = True

        print(session_id, prefix, user_id)
        return redirect('/')

    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
