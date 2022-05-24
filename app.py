from flask import Flask, render_template, request

app = Flask(__name__)

L=[]

@app.route("/",methods=["POST","GET"])
def home(): 
    return render_template('index.html')



@app.route("/form",methods=["POST","GET"])
def form1():
    FisrtName = request.form.get("FisrtName")
    LastName = request.form.get("LastName")
    Email = request.form.get("Email")
    Country = request.form.get("Country")
    Tel = request.form.get("Tel")
    Password = request.form.get("Password") 
    if  request.form.get("FisrtName"):
        return render_template('Thanks.html')
    return render_template('fail.html',LastName=LastName)

@app.route("/newsletter",methods=["POST","GET"])
def newsletter():
    return render_template('newsletter.html')



@app.route("/Thanks", methods=["POST"])
def Thanks():
    email = request.form.get("email")
    if not email:
        return render_template('fail.html')
    return render_template('Thanks.html')





if __name__=='__main__':
    app.run(debug=True)