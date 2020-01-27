import random
import math

####################
# GLOBAL CONSTANTS #
####################

INPUT_FILE = "sample_data.csv"

OUTPUT_FILE = "Dinner Assignments.csv"

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

class Person(object):

    def __init__(self, lname, fname):
        self.lname = lname
        self.fname = fname

class Attendant(Person):

    def __init__(self, lname, fname):
        super().__init__(lname, fname)
        self.assigned = False
        self.assignable = True

class Student(Attendant):

    all = []

    def __init__(self, lname, fname):
        super().__init__(lname, fname)
        self.all.append(self)

    def __str__(self):
        if self.type_of_assignment == "Kitchen_crew":
            last_s = "Kitchen"
        elif self.type_of_assignment == "Waiter":
            last_s = "W %s" % (self.waiter.table.number)
        else:
            last_s = "%s" % (self.diner.table.number)
        return "%s, %s, %s\n" % (self.lname, self.fname, last_s)

class Waiter():
    all = []

    def __init__(self, parent, table_number):
        self.super = parent
        parent.assigned = True
        parent.waiter = self
        parent.type_of_assignment = "Waiter"
        self.all.append(self)

    def __str__(self):
        return "%s, %s, W%s" % (self.super.lname, self.super.fname, self.table.number)

class Kitchen_crew(Student):
    all = []

    def __init__(self, parent, number):
        self.super = parent
        parent.assigned = True
        parent.type_of_assignment = "Kitchen_crew"
        self.all.append(self)

    def __str__(self):
        return "%s, %s, Kitchen" % (self.super.lname, self.super.fname)

class Diner(Student):
    all = []

    def __init__(self, parent, table_number):
        self.super = parent
        parent.assigned = True
        parent.diner = self
        parent.type_of_assignment = "Diner"
        self.all.append(self)

    def __str__(self):
        return "%s, %s, %s" % (self.super.lname, self.super.fname, self.table.number)

class Table:
    all = []

    def __init__(self, number):
        self.number = number
        self.all.append(self)
        self.full = False
        self.diners = []
        self.waiters = []

    def add_diner(self, diner, number_needed):
        self.diners.append(diner)
        diner.table = self
        if len(self.diners) == number_needed:
            self.full = True

    def add_waiter(self, waiter):
        self.waiters.append(waiter)
        waiter.table = self

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

#Takes in the type of work, the class representing the workers (e.g., Student, but in the future maybe also Teacher)
# and the number of that class needed to perform the work.
def assign_work(work_type, work_force, number_needed):

    #get a list of Student objects that aren't already assigned to other work
    unassigned = list(filter(lambda obj: obj.assigned == False and obj.assignable == True, work_force))

    i = 1
    while i <= number_needed and len(unassigned) > 0: #assign the number_needed

        # choose a number at random from the list of available students
        available_pool = len(unassigned)
        rand = random.randint(0, (available_pool - 1))

        # remove assignee from the unassigned list so that we don't double assign the object
        assignee = unassigned.pop(rand)

        #get the correct Class-type using a string that matches the Class name
        cls = str_to_class(work_type)

        worker = cls(assignee, i) #create the correct type of worker object
        if work_type == "Waiter": #if the worker is a waiter add them to the correct table_number
            table = worker.table= Table(i)
            table.add_waiter(worker)

        i += 1

def assign_dinner_tables(number_of_tables_needed):

    # get a list of the attendants who do not have a work assignment
    needing_a_table = list(filter(lambda obj: obj.assigned == False, Student.all))

    for table_number in range(1, number_of_tables_needed + 1):

        for table_position in range(1, MAX_NUMBER_SITTING_AT_A_TABLE + 1):

            #handle the case where we don't have enough students to fill the last table
            if len(needing_a_table) <1:
                break

            # an index for a diner chosen at random
            rand = random.randint(0, (len(needing_a_table) - 1))
            diner = needing_a_table.pop(rand)
            diner = Diner(diner, table_number)
            table = Table.all[table_number - 1] #note, the Table obj was created when we assigned waiters
            table.add_diner(diner, MAX_NUMBER_SITTING_AT_A_TABLE)

#################
# Main Body     #
#################

#read all students from a csv file and create a Student object for each one of them
read_students_file(INPUT_FILE)

#determine how many tables we need given the capacity of each table and the total number
#of people that we need to seat for dinner
number_of_tables_needed = calc_number_of_tables_needed()

#I'm relying on a constant to pass the name of the work-types because they need to match my Class names for that work-type
assign_work(WORK_TYPES[0], Student.all, NUMBER_IN_KITCHEN_STAFF)
assign_work(WORK_TYPES[1], Student.all, number_of_tables_needed * NUMBER_OF_WAITERS_AT_A_TABLE)

#assign the non-workers to a dinner table
assign_dinner_tables(number_of_tables_needed)

#print status of each student to an output file
write_all_of_a_class(Student, OUTPUT_FILE)
