from flask import Flask
print("I'm going to use port 55555")
application = Flask(__name__)
application.run("0.0.0.0", 55555)
