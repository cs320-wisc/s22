from flask import Flask, request

my320app = Flask("example-server")

donate_visits = 0
def count_donate():
    donate_visits += 1
    print("VISITER", donate_visits)

@my320app.route("/")
def home():
    with open("index.html") as f:
        html = f.read()
    html = html.replace("XYZ", str(donate_visits))
    return html

@my320app.route("/donate.html")
def donate():
    count_donate()
    return """<html><body style="background-color:lightblue">
              <h1>Donations</h1>
              Please make one!
              <body></html>"""

if __name__ == '__main__':
    my320app.run("0.0.0.0", "5000", debug=True, threaded=False)
