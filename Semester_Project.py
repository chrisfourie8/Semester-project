from tkinter import *
import tkinter as tk
from tkinter.font import Font
from tkinter import messagebox


# My hypothetical dormitory has 12 floors, with 8 rooms on each floor
# Rooms on the 6th and 12th floors are single rooms, every other room is a double room
# On every 2nd floor, the rooms ending in 01 and 02 are laundry rooms (and will be excluded for in effect)

error_message = None

# function that calculates how compatible each potential roommate is
def compatibility(sex, course, languages, nationalist, nationality, exchange, medical_condition): 
    """
    function that calculates how compatible each potential roommate is
    returns a dictionary of roomnumbers as keys and compatibility scores as values
    """

    # list of compatability scores of the roommates in potential_roommates
    compatibility_dict = {}

    # dictionary of relative course compatability
    course_compatibility = {"Medicine" : 6, "Biology" : 6, "Physics" : 5, "Chemistry" : 5, "Computer Science" : 4, "Mathematics" : 4, "Humanities" : 2, "Politics" : 2, "Law" : 1, "Language" : 1 }


    for i, j in potential_roommates.items(): 
        current_compatibility = 0

        if j == None:       # no roommate, so no compatability check required
            compatibility_dict[i] = current_compatibility
            continue
        else:
            # sex factor 
            if sex == j[0]:    # same sex
                current_compatibility += 500
            else:
                current_compatibility -= 500

            # course factor
            self_course = course_compatibility[course]
            roommate_course = course_compatibility[j[1]] 

            if self_course - roommate_course == 0:     # very similar courses
                current_compatibility += 20
            elif self_course - roommate_course == 1 or self_course - roommate_course == -1: # similar courses
                current_compatibility += 10

            # language factor 
            common_language = False 
            for k in languages:
                if k in j[4]:
                    common_language = True  
            
            if common_language == True:
                current_compatibility += 50
            else:
                current_compatibility -= 50

            # nationalist factor
            if nationalist == True or j[3] == True:     # if either potential roommate is nationalist
                if nationality == j[2]:                        # if both roommates are from the same country
                    current_compatibility += 30
                else:
                    current_compatibility -= 30
            else:
                current_compatibility += 10


            # exchange factor
            if exchange ^ j[-1]:      # if only one (out of two potential roommates) is an exchange student
                current_compatibility -= 20
            else:
                current_compatibility += 20



            # medical_conditionical factor (this helps ensure that these students are assigned rooms from the top of the building)
            if medical_condition == True:
                current_compatibility += (i // 100)

            compatibility_dict[i] = current_compatibility

    print(compatibility_dict)          ### to justify the assigned room
    return compatibility_dict

        

def assign(medical_condition, single):
    """
    function that assigns the most appropriate room to the user
    returns an integer or string error-message
    """

    best_option = 0

    # cases where there are no rooms or 1 room available
    found_last = False

    if len(available) == 0 and len(available_single) == 0:
        return ("Unfortunately, there are no available rooms")
    
    # if one single room is available
    elif len(available) == 0 and len(available_single) == 1:
        best_option = available_single[0]
        del available_single[0]
        found_last = True
    
    # if one double room is available    
    elif len(available) == 1 and len(available_single) == 0:
        best_option = available[0]
        del available[0]
        found_last = True


    if found_last == True:
        unavailable.add(best_option) 
        student_rooms[student_id] = [best_option]
        return best_option


    # cases where single == True
    if single == True:
        found_single = False

        if len(available_single) > 0:
            if medical_condition == True:
                best_option = available_single[-1]    # from the top
            else:
                best_option = available_single[0]     # from the bottom
                
            found_single = True
                
        else:
            double_found = False
            delroommate = 0
            delroom = 0
            # check for any completely empty rooms in available (edge case) and add the new student to potential_roommates       
            for i, j in zip(available, potential_roommates):
                if potential_roommates[j] == None:
                    potential_roommates[j+1] = [sex, course, nationality, nationalist, languages, exchange]
                    best_option = available[i]
                    found_single = True
                    double_found = True

                    delroommate = j
                    delroom = i
                    break

            if double_found == True and found_single == True:
                del potential_roommates[delroommate]
                del available[delroom]

        if found_single == True:
            student_rooms[student_id] = best_option
            unavailable.add(best_option)

            return best_option
        else:
            return("Unfortunately, there are no available single rooms")
        

    options = []

    compatibility_dict = compatibility(sex, course, languages, nationalist, nationality, exchange, medical_condition)

    # split the options as a filter for medical_condition
    half = len(available) // 2
    keys = list(compatibility_dict.keys())

    if medical_condition == True:
        options = available[half:]
        half_dictionary = {keys[i]: compatibility_dict[keys[i]] for i in range(half, len(keys))}
        
    else:
        options = available[:half]
        half_dictionary = {keys[i]: compatibility_dict[keys[i]] for i in range(half)}


    # find the best option
    best_compatibility = 0
    for i, j in zip(options, half_dictionary):
        if half_dictionary[j] > best_compatibility:
            best_compatibility = half_dictionary[j]
            best_option = i



    # add the new student to student_rooms
    student_rooms[student_id] = [best_option]


    # check if potential_roommates needs to be updated (test case)
    if best_option in potential_roommates:
        if potential_roommates[best_option] == None:
            roomfinder = str(best_option)
            roomfloat = roomfinder[-2:-1]

            # calculates the other room's room number
            if roomfloat == ".1":
                otherroom = best_option + 0.1
            else:
                otherroom = best_option - 0.1

            potential_roommates[best_option] = [sex, course, nationality, nationalist, languages, exchange]
            del potential_roommates[otherroom]


    available.remove(best_option)
    unavailable.add(best_option)
    return best_option




# the dictionary containing information about which rooms contains which students (practically updated by the assign function)
student_rooms = {}

# test cases (edge cases on floor 8)
available = [107.2, 206.1, 307.2, 503.2, 803.1, 803.2, 904.1, 1103.2, 1106.1, 1108.2]
available_single = [607.1, 1203.1]

# assign numbers to all the unavailable rooms in the dormitory
unavailable = set()

for floor in range(1, 13):
    room = 0.0
    room += floor * 100

    for flat in range(1, 9):
        if floor % 2 == 0 and (flat == 1 or flat == 2):      # laundry rooms
            continue
        else:
            # keeps the test cases accessible and create a list of unavailable rooms
            if floor == 6 or floor == 12:
                if (room + flat + 0.1) not in available_single:
                    unavailable.add((room + flat + 0.1))
                    continue
            if (room + flat + 0.1) not in available and (room + flat + 0.2) not in available:
                unavailable.add((room + flat + 0.1))
                unavailable.add((room + flat + 0.2))
                
            elif (room + flat + 0.1) not in available and (room + flat + 0.2) in available:
                unavailable.add((room + flat + 0.1))
                
            elif (room + flat + 0.1) in available and (room + flat + 0.2) not in available:
                unavailable.add((room + flat + 0.2))
                


# information about the potential roommates of the user (practically updated by the assign function)
potential_roommates = {}

# the first boolean in the value is the nationalist value 
# the second boolean in the value is the exchange value
potential_roommates[107.1] = ["Male", "Computer Science", "Turkey", False, ["English", "Turkish/Azerbaijani"], False]
potential_roommates[206.2] = ["Female", "Humanities", "Germany", False, ["English", "German"], False]
potential_roommates[307.1] = ["Male", "Physics", "Czech Republic", False, ["Czech/Slovak", "English"], False]
potential_roommates[503.1] = ["Female", "Medicine", "Slovakia", True, ["Czech/Slovak"], False]   
potential_roommates[803.1] = None
potential_roommates[803.2] = None
potential_roommates[904.2] = ["Male", "Biology", "Portugal", False, ["Spanish/Portuguese", "English"], True]
potential_roommates[1103.1] = ["Female", "Language", "India", False, ["English", "French", "Hindi", "Italian"], False]
potential_roommates[1106.2] = ["Male", "Mathematics", "Serbia", False, ["Balkans", "English"], False]
potential_roommates[1108.1] = ["Female", "Politics", "Russia", False, ["Czech/Slovak", "English", "Russian/Ukrainian"], False]



# Create a new Tkinter window
window = tk.Tk()
window.title("Basic Information")

# Define a function to get the user's inputs
def get_inputs():
    """
    Retrieves the values from the inputs 
    Made global 
    """
    
    global name, student_id, sex, course, nationality, nationalist, languages, exchange, medical_condition, single
    name = name_entry.get()
    
    student_id = student_id_entry.get()
    sex = sex_var.get()
    course = course_var.get()
    languages = list(languages_entry.get().split(", ")) 
    nationality = nationality_entry.get()
    nationalist = nationalist_var.get()
    exchange = exchange_var.get()
    medical_condition = medical_condition_var.get()
    single = single_var.get()
    if error_message != "":
        window.destroy()

# Create labels and entry boxes for the user's inputs
name_label = tk.Label(window, text="Name:")
name_entry = tk.Entry(window)

student_id_label = tk.Label(window, text="Student Number (8 digits):")
student_id_entry = tk.Entry(window)

sex_label = tk.Label(window, text="Sex:")
sex_var = tk.StringVar(value="Male")
sex_male_radio = tk.Radiobutton(window, text="Male", variable=sex_var, value="Male")
sex_female_radio = tk.Radiobutton(window, text="Female", variable=sex_var, value="Female")

course_label = tk.Label(window, text="Course:")
course_options = ["Computer Science", "Mathematics", "Physics", "Chemistry", "Biology", "Medicine", "Politics", "Humanities", "Law", "Languages"]
course_var = tk.StringVar(value=course_options[0])
course_dropdown = tk.OptionMenu(window, course_var, *course_options)

nationality_label = tk.Label(window, text="My country of origin:")
nationality_entry = tk.Entry(window)


nationalist_var = tk.BooleanVar(value=False)
nationalist_checkbutton = tk.Checkbutton(window, text="I want to live with someone from my country", variable=nationalist_var)

languages_label = tk.Label(window, text="Languages spoken (separated by commas):")
languages_entry = tk.Entry(window)

exchange_var = tk.BooleanVar(value=False)
exchange_checkbutton = tk.Checkbutton(window, text="I am an exchange student", variable=exchange_var)

medical_condition_var = tk.BooleanVar(value=False)
medical_condition_checkbutton = tk.Checkbutton(window, text="I have a medical condition, such as asthma, diabetes etc", variable=medical_condition_var)

single_var = tk.BooleanVar(value=False)
single_checkbutton = tk.Checkbutton(window, text="I want to live in a single room", variable=single_var)

# Create a button to submit the inputs
submit_button = tk.Button(window, text="Submit", command=get_inputs)

# Add the widgets to the window
name_label.pack()
name_entry.pack()

student_id_label.pack()
student_id_entry.pack()


sex_label.pack()
sex_male_radio.pack()
sex_female_radio.pack()

course_label.pack()
course_dropdown.pack()

nationality_label.pack()
nationality_entry.pack()

nationalist_checkbutton.pack()

languages_label.pack()
languages_entry.pack()

exchange_checkbutton.pack()

medical_condition_checkbutton.pack()

single_checkbutton.pack()

submit_button.pack()

window.geometry("700x500")


# Start the Tkinter event loop
window.mainloop()

 
# handles invalid input
if not student_id.isnumeric() or len(student_id) != 8:
    error_message = "Invalid student number"
elif name == "":
    error_message = ("Please enter your name")
elif nationality == "":
    error_message = ("Please enter your nationality")
elif len(languages) == 0: 
    error_message = ("Please enter at least one language")


if error_message != None:
    messagebox.showerror(message = error_message)
else:
   assignedroom = assign(medical_condition, single)


if error_message == None:
    # create a tkinter window
    door = tk.Tk()

    # set the font and font size for the label
    my_font = Font(family='Helvetica', size=25, weight='bold')

    # create a label widget to display the assigned room
    if error_message!="":
        label = tk.Label(door, text=assignedroom, font=my_font)
    else:
        messagebox.showerror(message = "Invalid student number")


    # center the label widget in the window
    label.pack(expand=True)
    label.place(relx=0.5, rely=0.5, anchor='center')

    # set the size of the window
    door.geometry("800x500")

    # start the tkinter event loop
    door.mainloop()