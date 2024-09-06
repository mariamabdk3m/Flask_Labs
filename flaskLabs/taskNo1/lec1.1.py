from flask import Flask,redirect,url_for,render_template
app=Flask(__name__)
students = [{"id":1, "name":"Ahmed"}, {"id":2, "name":"Mohamed"}, {"id":3, "name":"Youssef"}]

@app.route("/home")
def home():
    return render_template("index.html", students_data=students)


@app.route("/search/<int:id>") 
def search(id):
    for student in students :
        if student["id"] == id:
            return render_template("search.html", student=student)
    else:
        return "No such student"



if  __name__ == '__main__':
    app.run(debug=True)


