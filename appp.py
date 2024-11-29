from flask import Flask , render_template, request, redirect, url_for,jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import base64
from sqlalchemy import func
from sqlalchemy import extract
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime



app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/hack'
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

from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route("/profile", methods=["GET"])
def get_profile():
    # Retrieve the JWT identity
    admin_id = 1

    # Debug the value of admin_id
    print("JWT Identity:", admin_id)

    # Ensure admin_id is an integer
    try:
        admin_id = int(admin_id)  # Convert the identity to an integer
    except ValueError:
        return jsonify({"error": "Invalid token identity"}), 400

    # Query the Admin table for the provided ID
    admin = Admin.query.get(admin_id)

    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    # Return the admin profile
    return jsonify({
        "first_name": admin.first_name,
        "last_name": admin.last_name,
        "email": admin.email
    }), 200



@app.route("/courses", methods=["GET"])
def get_courses():
    courses = Course.query.all()

    courses_list = []
    for course in courses:
        # Query the CourseGainedSkill table to get the associated gained skills
        gained_skills = db.session.query(GainedSkill.name).join(CourseGainedSkill).filter(CourseGainedSkill.course_id == course.id).all()
        
        # Convert the gained skills into a list of names
        gained_skills_list = [gs.name for gs in gained_skills]
        required_skills = db.session.query(RequiredSkill.name).join(CourseRequiredSkill).filter(CourseRequiredSkill.course_id == course.id).all()
        
        # Convert the gained skills into a list of names
        required_skills_list = [gs.name for gs in required_skills]
        professors = db.session.query(Professor.first_name, Professor.last_name).join(CourseProfessor).filter(CourseProfessor.course_id == course.id).all()

        # Combine first_name and last_name into a single string
        professors_list = [f"{prof.first_name} {prof.last_name}" for prof in professors]

        courses_list.append({
            "id": course.id,
            "title": course.title,
            "is_completed": "yes" if course.is_completed else "no",
            "department": course.department.name if course.department else None,
            "gainedSkills": gained_skills_list,  # List of gained skill names
            "requiredSkills": required_skills_list,  # List of gained skill names
            "professors": professors_list,  # List of professor names
            # Add other fields as needed, like requiredSkills and professors
        })

    return jsonify(courses_list), 200

@app.route("/courses/<int:id>", methods=["GET"])
def get_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({"error": "Course not found"}), 404
        # Query the CourseGainedSkill table to get the associated gained skills
    gained_skills = db.session.query(GainedSkill.name).join(CourseGainedSkill).filter(CourseGainedSkill.course_id == course.id).all()
        
        # Convert the gained skills into a list of names
    gained_skills_list = [gs.name for gs in gained_skills]
    required_skills = db.session.query(RequiredSkill.name).join(CourseRequiredSkill).filter(CourseRequiredSkill.course_id == course.id).all()
        
        # Convert the gained skills into a list of names
    required_skills_list = [gs.name for gs in required_skills]
    professors = db.session.query(Professor.first_name, Professor.last_name).join(CourseProfessor).filter(CourseProfessor.course_id == course.id).all()

        # Combine first_name and last_name into a single string
    professors_list = [f"{prof.first_name} {prof.last_name}" for prof in professors]

    return jsonify({
            "id": course.id,
            "title": course.title,
            "is_completed": "yes" if course.is_completed else "no",
            "department": course.department.name if course.department else None,
            "gainedSkills": gained_skills_list,  # List of gained skill names
            "requiredSkills": required_skills_list,  # List of gained skill names
            "professors": professors_list,  # List of professor names
            # Add other fields as needed, like requiredSkills and professors
        }

    ), 200

