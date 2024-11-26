import bcrypt

# Create an admin user
new_admin = Admin(
    email="admin@example.com",
    password=bcrypt.hashpw("adminpass".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
    role="admin"
)
db.session.add(new_admin)
db.session.commit()
