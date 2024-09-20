
from abc import ABC, abstractmethod
import re
import json

def can_be_int(s):
    try:
        int(s)  # Try to convert the string to an integer
        return True
    except ValueError:
        return False
    
class Person(ABC):
    def __init__(self, name, age, email):
        assert can_be_int(age) and int(age) > 0
        assert re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email), "Email address is not in the correct format"
        assert name != ""
        self.name = name
        self.age = age
        self.__email = email

    @abstractmethod
    def introduce(self):
        pass
    
    def get_email(self):
        return self.__email
    
    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'email': self.get_email()
        }
    
class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []
    def introduce(self):
        return f"I am a student, my name is {self.name}, I am {self.age} years old. These are the courses that I am taking: \n {self.registered_courses}"
    def register_course(self, course):
        self.registered_courses.append(course)
        course.add_student(self)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'student_id': self.student_id,
        })
        return data

    def save_to_json(self):
        # read existing data from the file
        try:
            with open('students.json', 'r') as file:
                existing_data = json.load(file)
        except Exception as e:
            existing_data = []
        
        # append new student data to the existing data
        existing_data.extend([self.to_dict()])

        with open('students.json', 'w') as file:
            json.dump(existing_data, file, indent=4)

    @staticmethod
    def load_from_json():
        with open('students.json', 'r') as file:
            students_data = json.load(file)
            students = []
            for data in students_data:
                student = Student(data['name'], data['age'], data['email'], data['student_id'])
                student.registered_courses = [Course.from_dict(course) for course in data['registered_courses']]
                students.append(student)
            return students

class Instructor(Person):
    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []
    
    def introduce(self):
        return f"I am an instructor, my name is {self.name}, I am {self.age} years old. These are the courses that I am teaching: \n {self.assigned_courses}"
    
    def assign_course(self, course):
        self.assigned_courses.append(course)
        course.instructor = self

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'instructor_id': self.instructor_id,
            'assigned_courses': [course.to_dict() for course in self.assigned_courses]
        })
        return data
    
    def save_to_json(self):
        try:
            with open('instructors.json', 'r') as file:
                existing_data = json.load(file)
        except Exception as e:
            existing_data = []

        existing_data.extend([self.to_dict()])

        with open('instructors.json', 'w') as file:
            json.dump(existing_data, file, indent=4)

    @staticmethod
    def load_from_json():
            with open('instructors.json', 'r') as file:
                instructors_data = json.load(file)
                instructors = []
                for data in instructors_data:
                    instructor = Instructor(data['name'], data['age'], data['email'], data['instructor_id'])
                    instructor.assigned_courses = [Course(**course) for course in data['assigned_courses']]
                    instructors.append(instructor)
                return instructors

class Course:
    def __init__(self, course_id, course_name):
        assert course_name != ""
        self.course_id = course_id
        self.course_name = course_name
        self.enrolled_students = []
        self.instructor_id = None
    
    def add_student(self, student):
        self.enrolled_students.append(student)

    def to_dict(self):
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'instructor_id': self.instructor_id
        }

    def from_dict(data):

        course = Course(data['course_id'], data['course_name'])
        course.instructor_id = data['instructor_id']

        return course

    def save_to_json(self):
        try:
            with open('courses.json', 'r') as file:
                existing_data = json.load(file)
        except Exception as e:
            existing_data = []

        existing_data.extend([self.to_dict()])

        with open('courses.json', 'w') as file:
            json.dump(existing_data, file, indent=4)

    @staticmethod
    def load_from_json():
            with open('courses.json', 'r') as file:
                courses_data = json.load(file)
                courses = []
                for data in courses_data:
                    course = Course(data['course_id'], data['course_name'])
                    course.instructor_id = data['instructor_id']
                    courses.append(course)
                return courses