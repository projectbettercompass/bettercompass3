from flask import Flask, render_template, request, redirect, make_response
import requests
from datetime import date, datetime
start_time = datetime.now()
import re
import json

# Function to calculate the uptime in seconds
def calculate_uptime():
    current_time = datetime.now()
    uptime = current_time - start_time
    return uptime.total_seconds()


# TODO  
# create a browser extention to automate the cookie process

# Bugs
# more dropdown dosent work when in subpage

app = Flask(__name__)


@app.route('/')
def index():
    # fetch classes for the current day

    session_id = request.cookies.get('session_id')
    prefix = request.cookies.get('prefix')
    user_id = request.cookies.get('user_id')

    if session_id is None or prefix is None or user_id is None:
        return make_response(redirect('/login'))

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
                "endDate": str(date.today()), # YYYY-MM-DD
                "start": 0,
        }).json()['d']


        user = requests.post(
            f'https://{prefix}.compass.education/Services/User.svc/GetUserDetailsBlobByUserId',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
                'Content-Type': 'application/json',
            }, 
            cookies={
                'ASP.NET_SessionId': session_id
            }, 
            json={
                "userId": user_id,
                "targetUserId": user_id,
        }).json()['d']

        # Sort classes by start time
        sorted_events = sorted(response, key=lambda x: x['start']) 
    except:
        print("error in class fetch")
        sorted_events = []
        user = []
    return render_template('index.html', sessions=sorted_events, user=user)

@app.route('/faq')  # New route for /faq
def faq():
    return render_template('faq.html')

@app.route('/howto')  # New route for /howto
def howto():
    return render_template('howto.html')

@app.route('/about')
def about():
    return render_template('about.html', uptime=calculate_uptime())

@app.route('/news')
def news():
    session_id = request.cookies.get('session_id')
    prefix = request.cookies.get('prefix')
    user_id = request.cookies.get('user_id')

    if session_id is None or prefix is None or user_id is None:
        return make_response(redirect('/login'))

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
                "limit": 10,
            }
        ).json()['d']['data']
    except Exception as e:
        print(f"Error in fetching news: {e}")
        news_data = []

    return render_template('news.html', news_data=news_data)

@app.route('/reports')
def get_reports(): 
    session_id = request.cookies.get('session_id')
    prefix = request.cookies.get('prefix')
    user_id = request.cookies.get('user_id')

    if session_id is None or prefix is None or user_id is None:
        return make_response(redirect('/login'))

    try:
        reports = []

        # fetch the report list with the name and id
        data = requests.post(
            f'https://{prefix}.compass.education/Services/Reports.svc/GetMyReportsList',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
            }, 
            cookies={
                'ASP.NET_SessionId': session_id
            }, 
            json={
                "userId": user_id,
            }
        ).json()


        # use the id's to get the url for the report, then append it to an array.
        for report in data['d']:
            url = requests.post(
                f'https://{prefix}.compass.education/Services/LongRunningFileRequest.svc/QueueTask',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
                }, 
                cookies={
                    'ASP.NET_SessionId': session_id
                }, 
                json={
                    "type": "9",
                    "parameters": json.dumps({
                        "cycleId": report['cycleId'],
                        "schoolId": report['schoolId'],
                        "userId": report['userIdForSchool']
                    })
                }
            ).json()

            reports.append({
                'desc': report['t'],
                'url': f"https://{prefix}.compass.education/Services/Reports/Download?cycleId={report['cycleId']}&schoolId={report['schoolId']}&userId={report['userIdForSchool']}&generationSessionId={url['d']}"
            })
    except:
        print("error in report fetch") 

    # Render the reports.html template with the response content
    return render_template('reports.html', reports=reports)

@app.route('/staff')
def staff():

    session_id = request.cookies.get('session_id')
    prefix = request.cookies.get('prefix')
    user_id = request.cookies.get('user_id')

    if session_id is None or prefix is None or user_id is None:
        return make_response(redirect('/login'))

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

    return render_template('staff.html', staff_data=staff_data, prefix=prefix)

@app.route('/tasks')
def tasks():

    session_id = request.cookies.get('session_id')
    prefix = request.cookies.get('prefix')
    user_id = request.cookies.get('user_id')

    if session_id is None or prefix is None or user_id is None:
        return make_response(redirect('/login'))

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
        sorted_tasks = sorted(tasks, key=lambda x: x['students'][0]['submissionStatus'])
    except KeyError:
        # If the expected structure is not found, handle it accordingly
        sorted_tasks = []

    return render_template('tasks.html', tasks=sorted_tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session_id = request.form['session_id']
        prefix = request.form['school_prefix']

        data = requests.get(
            f'https://{prefix}.compass.education/Records/User.aspx',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
                'Content-Type': 'application/json',
            }, 
            cookies={
                'ASP.NET_SessionId': session_id
            }, 
            json={
            }
        ).text

        match = re.search(r'targetUserId: (\w+),', data)

        if match:
            user_id = int(match.group(1))

        # Set a cookie on the browser end
        response = make_response(redirect('/'))
        response.set_cookie('user_id', str(user_id), max_age=31536000)  # 1 year 
        response.set_cookie('session_id', str(session_id), max_age=60*60*24)  # 1 day
        response.set_cookie('prefix', str(prefix), max_age=31536000)  # 1 year 

        return response

    return render_template('login.html')

@app.route('/mainLogin')
def mainLogin():
    return render_template('mainLogin.html')
 

if __name__ == '__main__':
    app.run(debug=True)
