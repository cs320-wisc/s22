import flask
import matplotlib.pyplot as plt
import pandas as pd
# fake text and binary files, respectively
from io import StringIO, BytesIO

app = flask.Flask("my lecture example")

@app.route("/")
def home():
    return """
    <html><body bgcolor="lightblue">
    <h3>Dashboard</h3>
    <h5>Cumulative Distribution Function (SVG)</h5>
    <img src="plot2.svg">
    <h5>Histogram (PNG)</h5>
    <img src="plot1.png">
    </body></html>
    """

temps = [70,73,75,68]

# box+whiskers
# histogram
# CDF

@app.route("/upload", methods=["POST"])
def upload():
    #print(flask.request.args) # for query str
    post_data = str(flask.request.get_data(), "utf-8")
    nums = post_data.split(",")
    print(nums)
    for num in nums:
        temps.append(float(num))
    return f"you now have {len(temps)} temps\n"

@app.route("/plot1.png")
def gen_png():
    fig, ax = plt.subplots(figsize=(3,2))
    pd.Series(temps).hist(ax=ax, bins=100)
    ax.set_ylabel("Temp")
    plt.tight_layout()
    f = BytesIO() # fake file (has a .write)
    fig.savefig(f)
    plt.close() # closes the most recent fig
    png = f.getvalue()
    hdr = {"Content-Type": "image/png"}
    return flask.Response(png, headers=hdr)

@app.route("/plot2.svg")
def gen_svg():
    fig, ax = plt.subplots(figsize=(3,2))
    
    s = pd.Series(sorted(temps))
    rev = pd.Series(100*(s.index+1)/len(s), index=s.values)
    rev.plot.line(ax=ax, ylim=(0,100), drawstyle="steps-post")
    ax.set_xlabel("Temp")
    ax.set_ylabel("% of Temp <")
    
    plt.tight_layout()
    f = StringIO() # fake file (has a .write)
    fig.savefig(f, format="svg")
    plt.close() # closes the most recent fig
    png = f.getvalue()
    hdr = {"Content-Type": "image/svg+xml"}
    return flask.Response(png, headers=hdr)
                  
app.run("0.0.0.0", debug=True, threaded=False)