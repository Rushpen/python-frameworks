from flask import Flask, render_template

app = Flask(__name__)  # Используйте __name__ вместо name

@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
