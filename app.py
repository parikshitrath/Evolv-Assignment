# first run this app so that the table with required rows and column is made 
from flask import Flask
from flask import request
from flask_restful import reqparse
import sqlite3


app = Flask(__name__)

@app.route('/')
def root():
    # Connect to db
    db = sqlite3.connect('user.db')  
    cursor = db.cursor()
    
    # Create Table user
    cursor.execute('CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT,author_name TEXT, blog_title TEXT , blog_content TEXT)')
    
    # Close db connection
    db.close()
    
    # Connect to db
    db = sqlite3.connect('comnt.db')
    cursor = db.cursor()

    # Create Table comment
    cursor.execute('CREATE TABLE comnt(id INTEGER PRIMARY KEY AUTOINCREMENT , blog_id INTEGER , comment TEXT)')

    # Close db connection
    db.close()

    return "Tables Created"

parser = reqparse.RequestParser()

@app.route('/add_blog' , methods=['POST'])
def add_blog():
    # Connect to db
    db = sqlite3.connect('user.db')
    cursor = db.cursor()

    # Get requested arguments
    author_name = request.args.get('author_name')
    blog_title = request.args.get('blog_title')
    blog_content = request.args.get('blog_content')

    # Using Parser to Return Data in Dictionary Form
    parser.add_argument("author_name")
    parser.add_argument("blog_title")
    parser.add_argument("blog_content")
    args = parser.parse_args()

    # Insert Data Into db
    cursor.execute('INSERT INTO user(author_name , blog_title , blog_content) VALUES("%s", "%s" , "%s")' % (author_name , blog_title , blog_content))
    db.commit()

    # Close db Connection
    db.close()

    return args

#By default methods=['GET']
@app.route('/display_blog' , methods=['GET'])
def display_blog():
    # Connect to db
    db = sqlite3.connect('user.db')
    cursor = db.cursor()

    # Get data from db
    cursor.execute('SELECT * FROM user')
    data = cursor.fetchall()

    # Close db connection
    db.close()

    return str(data)

#By default methods=['GET']
@app.route('/display_blog_by_id/<int:id>' , methods=['GET'])
def display_blog_by_id(id):
    # Connect to db
    db = sqlite3.connect('user.db')
    cursor = db.cursor()

    # Get data from db
    cursor.execute('SELECT * FROM user WHERE id = "%s"' %id)
    data = cursor.fetchall()

    # Close db connection
    db.close()

    return str(data)

@app.route('/update_blog/<int:id>' , methods=['PUT'])
def update_blog(id):
    # Connect to db
    db = sqlite3.connect('user.db')  
    cursor = db.cursor()
    
    # Get requested arguments
    author_name = request.args.get('author_name')
    blog_title = request.args.get('blog_title')
    blog_content = request.args.get('blog_content')

    # Using Parser to Return Data in Dictionary Form
    parser.add_argument("author_name")
    parser.add_argument("blog_title")
    parser.add_argument("blog_content")
    args = parser.parse_args()  
    
    # Update data in db
    cursor.execute('UPDATE user SET author_name="%s", blog_title="%s" , blog_content="%s" WHERE id=%s' % (author_name , blog_title , blog_content , id))
    db.commit()
    
    # Close db connection
    db.close()

    return args

@app.route('/delete_blog/<int:id>' , methods=['DELETE'])
def delete(id):
    # Connect to db
    db = sqlite3.connect('user.db')  
    cursor = db.cursor()
    
    # Update data in db
    cursor.execute('DELETE FROM user WHERE id = "%s" ' % id)
    db.commit()
    
    # Close db connection
    db.close()
    return 'Deleted Blog With id: %d' %id 

@app.route('/post_comment' , methods=['POST'])
def post_comment():
    # Connect to db
    db = sqlite3.connect('comnt.db')
    cursor = db.cursor()

    # Get requested arguments
    blog_id = request.args.get('blog_id')
    comment = request.args.get('comment')

    # Using Parser to Return Data in Dictionary Form
    # parser.add_argument("blog_id")
    # parser.add_argument("comment")
    # args = parser.parse_args()

    # Insert Data Into db
    cursor.execute('INSERT INTO comnt(blog_id , comment) VALUES("%s", "%s")' % (blog_id , comment))
    db.commit()

    # Close db Connection
    db.close()

    return " comment added to blog with id '%s' " %blog_id

@app.route('/get_comment/<int:id>' , methods=['GET'])
def get_comment(id):
    # Connect to db
    db = sqlite3.connect('comnt.db')
    cursor = db.cursor()

    # Get data from db
    cursor.execute('SELECT * FROM comnt WHERE blog_id = "%s" ' %id)
    data = cursor.fetchall()

    # Close db connection
    db.close()

    return str(data)



if __name__ == '__main__':
    app.run(debug=True)