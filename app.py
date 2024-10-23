from flask import Flask, request, render_template, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads/pet_images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  
db = SQLAlchemy(app)
app.secret_key = 'secret_key'


# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


# LostPet Model
class LostPet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_name = db.Column(db.String(100), nullable=False)
    pet_type = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100))
    color_markings = db.Column(db.String(100))
    size_weight = db.Column(db.String(100))
    age = db.Column(db.String(50))
    gender = db.Column(db.String(10))
    distinguishing_features = db.Column(db.Text)
    last_seen = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    images = db.Column(db.String(255))  

    def __init__(self, pet_name, pet_type, breed, color_markings, size_weight, age, gender,
                 distinguishing_features, last_seen, description, contact_info, images):
        self.pet_name = pet_name
        self.pet_type = pet_type
        self.breed = breed
        self.color_markings = color_markings
        self.size_weight = size_weight
        self.age = age
        self.gender = gender
        self.distinguishing_features = distinguishing_features
        self.last_seen = last_seen
        self.description = description
        self.contact_info = contact_info
        self.images = images

class FoundPet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    founder_name = db.Column(db.String(100), nullable=False)
    founder_phone = db.Column(db.String(100), nullable=False)
    pet_type = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100))
    gender = db.Column(db.String(50))
    location_found = db.Column(db.String(255), nullable=False)
    additional_info = db.Column(db.Text)
    images = db.Column(db.Text)  

    def __init__(self, founder_name, founder_phone, pet_type, breed, gender, location_found, additional_info, images):
        self.founder_name = founder_name
        self.founder_phone = founder_phone
        self.pet_type = pet_type
        self.breed = breed
        self.gender = gender
        self.location_found = location_found
        self.additional_info = additional_info
        self.images = images


with app.app_context():
    db.create_all()


@app.route('/')
def index():
   return render_template('register.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid user')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html', user=user)

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/report_lost', methods=['GET', 'POST'])
def report_lost():
    if request.method == 'POST':
        pet_name = request.form['pet-name']
        pet_type = request.form['pet-type']
        breed = request.form['breed']
        color_markings = request.form['color-markings']
        size_weight = request.form['size-weight']
        age = request.form['age']
        gender = request.form['gender']
        distinguishing_features = request.form['distinguishing-features']
        last_seen = request.form['last-seen']
        description = request.form['description']
        contact_info = request.form['contact']

        uploaded_images = []
        if 'pet-image' in request.files:
            files = request.files.getlist('pet-image')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join('static/uploads/lost_pets', filename))
                    uploaded_images.append(filename)

        image_filenames = ','.join(uploaded_images)

        lost_pet = LostPet(pet_name=pet_name, pet_type=pet_type, breed=breed,
                           color_markings=color_markings, size_weight=size_weight, age=age, gender=gender,
                           distinguishing_features=distinguishing_features, last_seen=last_seen,
                           description=description, contact_info=contact_info, images=image_filenames)
        db.session.add(lost_pet)
        db.session.commit()

        flash('Lost pet report submitted successfully!')
        return redirect(url_for('dashboard'))
    
    return render_template('report_lost.html')



@app.route('/found_pets', methods=['GET', 'POST'])
def found_pets():
    if request.method == 'POST':

        founder_name = request.form['founder-name']
        founder_phone = request.form['founder-phone']
        pet_type = request.form['pet-type']
        breed = request.form['breed']
        gender = request.form['gender']
        location_found = request.form['location-found']
        additional_info = request.form['additional-info']

        uploaded_images = []
        if 'pet-image' in request.files:
            files = request.files.getlist('pet-image')
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join('static/uploads/found_pets', filename))
                    uploaded_images.append(filename)

        image_filenames = ','.join(uploaded_images)

        found_pet = FoundPet(founder_name=founder_name, founder_phone=founder_phone, pet_type=pet_type,
                             breed=breed, gender=gender, location_found=location_found,
                             additional_info=additional_info, images=image_filenames)
        db.session.add(found_pet)
        db.session.commit()

        flash('Found pet report submitted successfully!')
        return redirect(url_for('dashboard'))

    return render_template('found_pets.html')

if __name__ == '__main__':
    app.run(debug=True)
