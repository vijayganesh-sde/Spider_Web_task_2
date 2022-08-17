from flask import Flask, redirect, render_template, request
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash,check_password_hash
import MySQLdb.cursors
app=Flask(__name__,template_folder='templates')
app.config['MYSQL_HOST'] = 'Localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'diary_notes'
mysql = MySQL(app)

@app.route('/')
def insert():
    return render_template('index.html')
@app.route('/register',methods=['POST','GET'])
def register():
    return render_template('register.html')
@app.route('/login',methods=['POST','GET'])
def login():
    return render_template('login.html')
@app.route('/dashboard',methods=['POST','GET'])
def dashboard():
    result=request.form
    mailid=result['email']
    password=result['pass']
    pas_hash=generate_password_hash(password)
    print(check_password_hash(pas_hash,"pbkdf2:sha256:260000$kdyEn9J7Q6DHUBy0$0439e33cfea4102dbe09e517892bb20d6b527d913759f7785ac45f6443e7da22"))
    print(pas_hash)
    curr=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curr.execute('SELECT * FROM users where Email=%s',(mailid,))
    data = curr.fetchall()
    print(data)
    
    if request.method == 'POST':
        if data!=():
            return render_template('login.html')
        else:
            curr.execute("INSERT INTO users VALUES(%s,%s)",(mailid,pas_hash))
            print("executed")
            mysql.connection.commit()
            curr.close()
            return render_template('main_page.html')
@app.route('/log_sub',methods=['POST','GET'])
def log_entry():
    result=request.form
    mailid=result['email']
    password=result['pass']
    curr=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curr.execute('SELECT * FROM users where Email=%s',(mailid,))
    data = curr.fetchall()
    print(data)
    if (data==()):
        return render_template('register.html')
    else:
        if check_password_hash(password,data[0]['password']):
            return render_template('main_page.html')
        return render_template('login.html')
if __name__ == '__main__':
    app.run(debug=True)