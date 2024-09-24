import re
import json
import tkinter as tk
from tkinter import ttk


class SchoolManagementSystem:
    """
    A class used to represent the School Management System.

    Methods
    -------
    save_data(filename, data)
        Saves the given data to the specified JSON file.

    save_data_dump(filename, data)
        Dumps the given data directly into the specified JSON file.
    """

    @staticmethod
    def save_data(filename, data):
        """
        Save the given data to a JSON file.

        If the file exists, it loads the existing data and appends new data. Otherwise, it creates a new file.

        :param filename: The name of the file to save the data to.
        :type filename: str
        :param data: The data to be saved.
        :type data: list
        """
        try:
            with open(filename, 'r') as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        json_data = [obj.__dict__ for obj in data]
        existing_data.extend(json_data)

        with open(filename, 'w') as file:
            json.dump(existing_data, file, indent=4)

    @staticmethod
    def save_data_dump(filename, data):
        """
        Dump the given data into a JSON file, overwriting the existing file.

        :param filename: The name of the file to dump the data into.
        :type filename: str
        :param data: The data to be saved.
        :type data: dict or list
        """
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)


class Person:
    """
    A class to represent a Person.

    Attributes
    ----------
    name : str
        The name of the person.
    age : int
        The age of the person.
    email : str
        The email of the person.

    Methods
    -------
    validate_email(email)
        Validates the email format using a regex pattern.

    introduce()
        Prints an introduction of the person.
    """

    def __init__(self, name, age, email):
        """
        Constructs the necessary attributes for the Person object.

        :param name: The name of the person.
        :type name: str
        :param age: The age of the person. Must be positive.
        :type age: int
        :param email: The email address of the person.
        :type email: str
        """
        self.name = name
        if age <= 0:
            raise ValueError("age is negative!")
        else:
            self.age = age
        self._email = Person.validate_email(email)  # Validate email format

    @staticmethod
    def validate_email(email):
        """
        Validate the format of the email using a regex pattern.

        :param email: The email to be validated.
        :type email: str
        :return: The validated email.
        :rtype: str
        :raises ValueError: If the email format is invalid.
        """
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if re.match(email_regex, email):
            return email
        else:
            raise ValueError("Invalid email format")

    def introduce(self):
        """
        Prints an introduction that includes the person's name and age.

        :return: None
        """
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")


class Course:
    """
    A class to represent a Course.

    Attributes
    ----------
    course_id : str
        The ID of the course.
    course_name : str
        The name of the course.
    instructor : Instructor, optional
        The instructor assigned to the course. Default is None.
    enrolled_students : list
        A list of enrolled students.

    Methods
    -------
    add_student(student)
        Adds a student to the course's enrolled students list.
    """

    def __init__(self, course_id, course_name, instructor=None):
        """
        Constructs the necessary attributes for the Course object.

        :param course_id: The ID of the course.
        :type course_id: str
        :param course_name: The name of the course.
        :type course_name: str
        :param instructor: The instructor assigned to the course.
        :type instructor: Instructor or None
        """
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []  # List to hold enrolled Student objects

    def add_student(self, student):
        """
        Adds a student to the course's enrolled students list.

        :param student: The student to be added.
        :type student: Student
        """
        self.enrolled_students.append(student)


class RegCourse:
    """
    A class to represent a registered course for a student.

    Attributes
    ----------
    student_id : str
        The ID of the student.
    course_name : str
        The name of the registered course.
    """

    def __init__(self, student_id, course_name):
        """
        Constructs the necessary attributes for the RegCourse object.

        :param student_id: The ID of the student.
        :type student_id: str
        :param course_name: The name of the registered course.
        :type course_name: str
        """
        self.student_id = student_id
        self.course_name = course_name


class AssCourse:
    """
    A class to represent an assigned course for an instructor.

    Attributes
    ----------
    instructor_id : str
        The ID of the instructor.
    course_name : str
        The name of the assigned course.
    """

    def __init__(self, instructor_id, course_name):
        """
        Constructs the necessary attributes for the AssCourse object.

        :param instructor_id: The ID of the instructor.
        :type instructor_id: str
        :param course_name: The name of the assigned course.
        :type course_name: str
        """
        self.instructor_id = instructor_id
        self.course_name = course_name


class Student(Person):
    """
    A class to represent a Student, inherits from Person.

    Attributes
    ----------
    student_id : str
        The ID of the student.
    registered_courses : list
        A list of registered courses.

    Methods
    -------
    register_course(course)
        Adds a course to the student's registered courses list.
    """

    def __init__(self, name, age, email, student_id):
        """
        Constructs the necessary attributes for the Student object.

        :param name: The name of the student.
        :type name: str
        :param age: The age of the student.
        :type age: int
        :param email: The email of the student.
        :type email: str
        :param student_id: The ID of the student.
        :type student_id: str
        """
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []  # List to hold registered Course objects

    def register_course(self, course):
        """
        Registers a course for the student.

        :param course: The course to be registered.
        :type course: Course
        """
        self.registered_courses.append(course)

