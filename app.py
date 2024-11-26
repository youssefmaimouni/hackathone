from flask import Flask , render_template, request, redirect, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token



app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/university'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
jwt = JWTManager(app)  

# Define the models based on the provided ER diagram

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    department_code = db.Column(db.Text, nullable=True)
    created_date = db.Column(db.Text, nullable=True)
    phone_number = db.Column(db.Text, nullable=True)
    email = db.Column(db.Text, nullable=True)

class Dataset(db.Model):
    __tablename__ = 'dataset'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school_department = db.Column(db.String(255), nullable=True)
    course_title = db.Column(db.String(255), nullable=True)
    date_and_time = db.Column(db.DateTime, nullable=True)
    finish_time = db.Column(db.DateTime, nullable=True)
    email = db.Column(db.String(255), nullable=True)
    required_skill = db.Column(db.String(255), nullable=True)
    professors = db.Column(db.String(255), nullable=True)
    gained_skill = db.Column(db.String(355), nullable=True)

class Professor(db.Model):
    __tablename__ = 'professor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    hire_date = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, default=None, nullable=True)
    password = db.Column(db.Text, nullable=False)
    birth_date = db.Column(db.Text, nullable=True)
    phone_number = db.Column(db.Text, nullable=True)
    salary = db.Column(db.Text, nullable=True)
    professor_number = db.Column(db.Text, nullable=True)


class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    is_completed = db.Column(db.Boolean, default=None)
    course_manager_email = db.Column(db.Text, nullable=True)
    client_company_name = db.Column(db.Text, nullable=True)
    contract_number = db.Column(db.Text, nullable=True)
    invoice_status = db.Column(db.Text, nullable=True)
    contract_start_date = db.Column(db.Text, nullable=True)
    approval_status = db.Column(db.Text, nullable=True)

    # Relationship to Department (assuming you have a Department model defined)
    department = db.relationship('Department', backref='courses', lazy=True)

class GainedSkill(db.Model):
    __tablename__ = 'gained_skill'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)

class RequiredSkill(db.Model):
    __tablename__ = 'required_skill'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)

class CourseRequiredSkill(db.Model):
    __tablename__ = 'course_required_skill'

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    required_skill_id = db.Column(db.Integer, db.ForeignKey('required_skill.id'), primary_key=True)

    # Optionally, define relationships for easier access to related objects:
    course = db.relationship('Course', backref=db.backref('required_skills', lazy=True))
    required_skill = db.relationship('RequiredSkill', backref=db.backref('courses', lazy=True))

class CourseGainedSkill(db.Model):
    __tablename__ = 'course_gained_skill'
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    gained_skill_id = db.Column(db.Integer, db.ForeignKey('gained_skill.id'), primary_key=True)
    course = db.relationship('Course', backref=db.backref('course_gained_skills', lazy=True))
    gained_skill = db.relationship('GainedSkill', backref=db.backref('course_gained_skills', lazy=True))

class CourseProfessor(db.Model):
    __tablename__ = 'course_professor'

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), primary_key=True)
    assignment_date = db.Column(db.DateTime, nullable=False)
    finish_date = db.Column(db.DateTime, nullable=True)

    # Relationship to Course and Professor
    course = db.relationship('Course', backref=db.backref('professors', lazy=True))
    professor = db.relationship('Professor', backref=db.backref('courses', lazy=True))



def restore_Departments(csv_file):
    # Charger le fichier CSV
    data = pd.read_csv(csv_file)
    print(data.head())
    # Insérer les données dans la base de données
    for _, row in data.iterrows():
        date=pd.to_datetime(row['created_date'],format='%Y-%m-%d %H:%M:%S')
        department = Department(name=row['name'],description=row['description'],department_code=row['department_code'],created_date=date,phone_number=row['phone_number'],email=row['email'])
        print(department.name)
        db.session.add(department)
    print('departements inserted')
    db.session.commit()
def restore_Professors(data):
    # Charger le fichier CSV
    print(data.head())
    for _, row in data.iterrows():
        professor = Professor(first_name=row['first_name'],last_name=row['last_name'],email=row['Email'])
        print(professor.last_name)
        db.session.add(professor)
    print('Professors inserted')
    db.session.commit()
