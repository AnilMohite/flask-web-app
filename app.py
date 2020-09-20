from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/services")
def services():
    return render_template('services.html')

@app.route("/service_detail")
def service_detail():
    return render_template('service_detail.html')

@app.route("/blogs")
def blogs():
    return render_template('blogs.html')

@app.route("/blog-detail")
def blog_detail():
    return render_template('blog_detail.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')


app.run(debug=True)