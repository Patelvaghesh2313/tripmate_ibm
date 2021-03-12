from flask import Flask, render_template, session, g, request, redirect, url_for, flash
from passlib.hash import sha256_crypt
import pyrebase
from flask_mail import *
from random import *
import requests,json

app = Flask(__name__)
app.secret_key = 'Tripmate'

#----------------FireBase Configuration Part--------------#

firebaseConfig = {
    "apiKey": "AIzaSyBz1_qjfCsTjdqvg2fECJmd38M_miSYo20",
    "authDomain": "tripmate-ceb71.firebaseapp.com",
    "databaseURL": "https://tripmate-ceb71-default-rtdb.firebaseio.com",
    "projectId": "tripmate-ceb71",
    "storageBucket": "tripmate-ceb71.appspot.com",
    "messagingSenderId": "207751222121",
  }

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

#user = auth.create_user_with_email_and_password(email,password)
#auth.send_email_verification(user['idToken'])

#----------------End Of FireBase Configuration Part--------------#


#-----------------Email Server Configuration------------------#
# make sure you enable less secure apps for your email #
app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'kingpatel8122@gmail.com',
    MAIL_PASSWORD = '347676747926vir',
))


mail = Mail(app)
otp = randint(000000, 999999)

#-----------------End Of Email Server Configuration----------------#


#-----------------Landing Page Route-------------------#


@app.route('/')
def index():
    return render_template('landingDashboard.html')


##---------Start Of Register and Login Modules--------##
def customerData():
    customers_data = db.child('customers').child('profiles').get().val()
    temp_list = []
    for i in customers_data:
        temp_list.append(i)
    return temp_list

def serviceProviderData():
    providers_data = db.child('service_providers').child('shopsDetails').get().val()
    temp_list = []
    for i in providers_data:
        temp_list.append(i)
    return temp_list


@app.route('/customerLogin', methods=['GET', 'POST'])
def customerLogin():
    if request.method == 'GET':
        session.pop('user', None)
        return render_template('customerLogin.html')
    elif request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        temp = customerData()
        for i in temp:
            c_email = db.child('customers').child('profiles').child(i).child('Email').get().val()
            c_password = db.child('customers').child('profiles').child(i).child('Password').get().val()
            if (email == c_email) and sha256_crypt.verify(password, c_password):
                session['user'] = c_email
                return redirect(url_for('customerDashboard'))
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
                flash("Try Again ! Something Went Wrong", 'danger')
                return redirect(url_for('customerRegister'))
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
        temp = serviceProviderData()
        for i in temp:
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
        sprovider_shop_number = request.form.get("s_number")
        sprovider_street_name = request.form.get("street_name")
        sprovider_email = request.form.get("provider_email")
        sprovider_servicetype = request.form.get("service_type")
        sprovider_state = request.form.get("state")
        sprovider_city = request.form.get("city")
        sprovider_mobilenumber = request.form.get("mobile_number")
        sprovider_password = request.form.get("provider_password")
        confirm_password = request.form.get("provider_cpassword")
        if sprovider_password == confirm_password:
            secure_password = sha256_crypt.encrypt(str(sprovider_password))
            service_provider_details = {"Email": sprovider_email, "ShopNumber": sprovider_shop_number,
                                        "ShopName": sprovider_shop_name, "StreetName":sprovider_street_name,
                                        "ServiceType": sprovider_servicetype, "State": sprovider_state,
                                        "City": sprovider_city, "MobileNumber": sprovider_mobilenumber,
                                        "Password": secure_password}
            db.child('service_providers').child('shopsDetails').push(service_provider_details)
            flash("Hey! You Are successfully Registered. ", 'success')
            return redirect(url_for('serviceproviderLogin'))
    else:
        return render_template('404.html')

#---------End Of Register and Login Modules--------#

#---------Start Of Forgot Password Modules--------#


@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    if request.method == 'GET':
        return render_template('forgotpassword.html')
    elif request.method == 'POST':
        requested_email = request.form.get('email')
        temp = customerData()
        for i in temp:
            c_email = db.child('customers').child('profiles').child(i).child('Email').get().val()
            #c_id = db.child('customers').child('profiles').child(i).get().val()
            print(c_email)
            if (requested_email == c_email):
                c_id = i
                session['c_id'] = c_id
                msg = Message('OTP Verification', sender='kingpate8122@gmail.com', recipients=[requested_email])
                msg.body = str(otp)
                mail.send(msg)
                session['email'] = requested_email
                flash("We sent OTP on your email, Check it", 'success')
                return redirect(url_for('otpverification'))

        flash("This Email Doesn't Exist", 'danger')
        return redirect(url_for('forgotpassword'))


