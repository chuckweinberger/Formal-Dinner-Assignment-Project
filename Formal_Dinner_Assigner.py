import random
import math

####################
# GLOBAL CONSTANTS #
####################

INPUT_FILE = "Dinner Seating - Student List 2018-19 4.csv"

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

class Attendant():

    all_attendants = []
    def __init__(self, lname, fname, last_weeks_assignment = None):
        self.lname = lname
        self.fname = fname
        self.assigned = False #no one has an assigned job on initial creation
        self.assignable = True #for future use if we have attendants who are excluded from work
        self.type_of_assignment = None
        self.attendant_type = None #for future use in case we add different types of attendants, like faculty, parents, etc.
        self.table = None
        self.blacklist = [] #holds a list of all Attendant instances with whom this instance should not be seated
        self.all_attendants.append(self)

        #we want to keep track of table assignments from last week so that we can create a black-list of people with whom
        #this attendant shouldn't sit at the coming diner.  Black-lists are only needed for people who dined last week

        if last_weeks_assignment == "Kitchen":
            self.last_weeks_assignment = "Kitchen"
        elif last_weeks_assignment[0] == "W":
            self.last_weeks_assignment = "Waiter"
        else:
            self.last_weeks_assignment = "Diner"

            #Look-up the table where this instance sat last week.
            #We need to keep track of everyone who sat at each of the tables for last week's dinner so that we can create a black-list for each attendant.
            #First, see if we've already created a Table instance for the table at which this attendant sat last week
            last_weeks_table_number = int(last_weeks_assignment)
            if last_weeks_table_number in Table.all_tables.keys(): #the needed instance of Last_weeks_tables has already been created
                lwt = Table.all_tables[last_weeks_table_number]
                lwt.add_diner(self)
            else:  #we haven't yet created this instance of Last_weeks_table.  So, create it
                lwt = Table(last_weeks_table_number, self) #diner will be added to the list of diners at this table as part of the creation process

    def __str__(self):
        if self.type_of_assignment == "Kitchen_crew":
            last_s = "Kitchen"
        elif self.type_of_assignment == "Waiter":
            last_s = "W %s" % (self.waiter.table.number)
        else:
            last_s = "%s" % (self.table.number)
        return "%s, %s, %s\n" % (self.lname, self.fname, last_s)

    #class method that traverses all instances of the class and creates a blacklist for each such instance.
    #the blacklist contains all of the diners with whom this instance ate with in the previous dinner so that we
    #can make sure that this instance doesn't eat with any of the same diners two times in a row
    @classmethod
    def create_blacklists(cls):
        for attendant in cls.all_attendants:
            if attendant.last_weeks_assignment == "Diner": #if  the attendant wasn't a diner last dinner then his blacklist should remain empty
                attendant.blacklist = attendant.table.diners

#Note, I really should set this up so that it inherits attributes from the Attendant class rather than just points to the parent
class Waiter():
    all_waiters = []

    def __init__(self, parent, table_number):
        self.super = parent
        parent.assigned = True
        parent.waiter = self
        parent.type_of_assignment = "Waiter"
        self.all_waiters.append(self)

    def __str__(self):
        return "%s, %s, W%s" % (self.super.lname, self.super.fname, self.table.number)

#Note, I really should set this up so that it inherits attributes from the Attendant class rather than just points to the parent
class Kitchen_crew():
    all_kitchen_crew = []

    def __init__(self, parent, number):
        self.super = parent
        parent.assigned = True
        parent.type_of_assignment = "Kitchen_crew"
        self.all_kitchen_crew.append(self)

    def __str__(self):
        return "%s, %s, Kitchen" % (self.super.lname, self.super.fname)

# class Diner(Attendant):
#     all_diners = []
#
#     def __init__(self, parent, table_number):
#         self.super = parent
#         parent.assigned = True
#         parent.diner = self
#         parent.type_of_assignment = "Diner"
#         self.all_diners.append(self)
#
#     def __str__(self):
#         return "%s, %s, %s" % (self.super.lname, self.super.fname, self.table.number)

