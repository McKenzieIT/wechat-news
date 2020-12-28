from flask import Flask, redirect, url_for
app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'hello world'

@app.route('/hello/<string:name>')
def say_hello(name):
    return 'Hello {} !'.format(name)

@app.route('/guest/<string:guest_name>')
def hello_guest(guest_name):
    return 'Hello {} !'.format(guest_name)

@app.route('/admin/<string:admin_name>')
def hello_admin(admin_name):
    return 'Welcome {} !'.format(admin_name)

@app.route('/user/<string:user_type>/<string:user_name>')
def hello_user(user_type, user_name):
    if user_type=='admin':
        print(url_for('hello_admin', admin_name=user_name))
        return redirect(url_for('hello_admin', admin_name=user_name))
    else:
        return redirect(url_for('hello_guest', guest_name=user_name))

if __name__ == '__main__':
    app.run(debug=True)
