from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date
from sqlalchemy.orm import relationship

from DB.database import db


student_course_association = Table(
    'student_course', db.Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)

class Person(db.Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    password = Column(String(250), nullable=False)
    
    
class StudentModel(Person):
    __tablename__ = 'students' 
    major = Column(String(50))

    courses = relationship('CourseModel', secondary=student_course_association, back_populates='students')

class TeacherModel(Person):
    __tablename__ = 'teachers'

    courses = relationship('CourseModel', back_populates='teacher', cascade="all, delete-orphan")

class CourseModel(db.Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True,nullable=False)
    start = Column(Date, index=True)
    end = Column(Date, index=True)
    
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    class_id = Column(Integer, ForeignKey('classes.id'))

    students = relationship('StudentModel', secondary=student_course_association, back_populates='courses')
    teacher = relationship('TeacherModel', back_populates='courses')
    classes = relationship('ClassModel', back_populates='course')

class ClassModel(db.Base):
    __tablename__ = 'classes'    
    id = Column(Integer, primary_key=True, index=True)

    course = relationship('CourseModel', back_populates='classes', cascade="all, delete-orphan")
