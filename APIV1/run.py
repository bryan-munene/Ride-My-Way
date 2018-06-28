from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, jsonify, make_response, abort
import os
 
app = Flask(__name__, template_folder = 'templates')

@app.route('/')
def index():
    return render_template("index.html")


users = [{
        "email": "email",
        "name": "Bryan",
        "psswrd": "passwrd",
        "user_id": 1,
        "username": "Bryan"
    }]


rides = [{
            "arrived": "false",
            "departure": "5m",
            "destination": "Thika",
            "driver_id": 1,
            "full": "false",
            "leaving": "1:00 pm",
            "ride_id": 1,
            "starting": "Juja"
        }]

requests = []

#USER SECTION


class Users(object):
    @app.route('/reg', methods=['POST'])
    def register():
        if not request.is_json:
            abort(400,"request not json")
        

        data = request.get_json() 
        user_id =  len(users)+1
        name = data['name']
        email = data['email']
        username = data['username']
        password = data['password']
        password2 = data['password2']
        
        if not password == password2:
            
            abort(403,"password don't match")

        #user = [user_id, name, email, username, password]
        user = {
             "user_id":user_id,
             "name":name,
             "email":email,   
             "username":username,
             "passwrd":password
         }

        users.append(user)

        return make_response(jsonify({"status":"created", "user":user}),201)


    @app.route('/login')
    def home():
        if not session.get('logged_in'):
            return make_response(jsonify({"status":"login error", "login":False}),401)
        else:
            return make_response(jsonify({"status":"logged in", "login":True}, ),200)
     
    @app.route('/login', methods=['POST'])
    def do_user_login():
        user = request.json['username']
        psword = request.json['password']

        for user in users:
            u = user.get('username')
            p = user.get('password')

        if psword == p and user == u:
            session['logged_in'] = True
        else:
            session['logged_in'] = False
            
        return Users.home()



    @app.route("/logout")
    def logout():
        session['logged_in'] = False
        return Users.home()



#RIDES SECTION

class Rides(object):
    @app.route("/ridescreate", methods=["POST"])
    def ridescreate():
        if not request.is_json:
            abort(400,"request not json")
        
        for user in users:
            user_id= user.get('user_id')
        

        if user_id == (0):
            abort(422,"driver_id does not exist")
   

        data = request.get_json()
        ride_id = len(rides)+1
        driver_id = user_id
        starting = data['starting']
        destination = data['destination']
        departure = data['departure']
        capacity = data['capacity']
        full = False
        arrived = False

        ride = {
            "ride_id":ride_id,
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
        ride = [ride for ride in rides if ride["ride_id"]==ride_id]
        
        
        if len(ride) == 0:
            return 
            abort(422,"Ride you are looking for does not exist")


        else:
            return 
            make_response(jsonify({"status":"ok", "ride":ride}),200)
        

#REQUESTS SECTION

class Request(object):
    @app.route('/rides/<int:ride_id>/requests', methods=['POST'])
    def requests(ride_id): 

        if not request.is_json:
            abort(400,"request not json")
        
        if not 'passenger_id' in request.get_json():
            abort(422,"passenger_id missing")
        
        data = request.get_json()
        passenger_id = data['passenger_id']
        pickup = data['pickup']

        request = {
            "request_id":len(requests)+1,
            "ride_id":ride_id,
            "passenger_id":passenger_id,
            "pickup":pickup,
            "status":False
        }
        
        requests.append(request)
        return make_response(jsonify({"status":"created","request":request, "requests":requests}),201)
        


 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)