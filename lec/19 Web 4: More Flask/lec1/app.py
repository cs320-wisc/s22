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
    return flask.Response(html, status=200,
                          headers={"A": "apple",
                                   "B": "banana"})

last_visit_time = 0

# Retry-After: 3600
# 429 status
@app.route("/goaway")
def goaway():
    global last_visit_time
    # TODO: have a dict of last visit times for each user
    print(flask.request.remote_addr)
    
    if time.time() - last_visit_time < 3:
        return flask.Response("too many requests", status=429,
                              headers={"Retry-After": "3"})
    else:
        last_visit_time = time.time()
        return "welcome"

@app.route("/robots.txt")
def robo():
    s = "\n".join(["User-agent: *",
                   "Disallow: /ha.html"])
    return flask.Response(s, headers={"Content-Type": "text/plain"})

@app.route("/add")
def adder():
    args = dict(flask.request.args)
    print(args["a"], args["b"])
    total = int(args["a"]) + int(args["b"])
    return f"{args['a']} + {args['b']} = {total}"

major_counts = {}

@app.route("/survey.html")
def survey():
    major = flask.request.args.get("major", "unknown")
    major_counts[major] = major_counts.get(major, 0) + 1
    return str(major_counts)

if __name__ == "__main__":
    print("BEFORE")
    app.run(host="0.0.0.0", debug=True, threaded=True)
    print("AFTER")

# app.run never returns, so don't define functions
# after this (the def lines will never be reached)