class Instructor(Person):
    """
    A class to represent an Instructor, inherits from Person.

    Attributes
    ----------
    instructor_id : str
        The ID of the instructor.
    assigned_courses : list
        A list of assigned courses.

    Methods
    -------
    assign_course(course)
        Adds a course to the instructor's assigned courses list.
    """

    def __init__(self, name, age, email, instructor_id):
        """
        Constructs the necessary attributes for the Instructor object.

        :param name: The name of the instructor.
        :type name: str
        :param age: The age of the instructor.
        :type age: int
        :param email: The email of the instructor.
        :type email: str
        :param instructor_id: The ID of the instructor.
        :type instructor_id: str
        """
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []  # List to hold assigned Course objects

    def assign_course(self, course):
        """
        Assigns a course to the instructor.

        :param course: The course to be assigned.
        :type course: Course
        """
        self.assigned_courses.append(course)



# Create the main window
root = tk.Tk()
root.title("School Management System")
root.geometry("400x400")


main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


second_frame = tk.Frame(canvas)

canvas.create_window((0, 0), window=second_frame, anchor="nw")

title_label = tk.Label(second_frame, text="Add Student, Instructor, or Course", font=("Arial", 14))
title_label.pack(pady=10)


def add_student():
    """
    Retrieves the student information from the entry fields,
    creates a `Student` object, and saves it to a JSON file.

    :return: None
    """
    name = student_name_entry.get()
    age = int(student_age_entry.get())
    email = student_email_entry.get()
    student_id = student_id_entry.get()

    stdnt = Student(name, age, email, student_id)
    SchoolManagementSystem.save_data("students.json", [stdnt])


# Labels and Entry fields for Student Form
student_label = tk.Label(second_frame, text="Add Student")
student_label.pack()

student_name_label = tk.Label(second_frame, text="Name")
student_name_label.pack()
student_name_entry = tk.Entry(second_frame)
student_name_entry.pack()

student_age_label = tk.Label(second_frame, text="Age")
student_age_label.pack()
student_age_entry = tk.Entry(second_frame)
student_age_entry.pack()

student_email_label = tk.Label(second_frame, text="Email")
student_email_label.pack()
student_email_entry = tk.Entry(second_frame)
student_email_entry.pack()

student_id_label = tk.Label(second_frame, text="Student ID")
student_id_label.pack()
student_id_entry = tk.Entry(second_frame)
student_id_entry.pack()

add_student_button = tk.Button(second_frame, text="Add Student", command=add_student)
add_student_button.pack(pady=10)

def load_json(filename):
    """
    Loads and returns data from the given JSON file.

    :param filename: The name of the file to load data from.
    :type filename: str
    :return: The loaded data.
    :rtype: dict or list
    """
    with open(filename, 'r') as file:
        return json.load(file)


def add_instructor():
    """
    Retrieves the instructor information from the entry fields,
    creates an `Instructor` object, and saves it to a JSON file.

    :return: None
    """
    name = instructor_name_entry.get()
    age = int(instructor_age_entry.get())
    email = instructor_email_entry.get()
    instructor_id = instructor_id_entry.get()

    inst = Instructor(name, age, email, instructor_id)
    SchoolManagementSystem.save_data("instructors.json", [inst])


instructor_label = tk.Label(second_frame, text="Add Instructor")
instructor_label.pack()

instructor_name_label = tk.Label(second_frame, text="Name")
instructor_name_label.pack()
instructor_name_entry = tk.Entry(second_frame)
instructor_name_entry.pack()

instructor_age_label = tk.Label(second_frame, text="Age")
instructor_age_label.pack()
instructor_age_entry = tk.Entry(second_frame)
instructor_age_entry.pack()

instructor_email_label = tk.Label(second_frame, text="Email")
instructor_email_label.pack()
instructor_email_entry = tk.Entry(second_frame)
instructor_email_entry.pack()

instructor_id_label = tk.Label(second_frame, text="Instructor ID")
instructor_id_label.pack()
instructor_id_entry = tk.Entry(second_frame)
instructor_id_entry.pack()

add_instructor_button = tk.Button(second_frame, text="Add Instructor", command=add_instructor)
add_instructor_button.pack(pady=10)



def add_course():
    """
    Retrieves the course information from the entry fields,
    creates a `Course` object, and saves it to a JSON file.

    :return: None
    """
    course_id = course_id_entry.get()
    course_name = course_name_entry.get()

    crs = Course(course_id, course_name)
    SchoolManagementSystem.save_data("Courses.json", [crs])
    refreshCourses()


course_label = tk.Label(second_frame, text="Add Course")
course_label.pack()

course_id_label = tk.Label(second_frame, text="Course ID")
course_id_label.pack()
course_id_entry = tk.Entry(second_frame)
course_id_entry.pack()

course_name_label = tk.Label(second_frame, text="Course Name")
course_name_label.pack()
course_name_entry = tk.Entry(second_frame)
course_name_entry.pack()


