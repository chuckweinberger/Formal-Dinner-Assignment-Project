import random
import math
##################
# Global variables
##################

# list of students who don't have work assignments
free_students = []

#list for all tables, will contain a dict of all Students who are sitting at the table.  Table number = index of that table in the array plus 1
table_assignments = []

#number of students that won't be sitting at a table or waiting on a table b/c they will be in the kitchen
number_in_kitchen_staff = 8

#how many people does a dining table hold
number_sitting_at_a_table = 8

#how many waiters per each table
number_of_waiters_at_a_table = 1

# Object definitions
class Student:
    all = []

    def __init__(self, lname, fname):
        self.lname = lname
        self.fname = fname
        # self.table = None
        # self.waiting = None
        # self.kitchen_staff = None
        self.assignment = { "kitchen_staff": False, "wait_staff": False, "table_assignment": False, "table": int }
        self.all.append(self)

class Table:
    all = []

    def __init__(self, number):
        self.number =number
        self.all.append(self)

#############################
# local function defintions #
#############################

#function to open a .cvs file, read each line, which contains student attributes, and create a student for each line of attributes
def read_students_file(file_name):
    # open the cvs file that holds students, one student per row
    f = open("Dinner Seating - Student List 2018-19 4.csv")
    lines = (f.read())
    f.close()

    # turn a multi-line string in which each line contains data on an individual student into Student objects
    for line in lines.splitlines():
        student_attributes = line.split(",")
        Student(lname=student_attributes[0], fname=student_attributes[1])

#function to take in a list of Student objects and print them to a .csf vile by lastname, firstname, and assignment
def write_student_list():
    f = open("Dinner Assignments.csv", "w", newline="")
    for student in Student.all:
        s = student.lname + "," + student.fname + ","
        if student.assignment["kitchen_staff"] == True:     #student has kitchen duty so is not assigned a table
            f.write(s + "kitchen\n")
        else:
            if student.assignment["wait_staff"]  == True:   #student is the waiter for a specific table
                s += "W {}\n"
            else:                                           #student is sitting at a table
                s += "{}\n"
            f.write(s.format(student.assignment["table"]))
    f.close()

#function to determine how many tables needed for the dinner given that tables hold a max of 8 people plus one waiter
#and also given that we'll need a certain number of students for kitchen staff
def calc_number_of_tables_needed():

    return math.ceil((len(Student.all) - number_in_kitchen_staff) / (number_sitting_at_a_table + number_of_waiters_at_a_table))

# function for assigning a specific number of students at random to a given task
def choose_random_individuals_for_something(work_name, number_needed, table_number = None):
    #make sure that any changes to the global list of free_students is retained in the global scope
    global free_students
    the_chosen = []
    number_to_chose_from = len(free_students)
    while 0 < number_needed and free_students:
        #choose a number at random from a set equal to the indecises of the list of available students
        rand = random.randint(0,(number_to_chose_from - 1))
        free_students[rand].assignment[work_name] = True
        #if we are assigning tables to diners, make sure to keep track of the diner's table number
        if (work_name == "table_assignment"):
            free_students[rand].assignment["table"] = table_number
        the_chosen.append(free_students[rand])
        del free_students[rand]
        number_to_chose_from -= 1
        number_needed -= 1
    return the_chosen

#read all students from a csv file and create a Student object for each one of them
read_students_file("sample_data.csv")

#keep track of students that don't have jobs so that we don't give someone two jobs, and that we seat only those who don't have jobs
free_students = Student.all.copy()

number_of_tables_needed = calc_number_of_tables_needed()
waiters_list = choose_random_individuals_for_something("wait_staff", number_of_tables_needed)
kitchen_list = choose_random_individuals_for_something("kitchen_staff", number_in_kitchen_staff)

# iterate through the tables selecting students at random to sit at each table and to wait for each table
for i in range(1, (number_of_tables_needed + 1)):
    # get the students for the current table
    table_assignments.append(choose_random_individuals_for_something("table_assignment", number_sitting_at_a_table, i))
    # assign the waiter for the current table out of the list of already assigned waiters
    waiter = waiters_list[i-1]
    waiter.assignment["table"] = i
    table_assignments[i-1].append(waiter)

write_student_list()