@app.route('/otpverification', methods=['GET', 'POST'])
def otpverification():
    if request.method == 'GET':
        return render_template('otpverfication.html')
    elif request.method == 'POST':
        inserted_otp = request.form.get('user_otp')
        if otp == int(inserted_otp):
            flash("Successfully Verified", 'success')
            return redirect(url_for('resetpassword'))
        else:
            flash("OTP Does not match ! Try Again ", 'danger')
            return redirect(url_for('forgotpassword'))


@app.route('/resetpassword', methods=['GET', 'POST'])
def resetpassword():
    if request.method == 'GET':
        return render_template('resetpassword.html')
    elif request.method == 'POST':
        new_password = request.form.get('new_password')
        cnew_password = request.form.get('cnew_password')
        c_id = session['c_id']
        print(c_id)
        if new_password == cnew_password:
            c_email = db.child('customers').child('profiles').child(c_id).child('Email').get().val()
            print(c_email)
            if (session['email'] == c_email):
                secure_password = sha256_crypt.encrypt(str(new_password))
                reset_password = {"Password": secure_password}
                db.child('customers').child('profiles').child(c_id).update(reset_password)
                flash("Password Successfully Updated. ", 'success')
                return redirect(url_for('customerLogin'))


#---------End Of Forgot Password Modules--------#

#----After succcessfully logged in Customer -------#


@app.route('/customer/dashboard', methods=['GET'])
def customerDashboard():
    if g.user:
        return render_template('customerDashboard.html')
    return render_template('404.html')


@app.route('/dashboard/caraccessories', methods=['GET'])
def carAccessories():
    if g.user:
        temp = serviceProviderData()
        ishopname = []
        icity = []
        iemail = []
        inumber = []
        istate = []
        iserviceType = []
        for i in temp:
            print(temp)
            serviceType = db.child('service_providers').child('shopsDetails').child(i).child('ServiceType').get().val()
            print(serviceType)
            if serviceType == 'Accessories':
                shopname = db.child('service_providers').child('shopsDetails').child(i).child('ShopName').get().val()
                state = db.child('service_providers').child('shopsDetails').child(i).child('State').get().val()
                city = db.child('service_providers').child('shopsDetails').child(i).child('City').get().val()
                number = db.child('service_providers').child('shopsDetails').child(i).child('MobileNumber').get().val()
                email = db.child('service_providers').child('shopsDetails').child(i).child('Email').get().val()
                ishopname.append(shopname)
                iemail.append(email)
                icity.append(city)
                istate.append(state)
                inumber.append(number)
                iserviceType.append(serviceType)
            else:
                print('wrong')
        idetails = zip(ishopname, iemail, icity, istate, inumber)
        return render_template('carAccessories.html',details=idetails)
    return render_template('404.html')


@app.route('/dashboard/providerLocation', methods=['GET'])
def serviceProvidersLocation():
    if g.user:
        temp = serviceProviderData()
        for i in temp:
            shopNumber = db.child('service_providers').child('shopsDetails').child(i).child('ShopNumber').get().val()
            shopName = db.child('service_providers').child('shopsDetails').child(i).child('ShopName').get().val()
            streetName = db.child('service_providers').child('shopsDetails').child(i).child('StreetName').get().val()
            shopCity = db.child('service_providers').child('shopsDetails').child(i).child('City').get().val()
            shopState = db.child('service_providers').child('shopsDetails').child(i).child('State').get().val()
            shopFullAddress = str(shopNumber) + str(streetName) + str(shopCity) + str(shopState)

            parameters = {
                "key": "lks2Rcp9AgsAIvmvVAkpFf5t73ruurvy",
                "location": shopFullAddress
            }
            result = requests.get("http://www.mapquestapi.com/geocoding/v1/address", params=parameters)
            data = json.loads(result.text)['results']

            lat = data[0]['locations'][0]['latLng']['lat']
            lng = data[0]['locations'][0]['latLng']['lng']
            print(lat, lng)


@app.route('/dashboard/profile', methods=['GET'])
def profile():
    if g.user:
        temp = customerData()
        for i in temp:
            c_email = db.child('customers').child('profiles').child(i).child('Email').get().val()
            if c_email == session['user']:
                c_fname = db.child('customers').child('profiles').child(i).child('FirstName').get().val()
                c_lname = db.child('customers').child('profiles').child(i).child('LastName').get().val()
                c_mobile = db.child('customers').child('profiles').child(i).child('MobileNumber').get().val()
                c_data = {
                    "fname": c_fname,
                    "lname": c_lname,
                    "mobile": c_mobile
                }
        return render_template('profile.html', data=c_data)
    return render_template('404.html')
#--------------End Of Customer Module---------------#

#-------------Logout Module--------------------

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Come back soon!", 'success')
    return redirect(url_for('index'))

#----------- Make Global user Instance -----------
@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


if __name__ == '__main__':
    app.run()
