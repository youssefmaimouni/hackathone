from app import app, db  # Import your Flask app and SQLAlchemy instance

with app.app_context():
    db.drop_all()  # Drops all tables in the database
    print("All tables have been dropped.")