def restore_Course(data):
    # Charger le fichier CSV
    print(data.head())
    for _, row in data.iterrows():
        if row['FinishTime']:
            is_completed=True
        else:
            is_completed=False

        course = Course(title=row['CourseTitle'],is_completed=is_completed)
        print(course.title)
        db.session.add(course)
    print('courses inserted')
    db.session.commit()
def restore_GainedSkill(data):
    # Charger le fichier CSV
    print(data.head())
    for index, row in data.iterrows():
        gainedSkill = GainedSkill(name=row['Skill'])
        print(gainedSkill.name)
        db.session.add(gainedSkill)
    print('gainedSkills inserted')
    db.session.commit()
def restore_RequiredSkill(data):
    # Charger le fichier CSV
    print(data.head())
    for index, row in data.iterrows():
        requiredSkill = RequiredSkill(name=row['Skill'])
        print(requiredSkill.name)
        db.session.add(requiredSkill)
    print('RequiredSkills inserted')
    db.session.commit()
@app.route('/restore', methods=['POST'])
def restore():
    csv_file = 'department.csv'  # Chemin vers votre fichier CSV
    restore_Departments(csv_file)
    df=pd.read_csv('sorted_Data.csv')
    filtered_df = df[~df['Professors'].str.contains(',', na=False)]

    # Step 2: Remove duplicate rows based on 'Professors' and 'email'
    df_prof = filtered_df.drop_duplicates(subset=['Professors', 'Email'])

    # Step 3: Split 'Professors' into 'first_name' and 'last_name'
    df_prof[['first_name', 'last_name']] = df_prof['Professors'].str.split(' ', n=1, expand=True)

    # Drop the original 'Professors' column if needed
    df_prof = df_prof.drop(columns=['Professors'])
    restore_Professors(df_prof)
    df=pd.read_csv('updated_sorted_Data.csv')

    # Step 2: Remove duplicate rows based on 'Professors' and 'email'
    df_course = df.drop_duplicates(subset=['CourseTitle', 'FinishTime'])
    restore_Course(df_course)
    df=pd.read_csv('sorted_Data.csv')
    skills_split = df['RequiredSkill'].str.split(',', expand=True)

    # Step 2: Melt the DataFrame to turn columns into rows
    skills_normalized = skills_split.melt(value_name='Skill').dropna()

    # Step 3: Clean up extra spaces and ensure uniqueness
    skills_normalized['Skill'] = skills_normalized['Skill'].astype('string').str.strip()
    df_reqSkills  = skills_normalized[['Skill']].drop_duplicates().reset_index(drop=True)

    restore_RequiredSkill(df_reqSkills)
    skills_split = df['GainedSkill'].str.split(',', expand=True)

    # Step 2: Melt the DataFrame to turn columns into rows
    skills_normalized = skills_split.melt(value_name='Skill').dropna()

    # Step 3: Clean up extra spaces and ensure uniqueness
    skills_normalized['Skill'] = skills_normalized['Skill'].astype('string').str.strip()
    df_gainSkills  = skills_normalized[['Skill']].drop_duplicates().reset_index(drop=True)

    restore_GainedSkill(df_gainSkills)



    return "Database restored successfully!", 200
    
@app.route('/departments')
def get_departments():
    departments = Department.query.all()
    professors=Professor.query.all()
    courses=Course.query.all()
    print('departments loaded')
    return render_template("index.html",departments=departments,professors=professors,courses=courses)

# Flask-JWT-Extended setup
app.config["JWT_SECRET_KEY"] = "your-secret-key"
jwt = JWTManager(app)

# Login route for admins
@app.route("/login", methods=["POST"])
def login():
    # Get data from the request
    email = request.json.get("email")
    password = request.json.get("password")

    # Validate input
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Query the admin table for the given email
    admin = Admin.query.filter_by(email=email).first()

    # Check if the admin exists and if the password is correct
    if admin and bcrypt.checkpw(password.encode("utf-8"), admin.password.encode("utf-8")):
        # Create a JWT access token
        access_token = create_access_token(identity={"id": admin.id, "email": admin.email})
        return jsonify({"access_token": access_token})

    # If authentication fails
    return jsonify({"error": "Invalid email or password"}), 401



@app.route('/admin/create', methods=['POST'])
def create_admin():
    new_admin = Admin(
    first_name="John",
    last_name="Doe",
    email="admin@example.com",
    password=bcrypt.hashpw("adminpass".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
    )
    db.session.add(new_admin)
    db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
