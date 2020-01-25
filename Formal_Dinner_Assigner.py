import random
import math
import sys

####################
# GLOBAL CONSTANTS #
####################

OUTPUTFILE = "Dinner Assignments.csv"

WORK_TYPES = ("Kitchen_crew", "Waiter", "Diner")

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

    def __str__(self):
        return "%s, %s, W%s" % (self.super.lname, self.super.fname, self.super.table_number)

class Kitchen_crew:
    all = []

    def __init__(self, parent, number):
        self.super = parent
        parent.assigned = True
        parent.type_of_assignment = "Kitchen_crew"
        self.all.append(self)

    def __str__(self):
        return "%s, %s, Kitchen" % (self.super.lname, self.super.fname)

class Diner:
    all = []

    def __init__(self, parent, table_number):
        self.super = parent
        parent.assigned = True
        parent.table_number = table_number
        parent.type_of_assignment = "Diner"
        self.all.append(self)

    def __str__(self):
        return "%s, %s, %s" % (self.super.lname, self.super.fname, self.super.table_number)

class Student:
    all = []

    def __init__(self, lname, fname):
        self.lname = lname
        self.fname = fname
        self.all.append(self)
        self.assigned = False

    def __str__(self):
        if self.type_of_assignment == "Kitchen_crew":
            last_s = "Kitchen"
        elif self.type_of_assignment == "Waiter":
            last_s = "W %s" % (self.table_number)
        else:
            last_s = "%s" % (self.table_number)
        return "%s, %s, %s\n" % (self.lname, self.fname, last_s)

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

#function to write all students to a given output file using the format set-up for printing Students in the object definition
def write_all_of_a_class(cls, file):
    f = open(file, "w", newline="")
    for obj in cls.all:
        f.write(str(obj))
    f.close()

#function to get a class name given a string consisting of that class name
def str_to_class(classname):
    return globals()[classname]

#function to determine how many tables needed for the dinner given that tables hold a max of 8 people plus one waiter
#and also given that we'll need a certain number of students for kitchen staff
def calc_number_of_tables_needed():

    return math.ceil((len(Student.all) - NUMBER_IN_KITCHEN_STAFF) / (MAX_NUMBER_SITTING_AT_A_TABLE + NUMBER_OF_WAITERS_AT_A_TABLE))

def assign_work(*params): # work_type, work_force, number_needed, maybe table_number
    work_type = params[0]
    work_force = params[1]
    number_needed = params[2]
    unassigned = list(filter(lambda obj: obj.assigned == False, work_force))

    i = 1
    while i <= number_needed and len(unassigned) > 0:
        available_pool = len(unassigned)
        # choose a number at random from a set equal to the indecises of the list of available students
        rand = random.randint(0, (available_pool - 1))
        assignee = unassigned.pop(rand)

        #get the correct Class type using a string that matches the Class name
        cls = str_to_class(work_type)

        #assigning diners to tables is a special case because we need to create a Table object for the first diner, but
        #after that we only need to add the diner to the existing table
        if work_type != "Diner":
            cls(assignee, i)
        else:
            table_number = params[3]
            diner = Diner(assignee, table_number)
            if i == 1:  # this is the first diner for this table, so create a new Table object
                Table(table_number, diner)
            else:  # we have already created this table, so just add diner to existing table
                Table.all[table_number - 1].add_diner(diner, number_needed)
        i += 1

#################
# Main Body     #
#################

#read all students from a csv file and create a Student object for each one of them
read_students_file("sample_data.csv")

#determine how many tables we need given the capacity of each table and the total number
#of people that we need to seat for dinner
number_of_tables_needed = calc_number_of_tables_needed()

#I'm relying on a constant to pass the name of the work-types because they need to match my Class names for that work-type
assign_work(WORK_TYPES[0], Student.all, NUMBER_IN_KITCHEN_STAFF)
assign_work(WORK_TYPES[1], Student.all, number_of_tables_needed * NUMBER_OF_WAITERS_AT_A_TABLE)

#assign tables to the non-workers,
for x in range(number_of_tables_needed):
    assign_work(WORK_TYPES[2], Student.all, MAX_NUMBER_SITTING_AT_A_TABLE, x)

#print status of each student to an output file
write_all_of_a_class(Student, OUTPUTFILE)
