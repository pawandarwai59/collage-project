from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------
# Database Model
# -----------------------
class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Create table
with app.app_context():
    db.create_all()

# -----------------------
# Routes
# -----------------------

# Frontend page
@app.route('/')
def home():
    return render_template("index.html")

# API for form submit
@app.route('/contact', methods=['POST'])
def save_contact():
    try:
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not name or not email or not message:
            return jsonify({"message": "All fields are required"}), 400

        new_msg = ContactMessage(
            name=name,
            email=email,
            message=message
        )

        db.session.add(new_msg)
        db.session.commit()

        return jsonify({"message": "Form submitted successfully!"}), 200

    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}"}), 500


# -----------------------
# Run App
# -----------------------
if __name__ == '__main__':
    app.run(debug=True)