@app.route("/courses", methods=["POST"])
def create_course():

    # Parse the incoming JSON data
    data = request.get_json()

    # Extract data from the request
    title = data.get("title")
    is_completed = data.get("is_completed")
    department_id = data.get("department")
    gained_skills_ids = data.get("gainedSkills")
    required_skills_ids = data.get("requiredSkills")
    professors_ids = data.get("professors")

    # Validate the required fields
    if not title or department_id is None:
        return jsonify({"error": "Title and department are required"}), 400

    # Create a new course
    new_course = Course(
        title=title,
        is_completed=is_completed,
        department_id=department_id
    )

    # Add the new course to the session and commit to save it
    db.session.add(new_course)
    db.session.commit()

    # Associate required skills with the course
    for skill_id in required_skills_ids:
        required_skill = RequiredSkill.query.get(skill_id)
        if required_skill:
            course_reqskill=CourseRequiredSkill(required_skill_id=skill_id,course_id=new_course.id)
            db.session.add(course_reqskill)
    # Associate gained skills with the course
    for skill_id in gained_skills_ids:
        gained_skill = GainedSkill.query.get(skill_id)
        if gained_skill:
            course_gained=CourseGainedSkill(gained_skill_id=skill_id,course_id=new_course.id)
            db.session.add(course_gained)



    # Associate professors with the course
    for professor_id in professors_ids:
        professor = Professor.query.get(professor_id)
        if professor:
            course_professor=CourseProfessor(professor_id=professor_id,course_id=new_course.id,assignment_date=datetime.now())
            db.session.add(course_professor)

    # Commit all associations
    db.session.commit()

    # Return the course_id in the response
    return jsonify({"course_id": new_course.id}), 201

@app.route("/courses/<int:id>", methods=["PUT"])
def update_course(id):
    # Parse the incoming JSON data
    data = request.get_json()

    # Fetch the course by ID
    course = Course.query.get(id)

    # If the course doesn't exist, return a 404 error
    if not course:
        return jsonify({"error": "Course not found"}), 404

    # Extract data from the request
    title = data.get("title")
    is_completed = data.get("is_completed")
    department_id = data.get("department")
    gained_skills_ids = data.get("gainedSkills")
    required_skills_ids = data.get("requiredSkills")
    professors_ids = data.get("professors")

    # Update course fields
    if title:
        course.title = title
    if is_completed is not None:
        course.is_completed = is_completed
    if department_id is not None:
        course.department_id = department_id

    # Commit the changes to the course fields
    db.session.commit()

    # Remove existing associations (delete them explicitly)
    CourseGainedSkill.query.filter_by(course_id=course.id).delete()
    CourseRequiredSkill.query.filter_by(course_id=course.id).delete()
    CourseProfessor.query.filter_by(course_id=course.id).delete()

    # Re-associate gained skills
    for skill_id in gained_skills_ids:
        gained_skill = GainedSkill.query.get(skill_id)
        if gained_skill:
            course_gained = CourseGainedSkill(gained_skill_id=skill_id, course_id=course.id)
            db.session.add(course_gained)

    # Re-associate required skills
    for skill_id in required_skills_ids:
        required_skill = RequiredSkill.query.get(skill_id)
        if required_skill:
            course_reqskill = CourseRequiredSkill(required_skill_id=skill_id, course_id=course.id)
            db.session.add(course_reqskill)

    # Re-associate professors
    for professor_id in professors_ids:
        professor = Professor.query.get(professor_id)
        if professor:
            course_professor = CourseProfessor(professor_id=professor_id, course_id=course.id, assignment_date=datetime.now())
            db.session.add(course_professor)

    # Commit all associations
    db.session.commit()

    # Return the updated course_id in the response
    return jsonify({"course_id": course.id}), 200

@app.route("/courses/<int:id>", methods=["DELETE"])
def delete_course(id):
    # Fetch the course by ID
    course = Course.query.get(id)

    # If the course doesn't exist, return a 404 error
    if not course:
        return jsonify({"error": "Course not found"}), 404

    # Remove associations from the many-to-many relationship tables
    CourseGainedSkill.query.filter_by(course_id=course.id).delete()
    CourseRequiredSkill.query.filter_by(course_id=course.id).delete()
    CourseProfessor.query.filter_by(course_id=course.id).delete()

    # Finally, delete the course
    db.session.delete(course)
    db.session.commit()

    # Return a success message
    return jsonify({"message": "Course deleted successfully"}), 200
