from flask import Flask, redirect, render_template, request
from flask_mysqldb import MySQL
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
    curr=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curr.execute('SELECT * FROM users where Email=%s',(mailid,))
    data = curr.fetchall()
    print(data)
    
    if request.method == 'POST':
        if data!=():
            return render_template('login.html')
        else:
            print("cursoyruo",curr)
            curr.execute("INSERT INTO users VALUES(%s,%s)",(mailid,password))
            print("executed")
            mysql.connection.commit()
            curr.close()
            return render_template('main_page.html')
    
if __name__ == '__main__':
    app.run(debug=True)