import flask
import matplotlib.pyplot as plt
import pandas as pd
# fake text and byte files, respectively
from io import StringIO, BytesIO

app = flask.Flask("lecture 2 example")

@app.route("/")
def home():
    return """
    <html><body bgcolor="lightblue">
    <h3>Dashboard</h3>
    <h4>Cumulative Distribution Function (SVG)</h4>
    <img src="plot2.svg">
    <h4>Histogram (PNG)</h4>
    <img src="plot1.png">
    </body></body>
    """

temps = [70,75,74,72]

@app.route("/upload", methods=["POST"])
def upload():
    #print(flask.request.args) # query str
    post_data = flask.request.get_data()
    post_str = str(post_data, "utf-8")
    post_nums = post_str.split(",")
    print(post_nums)
    for num in post_nums:
        temps.append(float(num))
    return f"you now have {len(temps)} of measurements\n"



# histogram
@app.route("/plot1.png")
def gen_png():
    fig, ax = plt.subplots(figsize=(3,2))
    
    pd.Series(temps).hist(ax=ax, bins=100)
    ax.set_ylabel("Temps")
    
    f = BytesIO() # fake file (has a .write method)
    plt.tight_layout()
    fig.savefig(f)
    plt.close() # closes the most recent fig
    
    png = f.getvalue()
    
    hdr = {"Content-Type": "image/png"}
    return flask.Response(png, headers=hdr)

# CDF (cumulative distribution function)
@app.route("/plot2.svg")
def gen_svg():
    fig, ax = plt.subplots(figsize=(3,2))
    
    s = pd.Series(sorted(temps))
    rev = pd.Series(100*(s.index+1)/len(s), index=s.values)
    rev.plot.line(ax=ax, ylim=(0,100), drawstyle="steps-post")
    ax.set_xlabel("Temperature")
    ax.set_ylabel("% Obs Less Than")
    
    f = StringIO() # fake file (has a .write method)
    plt.tight_layout()
    fig.savefig(f, format="svg")
    plt.close() # closes the most recent fig
    
    png = f.getvalue()
    
    hdr = {"Content-Type": "image/svg+xml"}
    return flask.Response(png, headers=hdr)

app.run("0.0.0.0", debug=True, threaded=False)