class Table:
    all_tables = {}

    def __init__(self, number, diner, type_of_assignment = None):
        self.diners = []
        self.waiters = []
        self.all_tables[number] = self
        self.number = int(number)
        self.full = False
        if type_of_assignment == "Waiter":
            self.waiters = [diner]
        elif type_of_assignment == "Diner":
            self.diners = [diner]
        diner.table = self

    def add_waiter(self, waiter):
        self.waiters.append(waiter)
        waiter.table = self

    @classmethod
    def reset_all_table_list(cls):
        cls.all_tables = {}
        for attendant in Attendant.all_attendants:
            attendant.table = None

    #override the Table.add_diner function so to record last week's Table instance instead of the current weeks Table instance in the diner instance
    def add_diner(self, diner):
        self.diners.append(diner)
        diner.table = self
        diner.type_of_assignment = "Diner"
        if len(self.diners) == MAX_NUMBER_SITTING_AT_A_TABLE:
            self.full = True

#############################
# local function defintions #
#############################

#function to open a .cvs file, read each line, which contains student attributes, and create a student for each line of attributes
def read_attendant_file(INPUT_FILE):
    # open the cvs file that holds students, one student per row
    f = open(INPUT_FILE)
    lines = (f.read())
    f.close()

    # turn a multi-line string in which each line contains data on an individual student into Student objects
    for line in lines.splitlines():
        attendant_attribute = line.split(",")
        #create a table to hold last weeks diners
        Attendant(lname=attendant_attribute[0], fname=attendant_attribute[1], last_weeks_assignment = attendant_attribute[2])

#function to write all attendants to a given output file using the format set-up for printing Attendant in the class definition
def write_all_attendants(file):
    f = open(file, "w", newline="")
    for obj in Attendant.all_attendants:
        f.write(str(obj))
    f.close()

#function to get a class name given a string consisting of that class name
def str_to_class(classname):
    return globals()[classname]

#function to determine how many tables needed for the dinner given that tables hold a max of 8 people plus one waiter
#and also given that we'll need a certain number of students for kitchen staff
def calc_number_of_tables_needed():

    return math.ceil((len(Attendant.all_attendants) - NUMBER_IN_KITCHEN_STAFF) / (MAX_NUMBER_SITTING_AT_A_TABLE + NUMBER_OF_WAITERS_AT_A_TABLE))

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

        #get the correct Class-type using a string that matches the Class name. Probably easier to just use nested if statements
        cls = str_to_class(work_type)

        worker = cls(assignee, i) #create the correct type of worker object
        if work_type == "Waiter": #if the worker is a waiter add them to the correct table_number
            table = worker.table = Table(i, worker, type_of_assignment="Waiter")
            # table.add_waiter(worker)

        i += 1

def assign_dinner_tables(number_of_tables_needed):

    # get a list of the attendants who do not have a work assignment
    needing_a_table = list(filter(lambda obj: obj.assigned == False, Attendant.all_attendants))

    for table in Table.all_tables.values():

        table_position = 1
        while table_position <= MAX_NUMBER_SITTING_AT_A_TABLE:

            #handle the case where we don't have enough students to fill the last table
            if len(needing_a_table) <1:
                break

            # an index for a diner chosen at random
            rand = random.randint(0, (len(needing_a_table) - 1))
            potential_diner = needing_a_table[rand]
            bad_table = False

            #check to make sure that there is no one already seated at this table who is in the potential diner's blacklist
            for black_listed_diner in potential_diner.blacklist:
                if black_listed_diner in table.diners:
                    bad_table = True
            if not bad_table: #no diners who have already been seated at this table are in this potential_diner's blacklist
                diner = needing_a_table.pop(rand)
                table.add_diner(diner)
                table_position += 1

#################
# Main Body     #
#################

#read all students from a csv file and create a Student object for each one of them
read_attendant_file(INPUT_FILE)

#for each attendant at last week's dinner create a blacklist containing all of the students with which that student ate last week
Attendant.create_blacklists()

#clear-out the list of all tables so that we can assign then anew for this coming week's diner
Table.reset_all_table_list()

#determine how many tables we need given the capacity of each table and the total number
#of people that we need to seat for dinner
number_of_tables_needed = calc_number_of_tables_needed()

#I'm relying on a constant to pass the name of the work-types because they need to match my Class names for that work-type.  See above
#comment about it being easier to just implement nested if statements
assign_work(WORK_TYPES[0], Attendant.all_attendants, NUMBER_IN_KITCHEN_STAFF)
assign_work(WORK_TYPES[1], Attendant.all_attendants, number_of_tables_needed * NUMBER_OF_WAITERS_AT_A_TABLE)

#assign the non-workers to a dinner table
assign_dinner_tables(number_of_tables_needed)

#print status of each student to an output file
write_all_attendants(OUTPUT_FILE)
