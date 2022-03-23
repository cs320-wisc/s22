import flask, time

app = flask.Flask("my application")

# TEMPLATED
@app.route("/now.html")
def get_time():
    with open("now.html") as f:
        html = f.read()
    html = html.replace("????", str(time.time()))
    print("DEBUG")
    print(html)
    html += " TEST!"
        
    return html

# DYNAMIC
@app.route("/laugh.html")
def haha():
    html = "ha" * 10
    return html

# STATIC
@app.route("/")
def home():
    with open("index.html") as f:
        html = f.read()
        
    #return html   # return a string
    return flask.Response(html, status=200,
                          headers={"A": "apple", "B": "banana"})

last_visit = 0

@app.route("/goaway.html")
def goaway():
    global last_visit
    
    # TODO: limit on a per-person basis
    print(flask.request.remote_addr)
    
    if time.time() - last_visit > 3:
        last_visit = time.time()
        return "welcome!"
    else:
        html = "too many requests, come back later"
        return flask.Response(html, status=429,
           headers={"Retry-After": 3}                   )
    
@app.route("/robots.txt")
def robo():
    s = "\n".join(["User-Agent: *",
                   "Disallow: /laugh.html"])
    return flask.Response(s, headers={"Content-Type": "text/plain"})

@app.route("/add")
def adder():
    args = dict(flask.request.args)
    print(args)
    total = int(args["a"]) + int(args["b"])
    return f"{args['a']} + {args['b']} = {total}"

major_counts = {}

# http://104.154.131.51:5000/survey?major=DS
@app.route("/survey")
def survey():    
    args = dict(flask.request.args)
    major = args.get("major", "unknown")
    major_counts[major] = major_counts.get(major, 0) + 1 
    return str(major_counts)

if __name__ == "__main__":
    print("BEFORE")
    app.run(host="0.0.0.0", debug=True, threaded=True)
    print("THIS NEVER RUNS")
    
# app.run never returns, so don't define functions
# after this (the def lines will never be reached)
