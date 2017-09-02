import requests
import pandas
import re
from datetime import datetime, timedelta
from io import StringIO
from math import ceil
import json

#List of Survey Site Impression IDs with Survey Names 
survey_list = {'Survey1':'SI_xxxxx',
                'Survey2':'SI_xxxx'}

#Qualtrics ID (to access API)
myID = 'abc@xyz.com'

#Token of above Qualtrics ID
myToken = 'xxxxxx'

#Snippet to Auto-set Start and End as previous week's Monday to Sunday respectively 
dt = datetime.strftime(datetime.today() - timedelta(days=7),'%Y-%m-%d')
dt = datetime.strptime(dt, '%Y-%m-%d') 
start = dt - timedelta(days=dt.weekday())
end = start + timedelta(days=7)
start = datetime.strftime(start,'%Y-%m-%d')
end = datetime.strftime(end,'%Y-%m-%d')
#start = '2017-05-01 00:00:00'
#end = '2017-06-01 00:00:00'

def extract_impressions(mySurvey):
   
    url = "https://survey.qualtrics.com//WRAPI/SiteIntercept/api.php?Request=getInterceptStats&Version=2.0&User="+myID+"&Token="+myToken+"&Format=JSON&InterceptID="+mySurvey+"&StartDate="+start+"&EndDate="+end+"&DataType=Impressions&Interval=Day"
    r = requests.get(url)
    p = json.loads(r.text)
    pss = pandas.DataFrame((p['Result']['Data']).items(),columns=['Date','Impressions'])
    return(pss['Impressions'].sum())
    
print(start,end)
result = {}
for mySurvey in survey_list:
    result[mySurvey] = extract_impressions(survey_list[mySurvey])
result_df = pandas.DataFrame(result.items(),columns=['Survey Name','Impressions Count'])
print(result_df)
