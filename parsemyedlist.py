#!/usr/bin/python3.7
import csv

class Teacher():

    def __init__(self, name):
        self.name = name
        self.students = {}

    def __str__(self):
        return self.name

    def __eq__(self, item):
        if isinstance(item, Teacher):
            return self.name == item.name
        elif isinstance(item, str):
            return self.name == item
        else:
            return NotImplemented


def parse_myed_export(csv_file_name):

    teachers = []
    current_teach = None

    with open(csv_file_name, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:

            if "Teacher" in row:
                teacher_name = row[3]
                # print(teacher_name)
                if teacher_name in teachers:
                    current_teach = next(t for t in teachers if t.name == teacher_name)
                else:
                    # need to create new teacher
                    current_teach = Teacher(teacher_name)
                    teachers.append(current_teach)

            elif "Schedule" in row:
                current_block = row[3]
                # print(current_block)

            elif row[0]:  # not empty, the it's a student
                student = row[0]

                if current_block not in current_teach.students:
                    current_teach.students[current_block] = []
                
                current_teach.students[current_block].append(student)
        
    # for teach in teachers:
    #     print(teach)
    #     for block, student_list in teach.students.items():
    #         print(block)
    #         for s in student_list:
    #             print("\t", s)

    return teachers


def save_new_csv(teachers):
    with open('classlists.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(['TEACHER', 'BLOCK', 'STUDENT'])
        for t in teachers:
            for block, students in t.students.items():
                if block[:2] == "01":  # A block in the form of "01[....]"
                    for s in students:
                        spamwriter.writerow([t.name, block, s])


teachers = parse_myed_export("Timberline Class List by Teacher.csv")

save_new_csv(teachers)