@app.route('/professors', methods=['GET'])
def get_professors():
    professors = Professor.query.all()
    professors_list = []
    for professor in professors:
        professors_list.append({
            'id': professor.id,
        "firstname": professor.first_name,
        "lastname": professor.last_name,
        "email": professor.email,
        "hire_date": professor.hire_date,
        "is_active": professor.is_active,
        "birth_date": professor.birth_date,
        "phone_number": professor.phone_number,
        "salary": professor.salary,
        "professor_number": professor.professor_number
    })
    
    return jsonify(professors_list), 200
    


# Endpoint to get professor profile by ID
@app.route('/professor/<int:id>/profile', methods=['GET'])
def get_professor_profile(id):
    professor = Professor.query.get(id)

    if professor is None:
        return jsonify({"error": "Professor not found"}), 404

    return jsonify({
        "firstname": professor.first_name,
        "lastname": professor.last_name,
        "email": professor.email,
        "hire_date": professor.hire_date,
        "is_active": professor.is_active,
        "birth_date": professor.birth_date,
        "phone_number": professor.phone_number,
        "salary": professor.salary,
        "professor_number": professor.professor_number
    }), 200
    # Endpoint to add a new professor (POST)
@app.route('/professors/<int:id>', methods=['GET'])
def get_professor_profil(id):
    professor = Professor.query.get(id)

    if professor is None:
        return jsonify({"error": "Professor not found"}), 404

    return jsonify({
        "firstname": professor.first_name,
        "lastname": professor.last_name,
        "email": professor.email,
        "hire_date": professor.hire_date,
        "is_active": professor.is_active,
        "birth_date": professor.birth_date,
        "phone_number": professor.phone_number,
        "salary": professor.salary,
        "professor_number": professor.professor_number
    }), 200
@app.route('/professors', methods=['POST'])
def add_professor():
    data = request.get_json()

    # Password hashing before saving
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    new_professor = Professor(
        first_name=data['firstname'],
        last_name=data['lastname'],
        email=data['email'],
        hire_date=data['hire_date'],
        is_active=data.get('is_active', True),
        password=hashed_password,
        birth_date=data.get('birth_date'),
        phone_number=data.get('phone_number'),
    )
    
    db.session.add(new_professor)
    db.session.commit()
    
    return jsonify({"message": "Professor created successfully","prof_id":new_professor.id}), 201


# Endpoint PUT pour mettre à jour un professeur
@app.route('/professors/<int:id>', methods=['PUT'])
def update_professor(id):
    data = request.get_json()

    # Récupérer le professeur par son ID
    professor = Professor.query.get(id)
    if not professor:
        return jsonify({"error": "Professor not found"}), 404

    # Mettre à jour les champs (si présents dans la requête)
    if 'firstname' in data:
        professor.first_name = data['firstname']
    if 'lastname' in data:
        professor.last_name = data['lastname']
    if 'email' in data:
        professor.email = data['email']
    if 'hire_date' in data:
        professor.hire_date = data['hire_date']  # Assure-toi que la date est bien formatée (YYYY-MM-DD)
    if 'password' in data:
        # Hacher le mot de passe avant de le sauvegarder
        professor.password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Sauvegarder les modifications
    db.session.commit()

    return jsonify({"message": "Professor updated successfully"})

@app.route('/professors/<int:id>', methods=['DELETE'])
def delete_professor(id):
    # Recherche du professeur dans la base de données
    professor = Professor.query.get(id)
    
    
    # Si le professeur n'existe pas, renvoie une erreur 404
    if not professor:
        
        return jsonify({"message": "professor not found"}), 404
    CourseProfessor.query.filter_by(professor_id=professor.id).delete()
    # Supprimer le professeur
    db.session.delete(professor)
    db.session.commit()
    
    # Retourner une réponse de confirmation
    return jsonify({"message": f"Professor with id {id} has been deleted successfully"}), 200

