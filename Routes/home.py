from flask import Blueprint, render_template, request, url_for, redirect, flash, jsonify
from flask import current_app

homeviews = Blueprint('homeviews', __name__)

@homeviews.route('/', methods=['GET', 'POST'])
def home():
    
    current_app.mongodb_repository.create_user(username="john_doe", password="password123", email="john@example.com")

    return render_template("home.html")

