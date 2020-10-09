from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_mail import Mail
import json
import os
from werkzeug.utils import secure_filename
from datetime import datetime
now = datetime.now()
cdatetime = now.strftime('%Y-%m-%d %H:%M:%S')

#include config.json 
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.secret_key = params['secret-key']

# for file upload 
app.config['UPLOAD_FOLDER'] = params['UPLOAD_FOLDER']
ALLOWED_EXTENSIONS = params['ALLOWED_EXTENSIONS']
def allowed_file(filename):
    return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# mail config 
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)
mail = Mail(app)
# db config 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'alm'

mysql = MySQL(app)

# ================== app route ======================
# fontend route 
@app.route("/")
def home():
    return render_template('index.html', params=params)

@app.route("/about")
def about():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM about WHERE id=%s AND status=%s",(1,1))
    data = cur.fetchall()
    return render_template('about.html',params=params,data=data[0])

@app.route("/services")
def services():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM services WHERE status=%s order by id desc",(1,))
    data = cur.fetchall()
    return render_template('services.html',params=params,data=data)

@app.route("/services/<string:url>")
def service_detail(url):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM services WHERE status=%s AND slug_url=%s",(1,url))
    data = cur.fetchone()
    return render_template('service_detail.html',params=params,data=data)

@app.route("/blogs")
def blogs():
    return render_template('blogs.html',params=params)

@app.route("/blog-detail")
def blog_detail():
    return render_template('blog_detail.html',params=params)

@app.route("/contact", methods=['GET','POST'])
def contact():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contacts(name, email,message) VALUES (%s, %s, %s)", (name, email, message))
        mysql.connection.commit()
        cur.close()
        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients = [params['gmail-user']],
                          body = message 
                          )
        flash('Thank you for contact us... ','success')
        return redirect(url_for('contact'))
    else:
        error='failed.'
    return render_template('contact.html',error=error,params=params)

# ============ Dashboard Backend  ==========================

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    msg=''

    if 'loggedin' in session:
          return render_template('dashboard.html',params=params,username=session['user'])

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT username, password FROM users WHERE username=%s AND password=%s AND status=%s",(username,password,1))
        data = cur.fetchone()
        if data:
            session['loggedin'] = True
            session['id'] = data[0]
            session['user'] = data[1]
            return render_template('dashboard.html',params=params,username=session['user'])
        else:
            msg = 'Incorrect Username/Passwrod!'


    return render_template('login.html',params=params,msg=msg)

@app.route('/dashboard/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('user', None)
   # Redirect to login page
   return redirect(url_for('dashboard'))

# ============ Dashboard About  ==========================

@app.route('/dashboard-about')
def dashboard_about():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM about WHERE id=%s AND status=%s",(1,1))
        data = cur.fetchall()
        flash('Data Update Successfully... ','success')
        # data = data.json_encoder()
        if data:
            return render_template('dashboard-about.html',params=params,username=session['user'],data=data[0])
    return render_template('login.html',params=params)

@app.route('/dashboard-about-edit/<string:id>',methods=['GET','POST'])
def dashboard_about_edit(id):
    if 'loggedin' in session:  
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM about WHERE id=%s AND status=%s",(1,1))            
        data = cur.fetchall()
        if id and request.method == 'POST':
            title = request.form['title']
            head = request.form['head']
            body = request.form['body']
            file_old = request.form['file_old']
           
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
           
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                file_name = file_old
             
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_old))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_name = filename

            cur.execute("UPDATE about SET title=%s,head=%s,body=%s,file=%s WHERE id=%s",(title,head,body,file_name,id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('dashboard_about'))
            
        return render_template('dashboard-about-edit.html',params=params,username=session['user'],id=id,data=data[0])
    return render_template('login.html',params=params)

# ============ Dashboard Services  ==========================

@app.route('/dashboard-services')
def dashboard_services():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM services WHERE status=%s",(1,))            
        data = cur.fetchall()
        return render_template('dashboard-services.html',params=params,username=session['user'],data=data)
    return render_template('login.html',params=params)

@app.route('/dashboard-services/add', methods=['GET','POST'])
def dashboard_services_add():
    if 'loggedin' in session:
        if request.method == 'POST':
            title = request.form['title']
            head = request.form['head']
            body = request.form['body']
            slug_url = title.strip().replace(' ', '-').lower()
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part','warning')
                return redirect(request.url)
           
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file','warning')
                return redirect(request.url)
             
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO services(title, slug_url,head,body,image,status) VALUES (%s, %s, %s, %s, %s, %s)", (title, slug_url, head, body,filename,1))     
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('dashboard_services'))

        return render_template('dashboard-service-add.html',params=params,username=session['user'])
    return render_template('login.html',params=params)


@app.route('/dashboard-services/edit/<string:id>', methods=['GET','POST'])
def dashboard_services_edit(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM services WHERE id=%s AND status=%s",(id,1))     
        data = cur.fetchall()
        if request.method == 'POST':
            title = request.form['title']
            head = request.form['head']
            body = request.form['body']
            file_old = request.form['file_old']
            slug_url = title.strip().replace(' ', '-').lower()
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
           
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                file_name = file_old

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_old))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))            
                file_name = filename

            cur.execute("UPDATE services SET title=%s,slug_url=%s,head=%s,body=%s,image=%s,status=%s WHERE id=%s",(title,slug_url,head,body,file_name,1,id)) 
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('dashboard_services'))

        return render_template('dashboard-service-edit.html',params=params,username=session['user'],data=data[0])
    return render_template('login.html',params=params)


@app.route('/dashboard-services/delete/<string:id>')
def dashboard_services_del(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM services WHERE id=%s",(id))        
        data = cur.fetchall()
        del_file = data[0][5]
        if del_file !='':
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], del_file))
            
        cur.execute("DELETE FROM services WHERE id =%s",(id))    
        mysql.connection.commit()
        cur.execute("SELECT * FROM services order by id desc")        
        data = cur.fetchall()
        cur.close()
        return render_template('dashboard-services.html',params=params,username=session['user'],data=data)
    return render_template('login.html',params=params)

# ============ Dashboard Blogs  ==========================

@app.route('/dashboard-blogs',methods=['GET','POST'])
def dashboard_blogs():
    if 'loggedin' in session:
        return render_template('dashboard-blogs.html',params=params,username=session['user'])
    return render_template('login.html',params=params)

# ============ Dashboard Contacts  ==========================

@app.route('/dashboard-contacts')
def dashboard_contacts():
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM contacts order by id desc")            
        data = cur.fetchall()
       
        return render_template('dashboard-contacts.html',params=params,username=session['user'],data=data)
    return render_template('login.html',params=params)

@app.route('/dashboard-contacts/<string:id>')
def dashboard_contacts_del(id):
    if 'loggedin' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM contacts WHERE id =%s",(id))    
        mysql.connection.commit()
        cur.execute("SELECT * FROM contacts order by id desc")        
        data = cur.fetchall()
        cur.close()
        return render_template('dashboard-contacts.html',params=params,username=session['user'],data=data)
    return render_template('login.html',params=params)

app.run(debug=True)