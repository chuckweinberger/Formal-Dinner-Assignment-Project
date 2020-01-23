import random
##################
# Global variables
##################

# list for containing all students
students_list = []

# list of students who don't have work assignments
free_students = []

#list for all tables, will contain a dict of all Students who are sitting at the table.  Table number = index of that table in the array plus 1
table_assignments = []

# Object definitions
class Student:
    def __init__(self, lname, fname):
        self.lname = lname
        self.fname = fname
        self.assignment = { "kitchen_staff": False, "wait_staff": False, "table_assignment": False, "table": int }

#######################
# function defintions
#######################

# function takes in one line of ascii text with values separated by commas and returns a Student object that is created based on those values
def convert_string_to_student(comma_sep_attrs):
    attributes = comma_sep_attrs.split(",")
    student = Student(lname = attributes[0], fname = attributes[1])
    return student

#function to open a .cvs file, read its contents, call a function to process the contents, and then close the file
def read_students_file(file_name):
    # open the cvs file that holds students, one student per row
    f = open("Dinner Seating - Student List 2018-19 4.csv")
    lines = (f.read())
    f.close()

    # turn a multiline string in which each line contains data on an individual student into student objects
    file_list = []
    for i in lines.splitlines():
        student = convert_string_to_student(i)
        file_list.append(student)

    return file_list

#function to take in a list of Student objects and print them to a .csf vile by lastname, firstname, and assignment
def write_file(students):
    f = open("Dinner Assignments.csv", "w", newline="")
    for student in students:
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

students_list = read_students_file("sample_data.csv")
#keep track of students that don't have jobs so that we don't give someone two jobs, and that we seat only those who don't have jobs
free_students = students_list.copy()
#I really need a function here to determine how many tables that I'll need given the amount of students.
#That way I can determine the number of tables I'll have and the number of waiters I'll need.
#Instead, I've just predetermined that I'll need 32 tables
waiters_list = choose_random_individuals_for_something("wait_staff", 32)
kitchen_list = choose_random_individuals_for_something("kitchen_staff", 8)

# iterate through the 31 tables selecting students at random to sit at each table and to wait for each table
for i in range(1, 33):
    # get the students for the current table
    table_assignments.append(choose_random_individuals_for_something("table_assignment", 8, i))
    # assign the waiter for the current table out of the list of already assigned waiters
    waiter = waiters_list[i-1]
    waiter.assignment["table"] = i
    table_assignments[i-1].append(waiter)

write_file(students_list)
