import requests
import creds

data = requests.get(
    f'https://{creds.prefix}.compass.education/Records/User.aspx',
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Content-Type': 'application/json',
    }, 
    cookies={
        'ASP.NET_SessionId': creds.session_id
    }, 
    json={
    }
).text
print(data)