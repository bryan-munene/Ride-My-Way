from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, jsonify, make_response, abort
import os
 
app = Flask(__name__, template_folder = 'templates')

@app.route('/')
def index():
    return render_template("index.html")

#USER SECTION

users = []
 
@app.route('/login')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('dashboard.html')
 
@app.route('/login', methods=['POST'])
def do_user_login():
    user = request.form['username']
    psword = request.form['password']
    if psword == 'password' and user == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/reg")
def register():
    return render_template('reg.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()



#RIDES SECTION

rides = []


@app.route("/ridescreate", methods=["POST"])
def ridescreate():
    if not request.is_json:
        abort(400,"request not json")
    
    if not "driver_id" in request.get_json():
        abort(422,"Ride you are looking for does not exist")

    data = request.get_json()
    ride_id = len(rides)+1
    user_id = data["driver_id"]
    starting = request.form['starting']
    destination = request.form['destination']
    departure = request.form['departure']
    capacity = request.form['capacity']
    full = False
    arrived = False

    ride = {
        "id":ride_id,
        "driver_id":user_id,
        "starting":starting,   
        "destination":destination,
        "leaving":departure,
        "departure":capacity,
        "full":full,
        "arrived":arrived
    }

    rides.append(ride)

    return make_response(jsonify({"status":"created", "ride":ride}),201)
    

@app.route("/rides", methods=["GET"])
def ridesall():
   return make_response(jsonify({"status":"ok", "rides":rides}),200)
    


@app.route('/rides/<int:ride_id>', methods=['GET'])
def specificride(ride_id):
    ride = [ride for ride in rides if ride["id"]==ride_id]
    
    
    if len(ride) == 0:
        return 
        abort(422,"Ride you are looking for does not exist")


    else:
        return 
        make_response(jsonify({"status":"ok", "ride":ride}),200)
        



 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)