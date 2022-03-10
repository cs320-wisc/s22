import flask, time

app = flask.Flask("my application")

# TEMPLATING
@app.route("/time.html")
def clock():
    with open("time.html") as f:
        html = f.read()
    # TODO: change html slightly
    print("DEBUG")
    html = html.replace("REPLACE_ME", str(time.time()))
    html += " TEST!"
    print(html)
    
    return html

# DYNAMIC
@app.route("/ha.html")
def laugh():
    html = "ha"*10
    return html

# STATIC
@app.route("/")
def home():
    with open("index.html") as f:
        html = f.read()
        
    #return html # return a string
    return flask.Response(html, status=200, headers={"A": "apple", "B": "banana"})

# Retry-After: 3600
# 429 status
@app.route("/goaway")
def goaway():
    return flask.Response("too many requests", status=429, headers={"Retry-After": "3"})

if __name__ == "__main__":
    print("BEFORE")
    app.run(host="0.0.0.0", debug=True, threaded=False)
    print("AFTER")

# app.run never returns, so don't define functions
# after this (the def lines will never be reached)
