from run_interface import app
import db_utils as db

if __name__ == "__main__":
    db.initialize_database()
    app.run()
