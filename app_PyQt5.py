import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QTabWidget
from PyQt5.QtWidgets import *
import sqlite3
from objects import Person, Student, Instructor, Course
import json
import csv

conn = sqlite3.connect('university.db')
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        ID TEXT PRIMARY KEY,
        Name TEXT NOT NULL,
        Age INTEGER,
        Email TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Instructors (
        ID TEXT PRIMARY KEY,
        Name TEXT NOT NULL,
        Age INTEGER,
        Email TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Courses (
        ID TEXT PRIMARY KEY,
        Name TEXT NOT NULL,
        InstructorID TEXT,
        FOREIGN KEY (InstructorID) REFERENCES Instructors(ID) on delete cascade on update cascade
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Registrations (
        StudentID TEXT,
        CourseID TEXT,
        FOREIGN KEY (StudentID) REFERENCES Students(ID) on delete cascade on update cascade,
        FOREIGN KEY (CourseID) REFERENCES Courses(ID) on delete cascade on update cascade,
        PRIMARY KEY (StudentID, CourseID)
    )
''')

conn.commit()


def main():
    """
    Main function to start the School Management System application.
    
    This function creates the main window of the application with tabs for
    Students, Instructors, Courses, Registrations, and viewing and exporting the data. It initializes
    the GUI and connects the functions to the UI elements.

    :raises SystemExit: If the application exits unexpectedly.

    :return: nothing
    :rtype: None
    """
    sys.exit(app.exec_())
app =QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("School Management System")
window.setGeometry(100, 100, 1000, 1000)
window.show()
tabs = QTabWidget()
window.setCentralWidget(tabs)

def show_error_popup():
    """
    Displays an error message in a pop-up window.

    :return: nothing
    :rtype: None
    """
    # Create a message box for the error
    error_message = QMessageBox()
    error_message.setIcon(QMessageBox.Critical)
    error_message.setWindowTitle("Error")
    error_message.setText("An error occurred!")
    error_message.setInformativeText("Please check your input and try again.")
    error_message.setStandardButtons(QMessageBox.Ok)
    
    # Show the popup
    error_message.exec_()

def addStudent():
    """
    Adds a new student to the database.

    Retrieves student information from input fields and inserts a new record 
    into the Students table in the database. 
    updates the info in the tables by calling default_populate_tables.
    displays an error popup in case of errors or bad inputs


    :return: Nothing.
    :rtype: None
    """
    name = student_name_entry.text()
    age = student_age_entry.text()
    email = student_email_entry.text()
    student_id = student_id_entry.text()
    if (any(field == "" for field in [name, age, email, student_id]) ):
        show_error_popup()
        return
    try:
        student = Student(name, age, email, student_id)
        cursor.execute("INSERT INTO Students (ID, Name, Age, Email) VALUES (?, ?, ?, ?)", 
                        (student_id, name, age, email))
        conn.commit()
    except Exception as e:
        print(e)
        show_error_popup()
    default_populate_tables()



def deleteStudent():
    """
    Deletes a student from the database.

    Retrieves the student ID from the input field and deletes the corresponding 
    record from the Students table in the database.  
    updates the info in the tables by calling default_populate_tables
    displays an error popup in case of errors

    :return: Nothing.
    :rtype: None
    """
    try:
        cursor.execute("delete from Students where ID =  ?", (student_id_entry.text(),))
        conn.commit()
    except Exception as e:
        print(e)
        show_error_popup()
    default_populate_tables()


def editStudent():
    """
    Edit the student whose ID is retrieved from the input field
    by replacing one or more of its attributes in the database with the corresponding values in the nonempty input field.
    if an input field is left empty, the corresponding value is unchanged
    updates the info in the tables by calling default_populate_tables
    displays an error popup in case of errors


    :return: Nothing.
    :rtype: None
    """
    name = student_name_entry.text()
    age = student_age_entry.text()
    email = student_email_entry.text()
    student_id = student_id_entry.text()
    try:
        if (any(field != "" for field in [name, age, email])):
            if name!="":
                cursor.execute("Update Students set Name = ? where ID = ?", (name, student_id))
                conn.commit()
            if age!="":
                cursor.execute("Update Students set Age = ? where ID = ?", (age, student_id))
                conn.commit()
            if email!="":
                cursor.execute("Update Students set Email = ? where ID = ?", (email, student_id))
                conn.commit()
    except Exception as e:
        show_error_popup()
        print(e)
    default_populate_tables()


def addInstructor():
    """
    Adds a new instructor to the database.

    Retrieves instructor information from input fields and inserts a new record 
    into the instructor table in the database.
    updates the info in the tables by calling default_populate_tables
    displays an error popup in case of errors


    :return: Nothing.
    :rtype: None
    """
    name = instructor_name_entry.text()
    age = instructor_age_entry.text()
    email = instructor_email_entry.text()
    instructor_id = instructor_id_entry.text()
    if (any(field == "" for field in [name, age, email, instructor_id]) ):
        show_error_popup()
        return
    
    try:
        instructor = Instructor(name, age, email, instructor_id)
        cursor.execute("INSERT INTO Instructors (ID, Name, Age, Email) VALUES (?, ?, ?, ?)", 
                    (instructor_id, name, age, email))
        conn.commit()
    except Exception as e:
        show_error_popup()
        print(e)
    default_populate_tables()



def deleteInstructor():
    """
    Deletes a instructor from the database.

    Retrieves the instructor ID from the input field and deletes the corresponding 
    record from the instructors table in the database.  
    updates the info in the tables by calling default_populate_tables
    displays an error popup in case of errors


    :return: Nothing.
    :rtype: None
    """
    try:
        cursor.execute("delete from Instructors where ID =  ?", (instructor_id_entry.text(),))
        conn.commit()
    except Exception as e:
        show_error_popup()
        print(e)
    default_populate_tables()

    

def editInstructor():
    """
    Edit the instructor whose ID is retrieved from the input field
    by replacing one or more of its attributes in the database with the corresponding values in the nonempty input field.
    if an input field is left empty, the corresponding value is unchanged
    updates the info in the tables by calling default_populate_tables
    displays an error popup in case of errors


    :return: Nothing.
    :rtype: None
    """
    name = instructor_name_entry.text()
    age = instructor_age_entry.text()
    email = instructor_email_entry.text()
    instructor_id = instructor_id_entry.text()
    try:
        if (any(field != "" for field in [name, age, email])):
            if name!="":
                cursor.execute("Update Instructors set Name = ? where ID = ?", (name, instructor_id))
                conn.commit()
            if age!="":
                cursor.execute("Update Instructors set Age = ? where ID = ?", (age, instructor_id))
                conn.commit()
            if email!="":
                cursor.execute("Update Instructors set Email = ? where ID = ?", (email, instructor_id))
                conn.commit()
    except Exception as e:
        show_error_popup()
        print(e)
    default_populate_tables()


def addCourse():
    """
    Adds a new course to the database.

    Retrieves course information from input fields and inserts a new record 
    into the Courses table in the database.
    updates the info in the tables by calling default_populate_tables
    displays an error popup in case of errors


    :return: Nothing.
    :rtype: None
    """
    course_name = course_name_entry.text()
    course_id = course_id_entry.text()
    instructor_id = course_instructor_entry.text()
    if (any(field == "" for field in [course_name, course_id, instructor_id]) ):
        show_error_popup()
        return
    try:
        course = Course(course_id, course_name)
        course.instructor_id = instructor_id
        cursor.execute("INSERT INTO Courses (ID, Name, InstructorID) VALUES (?, ?, ?)", 
                    (course_id, course_name, instructor_id))
        conn.commit()
    except Exception as e:
        show_error_popup()
        print(e)
    default_populate_tables()



def deleteCourse():
    """
    Deletes a course from the database.

    Retrieves the course ID from the input field and deletes the corresponding 
    record from the courses table in the database.  
    updates the info in the tables by calling default_populate_tables
    displays an error popup in case of errors


    :return: Nothing.
    :rtype: None
    """
    try:
        cursor.execute("delete from Courses where ID =  ?", (course_id_entry.text(),))
        conn.commit()
    except Exception as e:
        show_error_popup()
        print(e)
    default_populate_tables()


def editCourse():
    """
    Edit the course whose ID is retrieved from the input field
    by replacing one or more of its attributes in the database with the corresponding values in the nonempty input field.
    if an input field is left empty, the corresponding value is unchanged
    updates the info in the tables by calling default_populate_tables
    displays an error popup in case of errors


    :return: Nothing.
    :rtype: None
    """
    name = course_name_entry.text()
    course_id = course_id_entry.text()
    instructor_id = course_instructor_entry.text()
    try:
        if (any(field != "" for field in [name, instructor_id])):
            if name!="":
                cursor.execute("Update Courses set Name = ? where ID = ?", (name, course_id))
                conn.commit()
            if instructor_id!="":
                cursor.execute("Update Courses set InstructorID = ? where ID = ?", (instructor_id, course_id))
                conn.commit()
    except Exception as e:
        show_error_popup()
        print(e)
    default_populate_tables()


def registerStudent():
    """
    Obtains a studentID and a courseID from input fields and inserts a record in the Registrations table,
    indicating that this student has registered in this course
    displays an error popup in case of errors


    :return: Nothing.
    :rtype: None
    """
    student_id = registering_student_id_entry.text()
    course_id = registered_course.currentText()
    try:
        cursor.execute("Insert into Registrations (StudentID, CourseID) values (?, ?)", (student_id, course_id))
        conn.commit()
    except Exception as e:
        show_error_popup()
        print(e)
        
def dropStudent():
    """
    Obtains a studentID and a courseID from input fields and deletes the row in Registrations table which corresponds to both values.
    shows an error popup in case of errors


    :return: Nothing.
    :rtype: None
    """
    student_id = registering_student_id_entry.text()
    course_id = registered_course.currentText()
    try:
        cursor.execute("delete from Registrations where StudentID=? and CourseID=?", (student_id, course_id))
        conn.commit()
    except Exception as e:
        show_error_popup()
        print(e)

def assignInstructor():
    """
    Obtains a course ID and InstructorID from input fields, and sets the value of the instructorID for this course to the
    obtained instructor id.
    displays an error popup in case of errors

    :return: Nothing.
    :rtype: None
    """
    course_id = assigned_course.currentText()
    instructor_id = assigned_instructor_id_entry.text()
    try:
        cursor.execute("update Courses set InstructorID = ? where ID = ? ", (instructor_id, course_id))
        conn.commit()
    except Exception as e:
        show_error_popup()
        print(e)

def changeInstructor():
    """
    Obtains a course ID and InstructorID from input fields, and sets the value of the instructorID for this course to the
    obtained instructor id.
    displays an error popup in case of error

    :return: Nothing.
    :rtype: None
    """
    instructor_id = assigned_instructor_id_entry.text()
    course_id = assigned_course.currentText()
    try:
        cursor.execute("Update Courses set InstructorID = ? where ID= ?", (instructor_id, course_id))
        conn.commit()
    except Exception as e:
        show_error_popup()
        print(e)


# Create tabs
student_tab = QWidget()
instructor_tab = QWidget()
course_tab = QWidget()
register_tab = QWidget()
assign_tab = QWidget()
display_tab = QWidget()
export_tab = QWidget()

tabs.addTab(student_tab, 'Students')
tabs.addTab(instructor_tab, 'Instructors')
tabs.addTab(course_tab, 'Courses')
tabs.addTab(register_tab, "Register Students")
tabs.addTab(assign_tab, "Assign Instructors")
tabs.addTab(display_tab, "Display Data")
tabs.addTab(export_tab, "Export Data")

### student tab

student_id_entry = QLineEdit()  
student_name_entry = QLineEdit()
student_age_entry = QLineEdit()
student_email_entry = QLineEdit()

add_student = QPushButton('Add Student')
add_student.clicked.connect(addStudent)
delete_student = QPushButton('Delete Student with this ID')
delete_student.clicked.connect(deleteStudent)
edit_student = QPushButton('Edit Student with this ID')
edit_student.clicked.connect(editStudent)

student_form_layout = QFormLayout()
student_form_layout.addRow('ID:', student_id_entry)
student_form_layout.addRow('Name:', student_name_entry)
student_form_layout.addRow('Age:', student_age_entry)
student_form_layout.addRow('Email:', student_email_entry)
student_form_layout.addRow(add_student)
student_form_layout.addRow(delete_student)
student_form_layout.addRow(edit_student)
student_tab.setLayout(student_form_layout)


#### Instructor tab

instructor_id_entry = QLineEdit()  
instructor_name_entry = QLineEdit()
instructor_age_entry = QLineEdit()
instructor_email_entry = QLineEdit()

add_instructor = QPushButton('Add instructor')
add_instructor.clicked.connect(addInstructor)
delete_instructor = QPushButton('Delete instructor with this ID')
delete_instructor.clicked.connect(deleteInstructor)
edit_instructor = QPushButton('Edit instructor with this ID')
edit_instructor.clicked.connect(editInstructor)

instructor_form_layout = QFormLayout()
instructor_form_layout.addRow('ID:', instructor_id_entry)
instructor_form_layout.addRow('Name:', instructor_name_entry)
instructor_form_layout.addRow('Age:', instructor_age_entry)
instructor_form_layout.addRow('Email:', instructor_email_entry)
instructor_form_layout.addRow(add_instructor)
instructor_form_layout.addRow(delete_instructor)
instructor_form_layout.addRow(edit_instructor)
instructor_tab.setLayout(instructor_form_layout)

#### Course Tab

course_id_entry = QLineEdit()  
course_name_entry = QLineEdit()
course_instructor_entry = QLineEdit()

add_course = QPushButton('Add course')
add_course.clicked.connect(addCourse)
delete_course = QPushButton('Delete course with this ID')
delete_course.clicked.connect(deleteCourse)
edit_course = QPushButton('Edit course with this ID')
edit_course.clicked.connect(editCourse)

course_form_layout = QFormLayout()
course_form_layout.addRow('ID:', course_id_entry)
course_form_layout.addRow('Name:', course_name_entry)
course_form_layout.addRow('Instructor ID:', course_instructor_entry)
course_form_layout.addRow(add_course)
course_form_layout.addRow(delete_course)
course_form_layout.addRow(edit_course)
course_tab.setLayout(course_form_layout)

#### Registration tab

registering_student_id_entry = QLineEdit()  
registered_course = QComboBox()
registered_course.addItems([t[0] for t in cursor.execute("select ID from Courses").fetchall()])

register = QPushButton('register student')
register.clicked.connect(registerStudent)
drop_student = QPushButton('Drop student from course')
drop_student.clicked.connect(dropStudent)

registration_form_layout = QFormLayout()
registration_form_layout.addRow('Student ID:', registering_student_id_entry)
registration_form_layout.addRow('Course ID:', registered_course)
registration_form_layout.addRow(register)
registration_form_layout.addRow(drop_student)
register_tab.setLayout(registration_form_layout)

#### Assign instructor tab

assigned_instructor_id_entry = QLineEdit()  
assigned_course = QComboBox()
assigned_course.addItems([t[0] for t in cursor.execute("select ID from Courses").fetchall()])


assign = QPushButton('assign instructor')
assign.clicked.connect(assignInstructor)
change_instructor = QPushButton('Change Instructor')
change_instructor.clicked.connect(changeInstructor)

assign_form_layout = QFormLayout()
assign_form_layout.addRow('Instructor ID:', assigned_instructor_id_entry)
assign_form_layout.addRow('Course ID:', assigned_course)
assign_form_layout.addRow(assign)
assign_form_layout.addRow(change_instructor)
assign_tab.setLayout(assign_form_layout)

#### View tables tab

def default_populate_tables():
    """
    populates the tables in the View Tables tab with all available entries (no filters)

    :return: Nothing.
    :rtype: None

    """
    populate_table(student_table, cursor.execute("select * from Students").fetchall())
    populate_table(course_table, cursor.execute("select * from Courses").fetchall())
    populate_table(instructor_table, cursor.execute("select * from Instructors").fetchall())

def populate_table(table, data):
    """
    populates the given table in the View Tables tab with the given data, after clearing it from existing data

    :param table: The table object to populate
    :type table: QTableWidget

    :param data: the data to populate the table with
    :type data: list of 4-tuples or 3-tuples 

    :return: Nothing.
    :rtype: None
    """
    i = 0
    table.setRowCount(0)
    for t in data:
        table.insertRow(i)
        table.setItem(i, 0, QTableWidgetItem(t[0]))
        table.setItem(i, 1, QTableWidgetItem(t[1]))
        table.setItem(i, 2, QTableWidgetItem(str(t[2])))
        try:
            table.setItem(i, 3, QTableWidgetItem(t[3]))
        except Exception as e:
            pass
        i+=1

#### Filter

def filter_results():
    """
    Obtains filter values from the input fields, and obtains data from the database according to these filters.
    Clears the tables, then populates them with the filtered results

    :return: Nothing.
    :rtype: None
    """
    student_table.setRowCount(0)
    instructor_table.setRowCount(0)
    course_table.setRowCount(0)
    name = filter_name_entry.text()
    id = filter_id_entry.text()
    student_query = "select * from Students where true "
    instructor_query = "select * from Instructors where true "
    course_query = "select * from Courses where true "
    if name!="":
        student_query += " and Name = '" + name +"'"
        instructor_query+= " and Name = '" + name +"'"
        course_query+= " and Name = '" + name +"'"
    if id != "":
        student_query += " and ID = '"+ id +"'"
        instructor_query+= " and ID = '"+ id +"'"
        course_query+= " and ID = '"+ id +"'"
        
    populate_table(student_table, cursor.execute(student_query).fetchall() )
    populate_table(instructor_table, cursor.execute(instructor_query).fetchall())
    populate_table(course_table, cursor.execute(course_query).fetchall() )

main_layout = QVBoxLayout()


filter_name_entry = QLineEdit() 
filter_id_entry = QLineEdit() 
filter_layout = QFormLayout()
filter = QPushButton('Filter')
filter.clicked.connect(filter_results)
filter_layout.addRow('Filter by Name:', filter_name_entry)
filter_layout.addRow('Filter by ID:', filter_id_entry)
filter_layout.addRow(filter)
main_layout.addLayout(filter_layout)


tables_tab_layout = QVBoxLayout()

student_table = QTableWidget()
student_table.setColumnCount(4)
student_table.setHorizontalHeaderLabels(['ID', 'Name', 'Age', 'Email'])

instructor_table = QTableWidget()
instructor_table.setColumnCount(4)
instructor_table.setHorizontalHeaderLabels(['ID', 'Name', 'Age', 'Email'])

course_table = QTableWidget()
course_table.setColumnCount(3)
course_table.setHorizontalHeaderLabels(['ID', 'Name', 'Instructor ID'])

default_populate_tables()

main_layout.addWidget(student_table)
main_layout.addWidget(instructor_table)
main_layout.addWidget(course_table)

display_tab.setLayout(main_layout)

#### Export/Import data tab

def exportStudents():
    """
    exports all database entries in the students table into a json file named students.json.
    Creates this file if it doesn't exist
    Overwrites it if it exists

    :return: Nothing.
    :rtype: None
    """
    all_students = cursor.execute("select * from Students").fetchall()
    with open("students.json", 'w') as file:
        # Write an empty JSON object (or any initial content)
        json.dump([], file)
    for t in all_students:
        student = Student(t[1], t[2], t[3], t[0])
        student.save_to_json()

def exportInstructors():
    """
    exports all database entries in the instructors table into a json file named instructors.json.
    Creates this file if it doesn't exist
    Overwrites it if it exists

    :return: Nothing.
    :rtype: None
    """
    all_instructors = cursor.execute("select * from Instructors").fetchall()
    with open("instructors.json", 'w') as file:
        # Write an empty JSON object (or any initial content)
        json.dump([], file)
    for t in all_instructors:
        instructor = Instructor(t[1], t[2], t[3], t[0])
        instructor.save_to_json()

def exportCourses():
    """
    exports all database entries in the courses table into a json file named courses.json.
    Creates this file if it doesn't exist
    Overwrites it if it exists

    :return: Nothing.
    :rtype: None
    """
    all_courses = cursor.execute("select * from Courses").fetchall()
    with open("courses.json", 'w') as file:
        # Write an empty JSON object (or any initial content)
        json.dump([], file)
    for t in all_courses:
        course = Course(t[0],t[1])
        course.instructor_id = t[2]
        course.save_to_json()

def exportRegistrations():
    """
    exports all database entries in the regsitrations table into a json file named regsitrations.json.
    Creates this file if it doesn't exist
    Overwrites it if it exists

    :return: Nothing.
    :rtype: None
    """
    all_registrations = cursor.execute("select * from Registrations").fetchall()
    with open("registrations.json", 'w') as file:
        # Write an empty JSON object (or any initial content)
        json.dump([], file)
    data = []
    with open("registrations.json", 'w') as file:
        for t in all_registrations:
            record = {
                "StudentID" : t[0],
                "CourseID" : t[1] 
            }
            data.extend([record])
        json.dump(data, file, indent=4)

def file_not_found_popup():
    """
    Displays an error message in a pop-up window, stating that the file was not found

    :return: nothing
    :rtype: None
    """
    # Create a message box for the error
    error_message = QMessageBox()
    error_message.setIcon(QMessageBox.Critical)
    error_message.setWindowTitle("Error")
    error_message.setText("File not found!")
    error_message.setStandardButtons(QMessageBox.Ok)
    
    # Show the popup
    error_message.exec_()

def loadStudents():
    """
    inserts all entries in the students.json file into the Students table in the database
    displays a file not found error in case this file doesn't exist
    display an error popup in case of errors in inserting data into the database

    :return: Nothing.
    :rtype: None
    """
    try:
        with open("students.json", 'r') as file:
            data = json.load(file)
            for t in data:
                try:
                    cursor.execute("insert into Students values (?,?,?,?)", (t["student_id"],t["name"],t["age"],t["email"]))
                    conn.commit()
                except Exception as e:
                    show_error_popup()
                    print(e)
    except:
        file_not_found_popup()
        
def loadInstructors():
    """
    inserts all entries in the instructors.json file into the Instructors table in the database
    displays a file not found error in case this file doesn't exist
    display an error popup in case of errors in inserting data into the database

    :return: Nothing.
    :rtype: None
    """
    try:
        with open("instructors.json", 'r') as file:
            data = json.load(file)
            for t in data:
                try:
                    cursor.execute("insert into Instructors values (?,?,?,?)", (t["instructor_id"],t["name"],t["age"],t["email"]))
                    conn.commit()
                except:
                    show_error_popup()
                    pass   
    except:
        file_not_found_popup()
        

def loadCourses():
    """
    inserts all entries in the courses.json file into the Courses table in the database
    displays a file not found error in case this file doesn't exist
    display an error popup in case of errors in inserting data into the database

    :return: Nothing.
    :rtype: None
    """
    try:
        with open("courses.json", 'r') as file:
            data = json.load(file)
            for t in data:
                try:
                    cursor.execute("insert into Courses values (?,?,?)", (t["course_id"],t["course_name"],t["instructor_id"]))
                    conn.commit()
                except:
                    show_error_popup()
                    pass  
    except:
        file_not_found_popup()
            

def loadRegistrations():
    """
    inserts all entries in the registrations.json file into the Registrations table in the database
    displays a file not found error in case this file doesn't exist
    display an error popup in case of errors in inserting data into the database

    :return: Nothing.
    :rtype: None
    """
    try:
        with open("registrations.json", 'r') as file:
            data = json.load(file)
            for t in data:
                try:
                    cursor.execute("insert into Registrations values (?,?)", (t["StudentID"],t["CourseID"]))
                    conn.commit()
                except Exception as e:
                    show_error_popup()
                    print(e)
    except:
        file_not_found_popup()
        

def generate_csv():
    """
    generates a csv file containing all records in the tables in the database
    by exporting them to json first, then using these json files to populate the csv file.

    :return: Nothing.
    :rtype: None
    """
    student_file = 'students.json'
    instructor_file = 'instructors.json'
    course_file = 'courses.json'
    registrations_file = 'registrations.json'

    exportStudents()
    exportInstructors()
    exportCourses()
    exportRegistrations()

    # Load JSON data from each file
    with open(student_file, 'r') as f:
        students = json.load(f)

    with open(instructor_file, 'r') as f:
        instructors = json.load(f)

    with open(course_file, 'r') as f:
        courses = json.load(f)

    with open(registrations_file, 'r') as f:
        registrations = json.load(f)

    csv_file = 'merged_data.csv'


    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        

        writer.writerow(['ID / Student ID', 'Name / Course ID', 'Type', 'Age/Instructor ID', 'Email'])
        
        # Write student data to the CSV
        for student in students:
            writer.writerow([student['student_id'], student['name'], 'Student', student['age'], student['email']])

        # Write instructor data to the CSV
        for instructor in instructors:
            writer.writerow([instructor['instructor_id'], instructor['name'], 'Instructor', instructor['age'], instructor['email']])

        # Write course data to the CSV
        for course in courses:
            writer.writerow([course['course_id'], course['course_name'], 'Course', course['instructor_id'], 'N/A'])  # 'N/A' for email

        for r in registrations:
            writer.writerow([r['StudentID'], r['CourseID'], 'Registration', "N/A", 'N/A'])  # 'N/A' for email



export_import_layout = QFormLayout()
export_students = QPushButton('Export Students to JSON')
export_students.clicked.connect(exportStudents)
export_instructors = QPushButton('Export Instructors to JSON')
export_instructors.clicked.connect(exportInstructors)
export_courses = QPushButton('Export Courses to JSON')
export_courses.clicked.connect(exportCourses)
export_registrations = QPushButton('Export Registrations to JSON')
export_registrations.clicked.connect(exportRegistrations)

load_students = QPushButton('load Students from JSON')
load_students.clicked.connect(loadStudents)
load_instructors = QPushButton('load Instructors from JSON')
load_instructors.clicked.connect(loadInstructors)
load_courses = QPushButton('load Courses from JSON')
load_courses.clicked.connect(loadCourses)
load_registrations = QPushButton('load Registrations from JSON')
load_registrations.clicked.connect(loadRegistrations)

export_csv = QPushButton('Export to CSV')
export_csv.clicked.connect(generate_csv)

export_import_layout.addRow(export_students)
export_import_layout.addRow(export_instructors)
export_import_layout.addRow(export_courses)
export_import_layout.addRow(export_registrations)

export_import_layout.addRow(load_students)
export_import_layout.addRow(load_instructors)
export_import_layout.addRow(load_courses)
export_import_layout.addRow(load_registrations)
export_import_layout.addRow(export_csv)

export_tab.setLayout(export_import_layout)



if __name__ == '__main__':
    main()