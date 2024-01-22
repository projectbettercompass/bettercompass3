# Have all the endpoints in one function for testing stuff/refrence

import requests
from testing.creds import *
from datetime import date


def fetchCompass(resource, headers = '', cookies = '', json = ''):
    # class, user_details, news, staff, tasks, reports
    endpoints = {
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


        'user_details': {
            'url': f'https://{prefix}.compass.education/Services/User.svc/GetUserDetailsBlobByUserId',
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
                    "targetUserId": user_id,
            }
        },

        'news': {
            'url': f'https://{prefix}.compass.education/Services/NewsFeed.svc/GetMyNewsFeedPaged?sessionstate=readonly',
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
                    "start": 0,
                    "limit": 10,
            }
        },

        'staff': {
            'url': f'https://{prefix}.compass.education/Services/User.svc/GetAllStaff',
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
            }
        },

        'tasks': {
            'url': f'https://{prefix}.compass.education/Services/LearningTasks.svc/GetAllLearningTasksByUserId?sessionstate=readonly',
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
                "forceTaskId": 0, 
                "showHiddenTasks": False, 
                "page": 1, 
                "start": 0, 
                "limit": 100, 
            }
        },

        'reports': {
            'url': f'https://{prefix}.compass.education/Services/Reports.svc/GetMyReportsList',
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
            }
        },

        'description': {
            'url': '',
            'method': '',
            'headers': '',
            'cookies': '',
            'json': '',
        }
    }

    # the recource is required. Values if passed to the function are used instead of defaults.
    response = endpoints[resource]['method'](
            url = endpoints[resource]['url'],
            headers = headers if headers else endpoints[resource]['headers'], 
            cookies = cookies if cookies else endpoints[resource]['cookies'], 
            json = json if json else endpoints[resource]['json']
    )

    # error checking and results returned
    if response.status_code == 200:
        return response.json()['d']
    else:
        return response.json()



print(fetchCompass(resource='class', json = {
                    "userId": user_id,
                    "startDate": "2024-01-05", # YYYY-MM-DDstr(date.today())
                    "endDate": "2024-01-05", 
                    "start": 0,
            }))