@app.route("/professor/<int:id>/courses", methods=["GET"])
def get_professor_courses(id):
    # Query the CourseProfessor table to get all course IDs associated with the professor
    course_professors = CourseProfessor.query.filter_by(professor_id=id).all()

    # If no courses are found for this professor
    if not course_professors:
        return jsonify({"error": "No courses found for this professor"}), 404

    # Get all the course details for the professor
    courses = []
    for course_professor in course_professors:
        course = course_professor.course
        assignment_date=course_professor.assignment_date
        courses.append({
            "id": course.id,
            "title": course.title,
            "is_completed": course.is_completed,
            "department": course.department_id,  # Or you can add the department's name if needed
            "assignment_date":assignment_date
        })

    # Return the list of courses
    return jsonify(courses), 200

@app.route("/professor/<int:prof_id>/courses/<int:course_id>", methods=["GET"])
def get_professor_course(prof_id,course_id):
    # Query the CourseProfessor table to get all course IDs associated with the professor
    course_professors = CourseProfessor.query.filter_by(professor_id=prof_id).all()

    # If no courses are found for this professor
    if not course_professors:
        return jsonify({"error": "No courses found for this professor"}), 404

    # Get all the course details for the professor
    
    for course_professor in course_professors:
        if course_professor.course_id == course_id:
            course = course_professor.course
    if course :
        return get_course(course.id)
    else:
        return jsonify({"error": "Course not found for this professor"}), 404
    



@app.route("/statistic_1", methods=["GET"])
def get_department_completion_rate_chart():
    # Query to get department completion rates
    departments = db.session.query(
        Course.department_id, 
        db.func.count(Course.id).label('total_courses'),
        db.func.sum(
            db.case(
                (Course.is_completed == True, 1),
                else_=0
            )
        ).label('completed_courses')
    ).group_by(Course.department_id).all()

    # If no departments are found
    if not departments:
        return jsonify({"error": "No departments found"}), 404

    # Prepare data for plotting
    department_ids = [str(department.department_id) for department in departments]
    total_courses = [department.total_courses for department in departments]
    completed_courses = [department.completed_courses for department in departments]
    completion_rates = [(completed / total) * 100 if total > 0 else 0 for completed, total in zip(completed_courses, total_courses)]

    # Create the bar chart using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(department_ids, completion_rates, color='skyblue')

    # Add labels and title
    ax.set_xlabel('Department ID')
    ax.set_ylabel('Completion Rate (%)')
    ax.set_title('Department Course Completion Rates')

    # Convert the plot to a PNG image and encode it to base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_b64 = base64.b64encode(img.read()).decode('utf-8')

    # Return the image as a response
    return jsonify({"image": img_b64})

@app.route("/statistic_2", methods=["GET"])
def get_courses_per_department_chart():
    # Query to get the number of courses per department
    department_counts = db.session.query(
        Course.department_id,
        db.func.count(Course.id).label('course_count')
    ).group_by(Course.department_id).all()

    # If no departments or courses are found
    if not department_counts:
        return jsonify({"error": "No departments found or no courses available"}), 404

    # Prepare data for plotting
    department_ids = [str(department.department_id) for department in department_counts]
    course_counts = [department.course_count for department in department_counts]

    # Create the bar chart using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(department_ids, course_counts, color='lightcoral')

    # Add labels and title
    ax.set_xlabel('Department ID')
    ax.set_ylabel('Number of Courses')
    ax.set_title('Number of Courses per Department')

    # Convert the plot to a PNG image and encode it to base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_b64 = base64.b64encode(img.read()).decode('utf-8')

    # Return the image as a response
    return jsonify({"image": img_b64})


