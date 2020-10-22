from flask import Flask, render_template, request
from flask import current_app

app = Flask(__name__)

if (app.config["ENV"] == "production"):
    app.config.from_object("config.ProductionConfig")
elif (app.config["ENV"] == "testing"):
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")