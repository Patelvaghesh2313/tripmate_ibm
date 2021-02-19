from flask import Flask, render_template, session, g, request, redirect, url_for, flash
from passlib.hash import sha256_crypt
import pyrebase

app = Flask(__name__)
app.secret_key = 'Tripmate'
firebaseConfig = {
    "apiKey": "AIzaSyBz1_qjfCsTjdqvg2fECJmd38M_miSYo20",
    "authDomain": "tripmate-ceb71.firebaseapp.com",
    "databaseURL": "https://tripmate-ceb71-default-rtdb.firebaseio.com",
    "projectId": "tripmate-ceb71",
    "storageBucket": "tripmate-ceb71.appspot.com",
    "messagingSenderId": "207751222121",
  };

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
#user = auth.create_user_with_email_and_password(email,password)
#auth.send_email_verification(user['idToken'])


@app.route('/')
def index():
    return render_template('landingDashboard.html')


#--In this part we write the logic for successfull customer login.---#
@app.route('/customerLogin', methods=['GET', 'POST'])
def customerLogin():
    if request.method == 'GET':
        session.pop('user', None)
        return render_template('customerLogin.html')
    elif request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        customers_data = db.child('customers').child('profiles').get().val()
        temp_list = []
        for i in customers_data:
            temp_list.append(i)
        #temp_emails = []
        #temp_passwords = []
        for i in temp_list:
            c_email = db.child('customers').child('profiles').child(i).child('Email').get().val()
            c_password = db.child('customers').child('profiles').child(i).child('Password').get().val()
            if (email == c_email) and sha256_crypt.verify(password, c_password):
                session['user'] = c_email
                return redirect(url_for('customerPage'))
            #temp_emails.append(c_email)
            #temp_passwords.append(c_password)
        flash("Incorrect Username And Password !", 'danger')
        return redirect(url_for('customerLogin'))
    return render_template('404.html')


@app.route('/customerRegister', methods=['GET', 'POST'])
def customerRegister():
        if request.method == 'GET':
            session.pop('user', None)
            return render_template('customerRegister.html')
        elif request.method == 'POST':
            customer_fname = request.form.get("customer_fname")
            customer_lname = request.form.get("customer_lname")
            customer_email = request.form.get("customer_email")
            customer_mobilenumber = request.form.get("customer_mobilenumber")
            customer_password = request.form.get("customer_password")
            confirm_password = request.form.get("confirm_password")
            if customer_password == confirm_password:
                secure_password = sha256_crypt.encrypt(str(customer_password))
                customer_details = {"FirstName": customer_fname, "LastName": customer_lname, "Email": customer_email, "MobileNumber": customer_mobilenumber,"Password": secure_password}
                db.child('customers').child('profiles').push(customer_details)
                flash("Hey! You Are successfully Registered. ", 'success')
                return redirect(url_for('customerLogin'))
        else:
            return render_template('404.html')


@app.route('/serviceproviderLogin', methods=['GET', 'POST'])
def serviceproviderLogin():
    if request.method == 'GET':
        session.pop('user', None)
        return render_template('serviceproviderLogin.html')
    elif request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        providers_data = db.child('service_providers').child('shopsDetails').get().val()
        temp_list = []
        for i in providers_data:
            temp_list.append(i)
            #print(temp_list)
        #temp_emails = []
        #temp_passwords = []
        for i in temp_list:
            sp_email = db.child('service_providers').child('shopsDetails').child(i).child('Email').get().val()
            sp_password = db.child('service_providers').child('shopsDetails').child(i).child('Password').get().val()
            if (email == sp_email) and sha256_crypt.verify(password, sp_password):
                session['user'] = sp_email
                return redirect(url_for('customerPage'))
            #temp_emails.append(c_email)
            #temp_passwords.append(c_password)
        flash("Incorrect Username And Password !", 'danger')
        return redirect(url_for('serviceproviderLogin'))
    return render_template('404.html')


@app.route('/serviceproviderRegister', methods=['GET', 'POST'])
def serviceproviderRegister():
    if request.method == 'GET':
        return render_template('serviceproviderRegister.html')
    elif request.method == 'POST':
        sprovider_shop_name = request.form.get("shop_name")
        sprovider_email = request.form.get("provider_email")
        sprovider_servicetype = request.form.get("service_type")
        sprovider_state = request.form.get("state")
        sprovider_city = request.form.get("city")
        sprovider_mobilenumber = request.form.get("mobile_number")
        sprovider_password = request.form.get("provider_password")
        confirm_password = request.form.get("provider_cpassword")
        if sprovider_password == confirm_password:
            secure_password = sha256_crypt.encrypt(str(sprovider_password))
            service_provider_details = {"ShopName": sprovider_shop_name, "Email": sprovider_email,
                                        "ServiceType": sprovider_servicetype, "State": sprovider_state, "City": sprovider_city, "MobileNumber": sprovider_mobilenumber, "Password": secure_password}
            db.child('service_providers').child('shopsDetails').push(service_provider_details)
            flash("Hey! You Are successfully Registered. ", 'success')
            return redirect(url_for('serviceproviderLogin'))
    else:
        return render_template('404.html')
#----After succcessfully logged in Customer -------#


@app.route('/customerPage', methods=['GET'])
def customerPage():
    if g.user:
        return render_template('customerDashboard.html')
    return render_template('404.html')


@app.route('/dashboard/car@accessories', methods=['GET'])
def caraccessories():
    if g.user:
        return render_template('carAccessories.html')
    return render_template('404.html')


#-------------Logout Customer--------------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

#----------- Make Global user Instance -----------
@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


if __name__ == '__main__':
    app.run()
