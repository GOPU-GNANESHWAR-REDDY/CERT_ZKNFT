from api.utils.storage import save_to_file, load_from_file

STUDENT_DB_FILE = "data/students.json"
student_profiles = load_from_file(STUDENT_DB_FILE)

def save_students():
    save_to_file(student_profiles, STUDENT_DB_FILE)
