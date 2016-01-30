from flask import Flask
app = Flask(__name__)

@app.route("/text.txt")
def text():
    return app.send_static_file('text.txt')


@app.route("/vote.txt")
def vote():
    return app.send_static_file('vote.txt')

if __name__ == "__main__":
    app.run()
