from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:lc101blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zp3B'

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
    blogs = db.relationship('Blog', backref='writer')

    def __init__(self, email, password):
        self.email= email
        self.password= password



   
@app.route('/')
def index():     
    users = User.query.all()
    return render_template('index.html', users=users)
    
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'display_blogs', 'index', 'display_post', 'display_user']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect ('/login')


 
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("logged in")
            return redirect ('/addpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')
    return render_template('login.html')
 
 
@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        if not is_email(email):
            flash(email + 'does not seem like an email address')
            return redirect('/signup')
        email_db_count = User.query.filter_by(email=email).count()
        if email_db_count > 0:
            flash(email + 'is already taken please click login.')
            return redirect('/signup')
        if len(email) < 3:
            flash('try a differnt username')
            return redirect('/signup')
        if len(password) < 3:
            flash('try a different password')
            return redirect('/signup')
        if password != verify:
            flash('passwords did not match')
            return redirect('/signup')
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.email
        return redirect("/")
        
          
    
    else:
        
        return render_template('signup.html')

def is_email(string):

    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present
    

    #return render_template('signup.html')   


@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')   



@app.route('/post', methods=['POST', 'GET'])
def display_post():
    if request.method == 'GET':
        #blog_id = int(request.form['id']
        blog_id = (request.args.get('id'))
        blog = Blog.query.filter_by(id=blog_id).first()
        user_id= (request.args.get('id'))
        user= User.query.filter_by(id=user_id) 
        
        if blog_id:
            return render_template('post.html', blog=blog, user=user)



@app.route('/blog', methods=['POST', 'GET'])
def display_blogs():
       
    
    blogs = Blog.query.all()
    user_id = (request.args.get('id'))
    writer_id=(request.args.get('writer_id'))
    user = User.query.filter_by(id=writer_id)
    return render_template('blog.html', blogs=blogs, user=user)




@app.route('/singleuser', methods=['POST', 'GET'])
def display_user():
    if request.method == 'GET':
        user_id = (request.args.get('id'))
        user = User.query.filter_by(id=user_id).first()
        blogs = Blog.query.filter_by(writer_id=user_id)
        
        if user:
            return render_template('singleuser.html', user=user, blogs=blogs)

    #return render_template('singleuser.html', user=user)


    
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
        writer = User.query.filter_by(email=session['email']).first()
        if (title == ""):
            title_error = "Please enter title"
            return render_template("addpost.html", title_error=title_error)
        if (body == ""):
            body_error = "Please enter body"
            return render_template("addpost.html", body_error=body_error)
        
        else:
            
            new_blog = Blog(title, body, writer)
        
            #new_body = Blog(body)
            db.session.add(new_blog)
            db.session.commit()  
            return render_template('newpost.html', title=title, body=body)
    
    return render_template('addpost.html')



    

if __name__ == '__main__':
    app.run()