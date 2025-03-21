from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# My App
app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# Creates a new DB for each user
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)

# Data class that stores a row of data
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"Task {self.id}"


with app.app_context():
    db.create_all()

# Routes to Webpages
# Home page
@app.route('/', methods=["POST", "GET"])
def index():
    # Add a task
    # Once we click submit, whatever is in the content payload gets stored in the database
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    # See all current tasks
    else: # if we haven't clicked submit, we show all the current tasks in our database
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.jinja", tasks=tasks)
    

# Delete an Item
@app.route("/delete/<int:id>")
def delete(id:int):
    # Go the database and get the task with the given id, delete it, commit changes, then send us back to our home page
    delete_task = MyTask.query.get_or_404(id) # Getting a task by its ID
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Error: {e}"

# Edit an item
@app.route("/update/<int:id>",  methods=["POST", "GET"])
def edit(id:int):
    # What happens within the edit page, essentially, once we click edit, whatever is in content payload gets stored inside the database and then we get redirected to the home page
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"Error: {e}"
    else:
        return render_template('edit.jinja', task=task)



# Runner and Debugger
if __name__ == "__main__":
    app.run(debug=True)