add_course_button = tk.Button(second_frame, text="Add Course", command=add_course)
add_course_button.pack(pady=10)





available_courses = ["None"]


def update_option_menu():
    """
    Updates the available course selection in the dropdown menus.

    :return: None
    """
    global course_dropdown
    global course_dropdown1
    menu = course_dropdown["menu"]
    menu1 = course_dropdown1["menu"]

    menu1.delete(0, "end")
    for course in available_courses:
        menu.add_command(label=course, command=tk._setit(selected_course_var, course))
        menu1.add_command(label=course, command=tk._setit(selected_course_var1, course))




def refreshCourses():
    """
    Loads the courses from a JSON file, updates the available courses list, and refreshes the dropdown menu.

    :return: None
    """
    with open("Courses.json", "r") as file:
        courses = json.load(file)

        global available_courses
        available_courses = []

        for obj in courses:
            available_courses.append(obj["course_name"])

    update_option_menu()


def addCourseToStudent(regcc):
    """
    Adds a registered course to a student's registered courses list.

    :param regcc: The registered course object.
    :type regcc: RegCourse
    :return: None
    """
    students = load_json("students.json")

    for obj in students:
        if obj["student_id"] == regcc.student_id:
            obj["registered_courses"].append(regcc.course_name)

    SchoolManagementSystem.save_data_dump("students.json", students)

def addCourseToInstructor(ass_course):
    """
    Adds an assigned course to an instructor's assigned courses list.

    :param ass_course: The assigned course object.
    :type ass_course: AssCourse
    :return: None
    """
    instructors = load_json("instructors.json")

    for obj in instructors:
        if obj["instructor_id"] == ass_course.instructor_id:
            obj["assigned_courses"].append(ass_course.course_name)

    SchoolManagementSystem.save_data_dump("instructors.json", instructors)



def register_course():
    """
    Registers a course for a student and updates the student's data in the JSON file.

    :return: None
    """
    student_id = student_id_entry1.get()
    selected_course = selected_course_var.get()

    regcc = RegCourse(student_id, selected_course)
    addCourseToStudent(regcc)

    SchoolManagementSystem.save_data("RegCourses.json", [regcc])


title_label = tk.Label(second_frame, text="Course Registration", font=("Arial", 14))
title_label.pack(pady=10)

student_id_label = tk.Label(second_frame, text="Student ID")
student_id_label.pack()
student_id_entry1 = tk.Entry(second_frame)
student_id_entry1.pack()

selected_course_var = tk.StringVar(second_frame)
selected_course_var.set(available_courses[0])  # Set default value

course_dropdown_label = tk.Label(second_frame, text="Select Course")
course_dropdown_label.pack()

course_dropdown = tk.OptionMenu(second_frame, selected_course_var, *available_courses)
course_dropdown.pack()

register_button = tk.Button(second_frame, text="Register", command=register_course)
register_button.pack(pady=10)


def assign_course():
    """
    Assigns a course to an instructor and updates the instructor's data in the JSON file.

    :return: None
    """
    instructor_id = instructor_id_entry1.get()
    selected_course = selected_course_var1.get()

    ass_course = AssCourse(instructor_id, selected_course)
    addCourseToInstructor(ass_course)

    SchoolManagementSystem.save_data("AssignedCourses.json", [ass_course])


def display_data():
    """
    Displays data about students and instructors in the tree view widget.

    :return: None
    """
    for item in treeview.get_children():
        treeview.delete(item)

    students = load_json("students.json")
    instructors = load_json("instructors.json")

    for obj in students:
        treeview.insert("", 'end', values=(obj["name"], "Student", obj["registered_courses"]))

    for obj in instructors:
        treeview.insert("", 'end', values=(obj["name"], "Instructor", obj["assigned_courses"]))



title_label = tk.Label(second_frame, text="Assign Instructor to Course", font=("Arial", 14))
title_label.pack(pady=10)

instructor_id_label = tk.Label(second_frame, text="Instructor ID")
instructor_id_label.pack()
instructor_id_entry1 = tk.Entry(second_frame)
instructor_id_entry1.pack()

selected_course_var1 = tk.StringVar(second_frame)
selected_course_var1.set(available_courses[0])  # Set default value

course_dropdown_label1 = tk.Label(second_frame, text="Select da Course")
course_dropdown_label1.pack()

course_dropdown1 = tk.OptionMenu(second_frame, selected_course_var1, *available_courses)
course_dropdown1.pack()

assign_button = tk.Button(second_frame, text="Assign Course", command=assign_course)
assign_button.pack(pady=10)


treeview = ttk.Treeview(second_frame, columns=("Name", "Type", "Info"), show="headings")
treeview.heading("Name", text="Name")
treeview.heading("Type", text="Type")
treeview.heading("Info", text="Additional Info")
treeview.pack(fill="both", expand=True)

display_button = tk.Button(second_frame, text="Display Data", command=display_data)
display_button.pack(side="bottom")



root.mainloop()

