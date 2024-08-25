from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tomyvet.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Create directories for file uploads if not exists
os.makedirs(os.path.join(app.instance_path, 'uploads'), exist_ok=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    owner_address = db.Column(db.String(200), nullable=False)
    owner_phone = db.Column(db.String(50), nullable=False)
    animal_type = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    medical_history = db.Column(db.Text, nullable=True)
    species = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    comuna = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(100), nullable=True)

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(200), nullable=False)

class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Please log in to post a story.')
            return redirect(url_for('login'))
        
        title = request.form['title']
        content = request.form['content']
        author = current_user.username
        new_story = Story(title=title, content=content, author=author)
        db.session.add(new_story)
        db.session.commit()
        return redirect(url_for('home'))
    
    stories = Story.query.order_by(Story.date_posted.desc()).all()
    return render_template('home.html', stories=stories)

@app.route('/delete_story/<int:story_id>', methods=['POST'])
@login_required
def delete_story(story_id):
    story = Story.query.get(story_id)
    if story and story.author == current_user.username:
        db.session.delete(story)
        db.session.commit()
        flash('Historia eliminada con éxito.')
    else:
        flash('No tienes permiso para eliminar esta historia.')
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/manage_animals')
@login_required
def manage_animals():
    animals = Animal.query.all()
    return render_template('manage_animals.html', animals=animals)

@app.route('/add_animal', methods=['GET', 'POST'])
@login_required
def add_animal():
    if request.method == 'POST':
        name = request.form['name']
        owner_name = request.form['owner_name']
        owner_address = request.form['owner_address']
        owner_phone = request.form['owner_phone']
        animal_type = request.form['animal_type']
        breed = request.form['breed']
        age = request.form['age']
        medical_history = request.form['medical_history']
        species = request.form['species']
        country = request.form['country']
        region = request.form['region']
        comuna = request.form['comuna']
        image = request.files['image']

        if image:
            image_path = os.path.join(app.instance_path, 'uploads', image.filename)
            image.save(image_path)
            image_path = image.filename  # Store only the filename in the database
        else:
            image_path = None

        new_animal = Animal(name=name, owner_name=owner_name, owner_address=owner_address, owner_phone=owner_phone,
                            animal_type=animal_type, breed=breed, age=age, medical_history=medical_history,
                            species=species, country=country, region=region, comuna=comuna, image_path=image_path)
        db.session.add(new_animal)
        db.session.commit()
        return redirect(url_for('manage_animals'))
    return render_template('add_animal.html')

@app.route('/delete_animal/<int:id>', methods=['POST'])
@login_required
def delete_animal(id):
    animal = Animal.query.get(id)
    db.session.delete(animal)
    db.session.commit()
    return redirect(url_for('manage_animals'))

@app.route('/inventory')
@login_required
def inventory():
    items = InventoryItem.query.all()
    return render_template('inventory.html', inventory=items)

@app.route('/add_inventory', methods=['GET', 'POST'])
@login_required
def add_inventory():
    if request.method == 'POST':
        medicine_name = request.form['medicine_name']
        quantity = request.form['quantity']
        price = request.form['price']
        new_item = InventoryItem(medicine_name=medicine_name, quantity=quantity, price=price)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('inventory'))
    return render_template('add_inventory.html')

@app.route('/delete_inventory/<int:id>', methods=['POST'])
@login_required
def delete_inventory(id):
    item = InventoryItem.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('inventory'))

@app.route('/appointments')
@login_required
def appointments():
    appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=appointments)

@app.route('/add_appointment', methods=['GET', 'POST'])
@login_required
def add_appointment():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        date = request.form['date']
        reason = request.form['reason']
        new_appointment = Appointment(patient_name=patient_name, date=date, reason=reason)
        db.session.add(new_appointment)
        db.session.commit()
        return redirect(url_for('appointments'))
    return render_template('add_appointment.html')

@app.route('/delete_appointment/<int:id>', methods=['POST'])
@login_required
def delete_appointment(id):
    appointment = Appointment.query.get(id)
    db.session.delete(appointment)
    db.session.commit()
    return redirect(url_for('appointments'))

@app.route('/forum', methods=['GET', 'POST'])
@login_required
def forum():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = current_user.username
        new_post = ForumPost(title=title, content=content, author=author)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('forum'))
    posts = ForumPost.query.all()
    return render_template('forum.html', posts=posts)

@app.route('/delete_post/<int:id>', methods=['POST'])
@login_required
def delete_post(id):
    post = ForumPost.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('forum'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
