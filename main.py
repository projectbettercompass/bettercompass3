from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Make it so when the user logs in it asks for the school prefix, ASP cookie and uid
    url = 'https://prefix.compass.education/Services/Calendar.svc/GetCalendarEventsByUser?sessionstate=readonly'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Content-Type': 'application/json',
    }

    # Put your user id in the "userId" value
    # You can change the date of the calendar view here
    data = {
        "userId": "1",
        "startDate": "2023-11-27",
        "endDate": "2023-11-27",
        "start": 0,
        # also if u can make it automatically show the data for the current day that would be great
    }

    # Put your session key here
    cookies = {
        'ASP.NET_SessionId': ''
    }

    response = requests.post(url, headers=headers, cookies=cookies, json=data)
    sessions = response.json()['d']

    return render_template('index.html', sessions=sessions)


@app.route('/faq')  # New route for /faq
def faq():
    return render_template('faq.html')

@app.route('/news')
def news():
    url = 'https://prefix.compass.education/Services/NewsFeed.svc/GetMyNewsFeedPaged?sessionstate=readonly'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Content-Type': 'application/json',
    }

    # Put your session key here
    cookies = {
        'ASP.NET_SessionId': ''
    }

    # Data to be included in the request payload
    data = {
        "userId": 1,
        "limit": 10,
        "start": 0,
    }

    response = requests.post(url, headers=headers, cookies=cookies, json=data)

    try:
        # Try to access the expected structure
        news_data = response.json()['d']['data']
    except KeyError:
        # If the expected structure is not found, handle it accordingly
        news_data = []

    return render_template('news.html', news_data=news_data)

@app.route('/staff')
def staff():
    url = 'https://prefix.compass.education/Services/User.svc/GetAllStaff'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Content-Type': 'application/json',
    }

    # Put your session key here
    cookies = {
        'ASP.NET_SessionId': ''
    }

    # Data to be included in the request payload
    data = {
        "userId": 1,
        "limit": 10,
        "start": 0,
    }

    response = requests.post(url, headers=headers, cookies=cookies, json=data)

    try:
        # Try to access the expected structure
        staff_data = response.json()['d']
    except KeyError:
        # If the expected structure is not found, handle it accordingly
        staff_data = []

    return render_template('staff.html', staff_data=staff_data)

if __name__ == '__main__':
    app.run(debug=True)
