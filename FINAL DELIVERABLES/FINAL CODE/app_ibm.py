from flask import Flask,request,render_template
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "9rgwTXNNVEK-K7ZBxOJ8ypezVmm8-qZLspTCTlpEoejm"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

@app.route('/')
def home ():
    return render_template("index.html")

@app.route('/prediction',methods = ['post'])

def predict():
    name = request.form['name']
    month = request.form['month']
    dayofmonth = request.form['dayofmonth']
    dayofweek = request.form['dayofweek']
    origin = request.form['origin']
    if (origin == "msp"):
        origin0,origin1,origin2,origin3,origin4 = 0,0,0,0,1
    if (origin == "dtw"):
        origin0,origin1,origin2,origin3,origin4 = 1,0,0,0,0    
    if (origin == "jfk"):
        origin0,origin1,origin2,origin3,origin4 = 0,0,1,0,0
    if (origin == "sea"):
        origin0,origin1,origin2,origin3,origin4 = 0,1,0,0,0
    if (origin == "atl"):
        origin0,origin1,origin2,origin3,origin4 = 0,0,0,1,0  
    destination = request.form['destination']
    if (destination == "msp"):
        destination0,destination1,destination2,destination3,destination4 = 0,0,0,0,1
    if (destination == "dtw"):
        destination0,destination1,destination2,destination3,destination4 = 1,0,0,0,0    
    if (destination == "jfk"):
        destination0,destination1,destination2,destination3,destination4 = 0,0,1,0,0
    if (destination == "sea"):
        destination0,destination1,destination2,destination3,destination4 = 0,1,0,0,0
    if (destination == "atl"):
        destination0,destination1,destination2,destination3,destination4 = 0,0,0,1,0
    dept = request.form['dept']
    arrtime = request.form['arrtime']
    actdept = request.form['actdept']
    dept15 = int(dept)-int(actdept)
    total = [[name,month,dayofmonth,dayofweek,arrtime,dept15,origin0,origin1,origin2,origin3,origin4,destination0,destination1,destination2,destination3,destination4,]]
    
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [['f0','f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','f11','f12','f13','f14','f15']], "values": total}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/a270a246-e678-4ae8-9e7d-1944f4f2b20c/predictions?version=2022-11-11', json=payload_scoring,
     headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    pred = response_scoring.json()
    y_pred = pred['predictions'][0]['values'][0][0]
    if(y_pred==0):
        ans = "The flight will be on time"
    else:
        ans = "The flight will be delayed"
    return render_template("index.html",showcase = ans)    

if __name__ == '__main__' :
 

    app.run(debug= False)
           

