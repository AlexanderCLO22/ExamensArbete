from flask import Blueprint, render_template, request, flash, jsonify

homeviews = Blueprint('homeviews', __name__)

@homeviews.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")