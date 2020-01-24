import random
import math

####################
# GLOBAL CONSTANTS #
####################

OUTPUTFILE = "Dinner Assignments.csv"

#number of students that won't be sitting at a table or waiting on a table b/c they will be in the kitchen
NUMBER_IN_KITCHEN_STAFF = 8

#how many people does a dining table hold
MAX_NUMBER_SITTING_AT_A_TABLE = 8

#how many waiters per each table
NUMBER_OF_WAITERS_AT_A_TABLE = 1

######################
# Object Definitions #
######################

class Waiter:
    all = []

    def __init__(self, parent, table_number):
        self.super = parent
        parent.assigned = True
        parent.type_of_assignment = "Waiter"
        parent.table_number = table_number
        self.all.append(self)

    @classmethod
    def get_wait_staff(cls, potentials, number_needed):
        i = 1
        while i <= number_needed:
            available_pool = len(potentials)
            # choose a number at random from a set equal to the indecises of the list of available students
            rand = random.randint(0, (available_pool - 1))
            Waiter(potentials[rand], i)
            del potentials[rand]
            i += 1

class Kitchen_crew:
    all = []

    def __init__(self, parent):
        self.super = parent
        parent.assigned = True
        parent.type_of_assignment = "Kitchen_crew"
        self.all.append(self)

    @classmethod
    def get_kitchen_staff(cls, potentials, number_needed):
        i = 1
        while i <= number_needed:
            available_pool = len(potentials)
            # choose a number at random from a set equal to the indecises of the list of available students
            rand = random.randint(0, (available_pool - 1))
            Kitchen_crew(potentials[rand])
            del potentials[rand]  #remove this student so that we don't double assign him to this task
            i += 1

class Diner:
    all = []

    def __init__(self, parent, table_number):
        self.super = parent
        parent.assigned = True
        parent.table_number = table_number
        parent.type_of_assignment = "Diner"
        self.all.append(self)

class Student:
    all = []

    def __init__(self, lname, fname):
        self.lname = lname
        self.fname = fname
        self.all.append(self)
        self.assigned = False

    @classmethod
    def write_all_students(cls, file):
        f = open(file, "w", newline="")
        for student in cls.all:
            s = student.lname + "," + student.fname + ","
            if student.type_of_assignment == "Kitchen_crew":  # student has kitchen duty so is not assigned a table
                f.write(s + "kitchen\n")
            else:
                if student.type_of_assignment == "Waiter":  # student is the waiter for a specific table
                    s += "W {}\n"
                else:  # student is a diner
                    s += "{}\n"
                f.write(s.format(student.table_number))
        f.close()

class Table:
    all = []

    def __init__(self, number, diner):
        self.number = number
        self.all.append(self)
        self.full = False
        self.diners = [diner]

    def add_diner(self, diner, number_needed):
        self.diners.append(diner)
        diner.table = self
        if len(self.diners) == number_needed:
            self.full = True

    @classmethod
    def fill_out_table(cls, potentials, table_number, number_needed):
        i = 1
        while i <= number_needed and len(potentials) > 0:
            available_pool = len(potentials)
            # choose a number at random from a set equal to the indecises of the list of available students
            rand = random.randint(0, (available_pool - 1))
            table_sitter = Diner(potentials[rand], table_number)
            #add this diner to this table
            if i == 1:  # this is the first diner for this table, so create a new Table object
                Table(table_number, table_sitter)
            else:  # we have already created this table, so just add diner to existing table
                Table.all[table_number - 1].add_diner(table_sitter, number_needed)

            del potentials[rand]  #remove this student so that we don't double assign him to this table
            i += 1

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

#function to determine how many tables needed for the dinner given that tables hold a max of 8 people plus one waiter
#and also given that we'll need a certain number of students for kitchen staff
def calc_number_of_tables_needed():

    return math.ceil((len(Student.all) - NUMBER_IN_KITCHEN_STAFF) / (MAX_NUMBER_SITTING_AT_A_TABLE + NUMBER_OF_WAITERS_AT_A_TABLE))

#################
# Main Body     #
#################

#read all students from a csv file and create a Student object for each one of them
read_students_file("sample_data.csv")

#determine how many tables we need given the capacity of each table and the total number
#of people that we need to seat for dinner
number_of_tables_needed = calc_number_of_tables_needed()

#keep track of all students that haven't already been assigned a task/dining table
unassigned = Student.all.copy()

#create waiters for all of the tables
Waiter.get_wait_staff(unassigned, number_of_tables_needed)
unassigned = list(filter(lambda student: student.assigned == False, unassigned))

#create kitchen crew from all students except those who are already assigned to wait tables
Kitchen_crew.get_kitchen_staff(unassigned, NUMBER_IN_KITCHEN_STAFF)
unassigned = list(filter(lambda student: student.assigned == False, unassigned))

#assign tables for all remaining students
for x in range(number_of_tables_needed):
    Table.fill_out_table(unassigned, x + 1, MAX_NUMBER_SITTING_AT_A_TABLE)

#print status of each student to an output file
Student.write_all_students(OUTPUTFILE)
