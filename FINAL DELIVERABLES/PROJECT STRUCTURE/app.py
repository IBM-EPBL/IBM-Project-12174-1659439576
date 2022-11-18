from flask import Flask,request,render_template
import pickle

model = pickle.load(open('flight.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def home ():
    return render_template("index.html")

@app.route('/prediction',methods = ['post'])

def predict():
    name = request.form['name']
    month = request.form["month"]
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

    y_pred = model.predict(total)
    
    print(y_pred)
    
    if(y_pred==[0]):
        ans = "The flight will be on time"
    else:
        ans = "The flight will be delayed"
    return render_template("index.html",showcase = ans)    

if __name__ == '__main__' :
 

    app.run(debug= False)
           
