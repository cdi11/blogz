from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:lc101blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    writer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
    def __init__(self, title, body, writer):
        self.title = title
        self.body = body
        self.writer = writer

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, email, password, blogs):
        self.email= email
        self.password= password



   

    def __repr__(self):
        return '<Title %r>' % self.title
        return '<Body %r>' % self.body


        def get_curent_titles():
            return Title.query.all()

        def get_current_blogs():
            return Body.query.all()

   
@app.route('/')
def index():
       
    #blogs = Blog.query.all()
        #new_blog = Blog(title, body)
        
         #new_body = Blog(body)
        #db.session.add(new_blog)
        #db.session.commit()  
           
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)
    
    
    

@app.route('/post', methods=['POST', 'GET'])
def display_post():
    if request.method == 'GET':
        #blog_id = int(request.form['id']
        blog_id = (request.args.get('id'))
        blog = Blog.query.filter_by(id=blog_id).first()
        if blog_id:
            return render_template('post.html', blog=blog)



    
@app.route("/addpost", methods=['POST', 'GET'])
def add_post():
    if request.method=='POST':
        title=request.form['title']
        body=request.form['body'] 
        

    return render_template('addpost.html')
  

@app.route("/newpost", methods=['POST', 'GET'])
def new_post():
    title_error =""
    body_error = ""
    if request.method == "POST":
        title =request.form['title']
        body = request.form['body']
        if (title == ""):
            title_error = "Please enter title"
            return render_template("addpost.html", title_error=title_error)
        if (body == ""):
            body_error = "Please enter body"
            return render_template("addpost.html", body_error=body_error)
        
        else:
            
            new_blog = Blog(title, body)
        
            #new_body = Blog(body)
            db.session.add(new_blog)
            db.session.commit()  
            return render_template('newpost.html', title=title, body=body)
    
    return render_template('addpost.html')



    

if __name__ == '__main__':
    app.run()