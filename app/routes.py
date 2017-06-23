from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template('dashboard.html')


@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

if __name__ == '__main__':
    app.run(debug=True)


# def connection():
#     conn = MySQLdb.connect(host="127.0.0.1:5000",
#                            user="testuser",
#                            passwd="123",
#                            db="TESTDB")
#     c = conn.cursor()

