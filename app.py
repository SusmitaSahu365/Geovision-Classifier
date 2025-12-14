from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors
import os
import numpy as np
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session management

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'space_users'

mysql = MySQL(app)

# Main page route (renamed from homepage)
@app.route("/")
def main():
    return render_template("main.html")

# Sign Up route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template("signup.html", error_message="Passwords do not match")

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        cursor = mysql.connection.cursor()
        try:
            cursor.execute('INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)',
                           (name, email, username, hashed_password))
            mysql.connection.commit()
            return render_template("main.html", success_message=f"User registered successfully")
        except Exception as e:
            return render_template("signup.html", error_message=f"Database Error: {e}")
        finally:
            cursor.close()

        

    return render_template("signup.html")

# Sign In route
@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            session['name'] = user['name']
            session['email'] = user['email']  # Add email to session
            return redirect(url_for("profile"))

        return render_template("signin.html", error_message="Incorrect username or password")

    return render_template("signin.html")

@app.route("/profile")
def profile():
    if 'username' not in session:
        return redirect(url_for('signin'))  # If the user isn't logged in, redirect to signin page

    username = session['username']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT name, email, username FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return render_template("profile.html", name=user[0], email=user[1], username=user[2])
    else:
        return "User not found", 404

# Logout route
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('main'))

# Load the trained model
model = load_model("Modelmain.h5")

# Define the class names
class_names = ['Cloudy', 'Desert', 'Green_Area', 'Water']

# Folder to save uploaded images
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route for the homepage (with sign-in/sign-out)
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

# Route to handle image upload and prediction
@app.route('/uploads', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename).replace("\\", "/")
        file.save(file_path)
        
        # Load and preprocess the image
        img = load_img(file_path, target_size=(255, 255))
        img_array = img_to_array(img) / 255.0
        img_array = np.reshape(img_array, (1, 255, 255, 3))

        # Get the model predictions
        predictions = model.predict(img_array)

        # Get the class index with the highest predicted probability
        class_index = np.argmax(predictions[0])

        # Get the predicted class label
        predicted_label = class_names[class_index]

        # Fetch the user's ID from the 'users' table using a dictionary cursor
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
        user = cursor.fetchone()

        if user:
            user_id = user['id']  # This will now work since 'user' is a dictionary

            # Insert the prediction into the 'predictions' table
            cursor.execute('INSERT INTO predictions (user_id, image_path, predicted_class) VALUES (%s, %s, %s)',
                           (user_id, file_path, predicted_label))
            mysql.connection.commit()

            # Return the response with prediction data
            return jsonify({
                'success': True,
                'path': file_path,
                'prediction': predicted_label
            })
        else:
            return jsonify({'success': False, 'error': 'User not found'})

    else:
        return jsonify({'success': False, 'error': 'Invalid file format'})

@app.route("/history")
def history():
    if 'username' not in session:
        return redirect(url_for('signin'))  # If the user isn't logged in, redirect to signin page

    username = session['username']

    # Fetch the user ID using the logged-in user's username
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        user_id = user['id']  # Get the user ID

        # Fetch predictions for this user
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM predictions WHERE user_id = %s", (user_id,))
        predictions = cursor.fetchall()
        cursor.close()

        if predictions:
            return render_template("history.html", predictions=predictions)
        else:
            return render_template("history.html", message="No history found.")
    else:
        return render_template("history.html", message="User not found.")



if __name__ == "__main__":
    app.run(debug=True)