@app.route("/statistic_3", methods=["GET"])
def get_skills_per_course_chart():
    # Query to get the required and gained skills counts per course
    course_skills = db.session.query(
        Course.id.label('course_id'),
        db.func.count(CourseRequiredSkill.course_id).label('required_skills_count'),  # Use course_id for counting
        db.func.count(CourseGainedSkill.course_id).label('gained_skills_count')  # Similarly, use course_id in CourseGainedSkill
    ).join(CourseRequiredSkill, CourseRequiredSkill.course_id == Course.id, isouter=True) \
    .join(CourseGainedSkill, CourseGainedSkill.course_id == Course.id, isouter=True) \
    .group_by(Course.id).all()
    # If no courses or skills found
    if not course_skills:
        return jsonify({"error": "No courses found or no skills available"}), 404

    # Prepare data for plotting
    course_ids = [str(course.course_id) for course in course_skills]
    required_skills = [course.required_skills_count for course in course_skills]
    gained_skills = [course.gained_skills_count for course in course_skills]

    # Create the stacked bar chart using Matplotlib
    fig, ax = plt.subplots(figsize=(12, 6))

    # Plot the bars: first required skills, then gained skills on top
    ax.bar(course_ids, required_skills, label='Required Skills', color='skyblue')
    ax.bar(course_ids, gained_skills, bottom=required_skills, label='Gained Skills', color='lightcoral')

    # Add labels and title
    ax.set_xlabel('Course ID')
    ax.set_ylabel('Number of Skills')
    ax.set_title('Required vs. Gained Skills per Course')
    ax.legend()

    # Convert the plot to a PNG image and encode it to base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)  # Rewind the buffer to the beginning

    # Encode the image as a Base64 string
    img_b64 = base64.b64encode(img.read()).decode('utf-8')

    # Return the image as JSON
    return jsonify({"image": img_b64})


from sqlalchemy import func
import matplotlib.pyplot as plt
from io import BytesIO
import base64

from sqlalchemy import func
import matplotlib.pyplot as plt
from io import BytesIO
import base64

@app.route("/statistic_4", methods=["GET"])
def get_courses_per_department_over_time():
    # Query to count the number of courses per department, grouped by year from contract_start_date
    course_counts = db.session.query(
        Department.name.label('department_name'),
        func.year(Course.contract_start_date).label('year'),  # Extract year from contract_start_date
        func.count(Course.id).label('course_count')
    ).join(Department, Department.id == Course.department_id) \
     .group_by(Department.name, func.year(Course.contract_start_date)) \
     .order_by(Department.name, func.year(Course.contract_start_date)) \
     .all()

    if not course_counts:
        return jsonify({"error": "No courses found"}), 404

    # Prepare data for plotting
    departments = set([course.department_name for course in course_counts])  # Unique department names
    department_course_counts = {dept: [] for dept in departments}
    
    # Filter out None values from years
    years = sorted(set([course.year for course in course_counts if course.year is not None]))  # Sorted list of years

    # Prepare the course counts for each department by year
    for dept in departments:
        for year in years:
            count = next((course.course_count for course in course_counts if course.department_name == dept and course.year == year), 0)
            department_course_counts[dept].append(count)

    # Create the line chart
    plt.figure(figsize=(12, 6))
    
    # Plot the data for each department
    for dept, counts in department_course_counts.items():
        plt.plot(years, counts, label=dept)

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Number of Courses')
    plt.title('Number of Courses Offered by Each Department Over Time')
    plt.xticks(years, rotation=45)
    plt.legend(title='Departments')
    plt.grid(True)

    # Save the plot as an image (base64) to display in the response
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_b64 = base64.b64encode(img.read()).decode('utf-8')

    # Return just the Base64 string as JSON
    return jsonify({"image": img_b64})


@app.route("/statistic_5/<int:id_employee>", methods=["GET"])
def get_professor_working_days(id_employee):
    # Query to count the total number of distinct working days for the professor with id_employee
    working_days_query = db.session.query(
        CourseProfessor.professor_id,
        func.count(func.distinct(CourseProfessor.assignment_date)).label('working_days')
    ).join(Course, Course.id == CourseProfessor.course_id).group_by(CourseProfessor.professor_id).all()  # Fetch all results

    # Check if any data is found
    if not working_days_query:
        return jsonify({"error": "No data found"}), 404

    # Prepare data for the bar chart
    professor_ids = [str(row.professor_id) for row in working_days_query]
    working_days = [row.working_days for row in working_days_query]

    # Create the bar chart
    fig, ax = plt.subplots()
    ax.bar(professor_ids, working_days)

    # Set labels and title
    ax.set_xlabel('Professor ID')
    ax.set_ylabel('Total Working Days')
    ax.set_title('Total Working Days for Each Professor')

    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)

    # Encode the image as a Base64 string
    img_base64 = base64.b64encode(img.read()).decode('utf-8')

    # Return the image as JSON
    return jsonify({"image": img_base64})


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
