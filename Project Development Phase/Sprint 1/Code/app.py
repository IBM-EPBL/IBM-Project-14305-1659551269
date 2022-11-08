from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=gmx70809;PWD=ogHRxZYkgsrkgHrK",'','')

app = Flask(__name__)
app.secret_key = 'SESSIONKEY'


@app.route("/",methods=['GET'])
def home():
  if 'email' not in session:
    return redirect(url_for('login'))
  return render_template('home.html',name='Home')

@app.route("/register",methods=['GET','POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    phno = request.form['phno']
    bloodGroup = request.form['blood_group']
    address = request.form['address'] or ''
    pincode = request.form['pincode']


    if not email or not username or not password or not phno or not bloodGroup or not pincode:
      return render_template('register.html',error='Please fill all fields')
    
    query = "SELECT * FROM USERS WHERE Email=?"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    
    if not isUser:
      insert_sql = "INSERT INTO Users(NAME,EMAIL,PASSWORD,PHONE,BLOOD_GROUP,ADDRESS,PINCODE) VALUES (?,?,?,?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, username)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, password)
      ibm_db.bind_param(prep_stmt, 4, phno)
      ibm_db.bind_param(prep_stmt, 5, bloodGroup)
      ibm_db.bind_param(prep_stmt, 6, address)
      ibm_db.bind_param(prep_stmt, 7, pincode)
      ibm_db.execute(prep_stmt)
      return render_template('register.html',success="You can login")
    else:
      return render_template('register.html',error='Invalid Credentials')

  return render_template('register.html',name='Home')

@app.route("/login",methods=['GET','POST'])
def login():
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']

    if not email or not password:
      return render_template('login.html',error='Please fill all fields')
    query = "SELECT * FROM USERS WHERE Email=?"
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    isUser = ibm_db.fetch_assoc(stmt)
    print(isUser,password)

    if not isUser:
      return render_template('login.html',error='Invalid Credentials')
      
    #if not isPasswordMatch:
    if(isUser['PASSWORD']!=password):
      return render_template('login.html',error='Invalid Credentials')

    session['email'] = isUser['EMAIL']
    return redirect(url_for('home'))

  return render_template('login.html',name='Home')

if __name__ == "__main__":
  app.run()