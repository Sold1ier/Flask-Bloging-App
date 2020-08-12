from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db' # database config
db = SQLAlchemy(app)
# database design
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return 'Blog Post ' + str(self.id)

all_posts = [
    {
        'title': 'Post 1',
        'content': 'Content of post 1',
        "author": "Guy Levitzky"
    },
    {
        'title': 'Post 2',
        'content': 'Content of post 2'
    }
]


@app.route('/')
def home():
    return render_template("index.html")

@app.route("/posts")
def posts():   
    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template("posts.html", posts=all_posts)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
       
    
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
                
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


@app.route("/about")
def about():
    return render_template('about.html')

@app.route('/posts/new' ,methods=['GET', 'POST'])
def new_post():
        if request.method == 'POST':                
            post_title = request.form['title']
            post_content = request.form['content']
            post_author = request.form['author']
            new_post = BlogPost(title=post_title, content=post_content, author=post_author)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/posts')
        else:
            return render_template('new_post.html')







if __name__ == "__main__":
    app.run(debug=True)