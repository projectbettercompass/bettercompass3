# A better way to have all the api stuff in one place?

import requests
from creds import *
from datetime import date


urls = {
    'class': {
        'url': f'https://{prefix}.compass.education/Services/Calendar.svc/GetCalendarEventsByUser?sessionstate=readonly',
        'method': requests.post,
        'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
                'Content-Type': 'application/json',
        },
        'cookies': {
                'ASP.NET_SessionId': session_id
        }, 
        'json': {
                "userId": user_id,
                "startDate": str(date.today()), # YYYY-MM-DD
                "endDate": str(date.today()), 
                "start": 0,
        }
    },


    'user_details': f'https://{prefix}.compass.education/Services/User.svc/GetUserDetailsBlobByUserId',
    'news': f'https://{prefix}.compass.education/Services/NewsFeed.svc/GetMyNewsFeedPaged?sessionstate=readonly',
    'staff': f'https://{prefix}.compass.education/Services/User.svc/GetAllStaff',
    'tasks': f'https://{prefix}.compass.education/Services/LearningTasks.svc/GetAllLearningTasksByUserId?sessionstate=readonly',
    'records': f'https://{prefix}.compass.education/Records/User.aspx',

    'user': {
        'url': '',
        'method': '',
        'header': '',
        'cookies': '',
        'json': '',
    }

}


def fetchCompass(resource = '', method = '', url = '', headers = '', cookies = '', json = ''):

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
    })

    if response.status_code == 200:
        return response.json()['d']
    else:
        return response.json()
    


print(fetchCompass('classes'))