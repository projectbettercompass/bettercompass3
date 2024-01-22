import requests
import testing.creds as creds
import json


reports = []

# fetch the report list with the name and id
data = requests.post(
    f'https://{creds.prefix}.compass.education/Services/Reports.svc/GetMyReportsList',
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
    }, 
    cookies={
        'ASP.NET_SessionId': creds.session_id
    }, 
    json={
        "userId": creds.user_id,
    }
).json()


# use the id's to get the url for the report, then append it to an array.
for report in data['d']:
    url = requests.post(
        f'https://{creds.prefix}.compass.education/Services/LongRunningFileRequest.svc/QueueTask',
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        }, 
        cookies={
            'ASP.NET_SessionId': creds.session_id
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
        'url': f"https://{creds.prefix}.compass.education/Services/Reports/Download?cycleId={report['cycleId']}&schoolId={report['schoolId']}&userId={report['userIdForSchool']}&generationSessionId={url['d']}"
    })

print(reports)