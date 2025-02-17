from flask import Flask
from login import auth_bp, setup_database

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

# Register the authentication blueprint from login.py
app.register_blueprint(auth_bp)

# Set up the login database on startup
setup_database()

if __name__ == "__main__":
    app.run(debug=True)
