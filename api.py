from werkzeug.security import generate_password_hash

# Create a new admin user with a hashed password
new_admin = Admin(
    email="admin@example.com",  # Replace with the actual admin email
    password=generate_password_hash("adminpass"),  # Hash the password
    role="admin"  # Optionally, specify the role
)

# Add the new admin to the database and commit the changes
with app.app_context():  # Ensure this is inside an app context
    db.session.add(new_admin)  # Add the new user to the session
    db.session.commit()  # Commit the transaction to save to the database

print("Admin user added successfully!")
