from flask import Flask, render_template, session, request, redirect, flash
from flask_app import app
from flask_app.controllers import users_controller

if __name__ == "__main__":
    app.run(debug=True)