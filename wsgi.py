from run_interface import app
import db_utils

if __name__ == "__main__":
  db_utils.initialize_database()
  app.run()