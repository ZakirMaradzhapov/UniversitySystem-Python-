import json

# курсы не удаляются у предыдущих учителей Студенты исчезают
class Person:
    def __init__(self, log, password, f_name, l_name):
        self.log = log
        self.password = password
        self.f_name = f_name
        self.l_name = l_name


class Admin(Person):
    def __init__(self, log, password, f_name, l_name):
        super(Admin, self).__init__(log, password, f_name, l_name)

    #log, password, f_name, l_name
    def create_student(self, old_s=None):
        print("Please, fill all the fields:")
        log = input("login: ")
        if log in students.keys():
            print("User with such login already exists!")
            return 0
        if old_s is not None and log not in t_data.keys():
            del s_data[old_s.log]
        if old_s is None:
            password = input("password: ")
        else:
            password = old_s.password

        f_name = input("first name: ")
        l_name = input("last name: ")
        student = Student(log, password, f_name, l_name)
        if old_s is not None:
            for x in student.course_mark.keys():
                x.delete_student(old_s)
                x.add_student(student)
        students[log] = student
        s_data[log] = {"log": log, "password": password, "f_name": f_name, "l_name": l_name}
        with open("students.json", "w") as s:
            json.dump(s_data, s)
        return student

    def delete_student(self, student):
        for x in list(map(lambda y: y, student.course_rate.keys())):
            x.delete_student(student)
        del students[student.log]
        del s_data[student.log]
        with open("students.json", "w") as s:
            json.dump(s_data, s)
        with open("courses.json", "w") as c:
            json.dump(c_data, c)


    def create_teacher(self, old_t=None):
        print("Please, fill all the fields:")
        log = input("login: ")
        if log in teachers.keys():
            print("Teacher with such login already exists!")
            return 0
        if old_t is not None and log not in t_data.keys():
            del t_data[old_t.log]
        if old_t is None:
            password = input("password: ")
        else:
            password = old_t.password

        f_name = input("first name: ")
        l_name = input("last name: ")
        teacher = Teacher(log, password, f_name, l_name)
        if old_t is not None:
            teacher.crss = old_t.crss
            for x in teacher.crss:
                x.teacher = teacher
                c_data[x.course_id]["teacher"] = teacher.log
            teacher.students_rate = old_t.students_rate
        teachers[log] = teacher
        t_data[log] = {"log": log, "password": password, "f_name": f_name, "l_name": l_name}
        with open("teachers.json", "w") as t:
            json.dump(t_data, t)
        with open("courses.json", "w") as c:
            json.dump(c_data, c)
        return teacher

    def delete_teacher(self, teacher):

        del teachers[teacher.log]
        del t_data[teacher.log]
        for x in teacher.crss:
            if self.assign_teacher(x) == 0:
                teachers[teacher.log] = teacher
                t_data[teacher.log] = {"log": teacher.log, "password": teacher.password, "f_name": teacher.f_name, "l_name": teacher.l_name}
        with open("teachers.json", "w") as t:
            json.dump(t_data, t)

    def assign_teacher(self, new_c, old_c=None):  # assign a new teacher to the course

        def delete_from_previous(crs):
            current_teacher = crs.teacher
            current_teacher.crss.remove(crs)

            return crs

        if len(teachers) == 0:
            print("There are no teachers you can assign to the course, need to create new teacher instance")
            teacher = self.create_teacher()
            if teacher == 0:
                print("Cancelling all operatoins...")
                return 0
            teacher.crss.append(new_c)
            new_c.teacher = teacher
            c_data[new_c.course_id]["teacher"] = teacher.log
            with open("courses.json", "w") as c:
                json.dump(c_data, c)
            return

        print("Please, choose an option:\n"
                       "1. Create new teacher instance for the " + new_c.title + " course\n"
                       "2. Assign existing teacher to the " + new_c.title + " course")
        if old_c is not None:
            del_c = delete_from_previous(old_c)  # remove instance of old course from its previous teacher
        elif new_c.teacher is not None:
            del_c = delete_from_previous(new_c)  # remove instance of this course from its previous teacher
        choice = input()
        if choice == "1":
            teacher = self.create_teacher()
            if teacher == 0:
                print("Cancelling all operatoins...")
                if old_c is not None:
                    teachers[old_c.teacher.log].crss.append(del_c)
                elif new_c.teacher is not None:
                    teachers[new_c.teacher.log].crss.append(del_c)
                return 0
            teacher.crss.append(new_c)
            new_c.teacher = teacher
            c_data[new_c.course_id]["teacher"] = teacher.log
            with open("courses.json", "w") as c:
                json.dump(c_data, c)
            return

        elif choice == "2":
            print("Available teachers:")
            for x in teachers.values():
                print(x.f_name + " " + x.l_name + "(login: " + x.log + ");")

            t_log = input("Please, enter login of a teacher you want to assign: ")

            if t_log not in teachers.keys():
                print("Teachers with such login don't exist! Cancelling all operatoins...")
                if old_c is not None:
                    teachers[old_c.teacher.log].crss.append(del_c)
                elif new_c.teacher is not None:
                    teachers[new_c.teacher.log].crss.append(del_c)
                return 0

            teacher = teachers[t_log]
            teacher.crss.append(new_c)  # add t to c_data
            if old_c is not None:
                if t_log == old_c.teacher.log:
                    print("You entered a login of previous teacher! Leave teacher the same.")
                    for x in new_c.studs:
                        mark = x.course_mark[old_c]
                        rate = x.course_rate[old_c]
                        x.course_mark[new_c] = mark
                        x.course_rate[new_c] = rate
                        old_c.delete_student(x)

                else:
                    for x in new_c.studs:
                        old_c.delete_student(x)
            elif new_c.teacher is not None and t_log == new_c.teacher.log:
                print("You entered a login of previous teacher! Leave teacher the same.")
            else:
                for x in new_c.studs:
                    x.course_mark[new_c] = None
                    x.course_rate[new_c] = None

            new_c.teacher = teacher
            c_data[new_c.course_id]["teacher"] = teacher.log
            with open("courses.json", "w") as c:
                json.dump(c_data, c)
            return

        else:
            print("Incorrect input!")
            return 0

    def create_course(self, old_c=None):
        print("Please, fill all the fields:")
        if old_c is None:
            c_id = str(int(max(courses.keys())) + 1)
        else:
            c_id = old_c.course_id
        title = input("title: ")
        max_stud_num = input("maximum number of students: ")
        if old_c is not None:
            if int(max_stud_num) < len(old_c.studs):
                l_studs = str(len(old_c.studs))
                print("There are more than " + str(max_stud_num) + " students in your group (" + l_studs + "), "
                      "so the maximum number of students in this course will be taken as " + l_studs)
                max_stud_num = l_studs

        teacher = None
        courses[c_id] = Course(c_id, title, max_stud_num, teacher)
        c_data[c_id] = {"course_id": c_id, "title": title, "max_stud_num": max_stud_num, "teacher": None, "studs": []}
        course = courses[c_id]
        if old_c is not None:
            for x in old_c.studs:
                course.add_student(x)  # we will delete students from old course in the assign_teacher()
            if self.assign_teacher(course, old_c) == 0:
                courses[c_id] = old_c
                return 0
        else:
            if self.assign_teacher(course) == 0:
                del courses[c_id]
                return 0

        if old_c is not None:
            if int(max_stud_num) == len(old_c.studs):
                courses[c_id].full = True
            c_data[c_id] = {"course_id": c_id, "title": title, "max_stud_num": max_stud_num, "teacher": course.teacher.log, "studs": list(map(lambda x: x.log, course.studs))}
        else:
            c_data[c_id] = {"course_id": c_id, "title": title, "max_stud_num": max_stud_num, "teacher": course.teacher.log, "studs": []}
        with open("courses.json", "w") as c:
            json.dump(c_data, c)

    def delete_course(self, course):
        for x in course.studs:
            course.delete_student(x)
        course.teacher.crss.remove(course)
        del courses[course.course_id]
        del c_data[course.course_id]
        with open("courses.json", "w") as c:
            json.dump(c_data, c)

    def modify_user(self, user):
        if type(user) == Student:
            del students[user.log]
            if self.create_student(user) == 0:
                print("The student won't be modified")
                students[user.log] = user
        elif type(user) == Teacher:
            del teachers[user.log]
            if self.create_teacher(user) == 0:
                print("The teacher won't be modified")
                teachers[user.log] = user
        elif type(user) == Course:
            del courses[user.course_id]
            if self.create_course(user) == 0:
                print("The course won't be modified")
                courses[user.course_id] = user


class Student(Person):

    def __init__(self, log, password, f_name, l_name):
        super(Student, self).__init__(log, password, f_name, l_name)
        self.course_mark = {}
        self.course_rate = {}  # rates of a student from teachers

    def check_courses(self):
        print("Enrolled courses:")
        for x in self.course_mark.keys():
            print("Course " + x.title + " (id: " + x.course_id + "); "
                  "Teacher - " + x.teacher.f_name + " " + x.teacher.l_name)

    def free_courses(self):
        free_c = {}
        for x in courses.values():
            if (not x.full) and (x not in self.course_mark.keys()):
                free_c[x.course_id] = x
        return free_c

    def enroll(self, course):
        free_c = self.free_courses()
        if c_id not in free_c:
            print("Incorrect input!")
        else:
            free_c[c_id].add_student(self)
            print(x.title + " (id: " + x.course_id + ") added to your courses!")

    def unenroll(self, course):
        if course not in self.course_mark.keys():
            print("Incorrect input!")
        else:
            course.delete_student(self)
            print(course.title + " (id: " + course.course_id + ") deleted from your courses!")

    def check_mark(self, course):
        if course not in self.course_mark.keys():
            print("You doesn't have " + course.title + " course (id: " + course.course_id + ")!")
        else:
            if self.course_mark[course] is None:
                print(course.title + " (id: " + course.course_id + ") - isn't marked yet")
            else:
                print(course.title + " (id: " + course.course_id + ") - " + self.course_mark[course])

    def check_rate(self, course):
        if course not in self.course_rate.keys():
            print("You doesn't have " + course.title + " course (id: " + course.course_id + ")!")
        else:
            if self.course_rate[course] is None:
                print(course.title + " (id: " + course.course_id + ") - isn't rated yet")
            else:
                print(course.title + " (id: " + course.course_id + ") - " + str(self.course_rate[course]))

    def check_teacher(self, course):
        if course not in self.course_mark.keys():
            print("You doesn't have " + course.title + " course (id: " + course.course_id + ")!")
        else:
            print("Teacher of " + course.title + " (id: " + course.course_id + "): " + course.teacher.f_name +
                  " " + course.teacher.l_name)

    def rate_teacher(self):
        unrated = {}
        print("Teachers you can rate right now:")
        for x in self.course_mark.keys():
            tchr = x.teacher
            if self not in tchr.students_rate and tchr not in unrated:
                unrated[tchr.log] = tchr
                print(tchr.f_name + " " + tchr.l_name + " (course: " + x.title +
                      "; login: " + tchr.log + ")")

        t_log = input("Please, enter login of a teacher you want to rate: ")
        if t_log not in unrated.keys():
            print("Incorrect input of teacher's login!")
            return 0

        tchr = unrated[t_log]
        rate = int(input("Please, rate chosen teacher from 0 to 100 (Remember, you can rate a teacher only once): "))
        if rate > 100 or rate < 0:
            print("Incorrect input of your rate!")
            return 0

        tchr.students_rate[self] = rate
        print("You rated teacher " + tchr.f_name + " " + tchr.l_name + " as " + str(rate) +
              " out of 100. Assessment can't be changed later")


class Teacher(Person):

    def __init__(self, log, password, f_name, l_name):
        super(Teacher, self).__init__(log, password, f_name, l_name)
        self.crss = []
        self.students_rate = {}

    def check_courses(self):
        print("Сourses you lead:")
        for x in self.crss:
            print("Course " + x.title + " (id: " + x.course_id + ");")

    def course_students(self, course):
        if course not in self.crss:
            print("The teacher " + self.f_name + " " + self.l_name + " doesn't lead " +
                  course.title + " course (id: " + course.course_id + ")!")
        else:
            for x in course.studs:
                print(x.f_name + " " + x.l_name + " (login: " + x.log + ");")

    def check_marks(self, course):
        if course not in self.crss:
            print("Incorrect input!")
            return 0
        for x in course.studs:
            print("Student " +
                         x.f_name + " " + x.l_name + ", (login: " + x.log + ") - ", end="")
            mark = x.course_mark[course]
            if mark == "p":
                print("present;")
            elif mark == "a":
                print("absent;")
            elif mark is None:
                print("wasn't marked yet;")

    def mark_student(self, course, student):
        if course not in self.crss or student not in course.studs:
            print("Incorrect input!")
            return 0

        mark = input("Please, enter your mark ('p' - present/'a' - absent) to student " +
                     student.f_name + " " + student.l_name + ": ")
        if mark == "p" or mark == "a":
            student.course_mark[course] = mark
        else:
            print("Incorrect input! The student won't be marked.")

    def mark_students(self, course):
        if course not in self.crss:
            print("Incorrect input!")
            return 0

        for x in course.studs:
            mark = input("Student " +
                         x.f_name + " " + x.l_name + ": ")
            if mark == "p" or mark == "a":
                x.course_mark[course] = mark
            else:
                print("Incorrect input! The student won't be marked.")

    def check_own_rate(self, student):
        if self.students_rate[student] is None:
            print(student.f_name + " " + student.l_name + " (login: " + student.log + ") - isn't rated yet")
        else:
            print(student.f_name + " " + student.l_name + " (login: " + student.log + ") - " + str(self.students_rate[student]))

    def rate_student(self, course):
        if course not in self.crss:
            print("You can't rate students from " + course.title + " course (id: " + course.course_id + "), "
                  "as you don't lead it!")
            return 0

        unrated = {}
        print("Students in " + course.title + " course (id: " + course.course_id + ") you can rate right now:")
        for x in course.studs:
            if course in x.course_rate.keys():
                if x.course_rate[course] is None:
                    unrated[x.log] = x
                    print(x.f_name + " " + x.l_name + " (login: " + x.log + ")")

        s_log = input("Please, enter login of a student you want to rate: ")
        if s_log not in unrated.keys():
            print("Incorrect input of student's login!")
            return 0

        student = unrated[s_log]
        rate = int(input(
            "Please, rate chosen student from 0 to 100 (Remember, you can rate a student only once): "))
        if rate > 100 or rate < 0:
            print("Incorrect input of your rate!")
            return 0

        student.course_rate[course] = rate
        print("You rated student " + student.f_name + " " + student.l_name + " as " + str(rate) +
              " out of 100. Assessment can't be changed later")

        def __str__(self):
            return self.f_name + " " + self.l_name + " (login: " + self.log + ")"

class Course:

    def __init__(self, course_id, title, max_stud_num, teacher):
        self.course_id = course_id
        self.title = title
        self.max_stud_num = max_stud_num
        self.teacher = teacher
        self.studs = []
        self.full = False

    def add_student(self, student, start=False):
        if student in self.studs:
            print("The student " + student.f_name + " " + student.l_name + " (login: " + student.log
                  + ") is already enrolled to the " + self.title + " course (id: " + self.course_id + ")!")
        elif self.full:
            print("The course " + self.title + " (id: " + self.course_id + ") is full!")
        else:
            self.studs.append(student)
            student.course_mark[self] = None
            student.course_rate[self] = None
            if len(self.studs) == self.max_stud_num:
                self.full = True
            if not start:
                c_data[self.course_id]["studs"].append(student.log)
                with open("courses.json", "w") as c:
                    json.dump(c_data, c)

    def delete_student(self, student):
        if student not in self.studs:
            print("The student " + student.f_name + " " + student.l_name + " (login: " + student.log
                  + ") is not enrolled to the " + self.title + "course (id: " + self.course_id + ")!")
        else:
            self.studs.remove(student)
            del student.course_mark[self]
            del student.course_rate[self]
            self.full = False
            c_data[self.course_id]["studs"].remove(student.log)
            with open("courses.json", "w") as c:
                json.dump(c_data, c)

    def __str__(self):
        return self.title + " course (id: " + self.course_id + ")"

def login(lst):
    log = input("Please, enter your login: ")
    if log in lst.keys():
        paswd = input("Please, enter your password: ")
        if lst[log].password == paswd:
            return lst[log]
        else:
            print("Incorrect password!")
            return 0
    else:
        print("Incorrect login!")
        return 0

global s_data
global t_data
global c_data

with open("students.json", "r") as s:
    s_data = json.load(s)
with open("teachers.json", "r") as t:
    t_data = json.load(t)
with open("courses.json", "r") as c:
    c_data = json.load(c)

global admins
global students
global teachers
global courses

# check correctness of data from json while adding to dict
admins = {"a": Admin("a", "a", "Zakir", "Marajapov")}  # login as a key and the respective object as value
students = {}
teachers = {}
courses = {}  # id as a key and the respective object as value

for x, y in zip(s_data.values(), s_data.keys()):
    if x["log"] != y:
        print("The key and login doesn't match! The student " + x["f_name"] + " " + x["l_name"] + " will be skipped")
        continue
    students[y] = Student(x["log"], x["password"], x["f_name"], x["l_name"])

for x, y in zip(t_data.values(), t_data.keys()):
    if x["log"] != y:
        print("The key and login doesn't match! The teacher " + x["f_name"] + " " + x["l_name"] + " will be skipped")
        continue
    teachers[y] = Teacher(x["log"], x["password"], x["f_name"], x["l_name"])

for x, y in zip(c_data.values(), c_data.keys()):
    t_id = x["teacher"]
    if t_id is None:
        print("Teacher of the course is not assigned in json! The course will be skipped.")
    else:
        if t_id not in teachers.keys():
            print("No such teacher in teachers list! The course will be skipped.")
            continue
        tchr = teachers[t_id]
        if int(x["max_stud_num"]) < len(x["studs"]):
            print("Incorrext value of max number of students! Number of students in the group will be set as max_stud_num")
            course = Course(x["course_id"], x["title"], len(x["studs"]), tchr)
            tchr.crss.append(course)
        else:
            course = Course(x["course_id"], x["title"], str(x["max_stud_num"]), tchr)
            tchr.crss.append(course)
        studs = x["studs"].copy()
        for z in studs:
            if z not in students.keys():
                print("No such student in students list! The student will be skipped.")
                continue
            course.add_student(students[z], True)
        if int(x["max_stud_num"]) == len(x["studs"]):
            course.full = True

    courses[y] = course


while True:
    role = input("Please, enter your role (a - admin; s - student; t - teacher): ")
    if role == "a":
        user = login(admins)
    elif role == "s":
        user = login(students)
    elif role == "t":
        user = login(teachers)
    else:
        print("Incorrect input!")
        continue

    if user == 0:
        continue

    innerProgramm = True
    print("Welcome, " + user.f_name + " " + user.l_name + "! Choose an option:\n")
    while innerProgramm:
        if role == "a":
            choice = input("1. Create/update/delete teacher accounts\n"
                           "2. Create/update/delete student accounts\n"
                           "3. Create/update/delete a course\n"
                           "4. Assign new teacher to the course\n"
                           "5. Add a student to a course\n"
                           "6. Delete student from the course\n"
                           "7. Check all teachers/students/courses\n"
                           "8. Exit\n")
            if choice == "1":
                ch = input("Choose:\n"
                           "1. Create teacher account\n"
                           "2. Update teacher account\n"
                           "3. Delete teacher account\n")
                if ch == "1":
                    user.create_teacher()
                elif ch == "2":
                    t_id = input("Please, enter login of a teacher: ")
                    if t_id not in teachers.keys():
                        print("Teacher with such login doen't exist!")
                        continue
                    teacher = teachers[t_id]
                    print("Teacher " + teacher.f_name + " " + teacher.l_name +
                          "(login: " + teacher.log+")")

                    user.modify_user(teachers[t_id])
                elif ch == "3":
                    t_id = input("Please, enter login of a teacher: ")
                    if t_id not in teachers.keys():
                        print("Teacher with such login doen't exist!")
                        continue
                    teacher = teachers[t_id]
                    user.delete_teacher(teacher)
                else:
                    print("Incorrect input!")
                    continue
            elif choice == "2":
                ch = input("Choose:\n"
                           "1. Create student account\n"
                           "2. Update student account\n"
                           "3. Delete student account\n")
                if ch == "1":
                    user.create_student()
                elif ch == "2":
                    s_id = input("Please, enter login of a student: ")
                    if s_id not in students.keys():
                        print("Student with such login doen't exist!")
                        continue
                    student = students[s_id]
                    print("Student " + student.f_name + " " + student.l_name +
                          " (login: " + student.log + ")")

                    user.modify_user(students[s_id])
                elif ch == "3":
                    s_id = input("Please, enter login of a student: ")
                    if s_id not in students.keys():
                        print("Student with such login doen't exist!")
                        continue
                    student = students[s_id]
                    user.delete_student(student)
                else:
                    print("Incorrect input!")
                    continue
            elif choice == "3":
                ch = input("Choose:\n"
                           "1. Create a course\n"
                           "2. Update a course\n"
                           "3. Delete a course\n")
                if ch == "1":
                    user.create_course()
                elif ch == "2":
                    c_id = input("Please, enter id of a course: ")
                    if c_id not in courses.keys():
                        print("Course with such id doen't exist!")
                        continue
                    course = courses[c_id]
                    print("Course " + course.title + ": id - " +
                          c_id + ", max_stud_num - " + str(course.max_stud_num) + ", teacher - " + course.teacher.log)
                    user.modify_user(courses[c_id])
                elif ch == "3":
                    c_id = input("Please, enter id of a course: ")
                    if c_id not in courses.keys():
                        print("Course with such id doen't exist!")
                        continue
                    course = courses[c_id]
                    user.delete_course(course)
                else:
                    print("Incorrect input!")
                    continue
            elif choice == "4":
                c_id = input("Please, enter id of a course: ")
                if c_id not in courses.keys():
                    print("Course with such id doen't exist!")
                    continue
                course = courses[c_id]
                user.assign_teacher(course)

            elif choice == "5":
                if len(students) == 0:
                    print("Currently, there are no any students in the system")
                    continue
                c_id = input("Please, enter id of course to which you want to add a student: ")
                if c_id not in courses.keys():
                    print("Course with such id doen't exist!")
                    continue
                course = courses[c_id]
                print("Students you can add to " + course.title + " course:")
                for x in students.values():
                    if x not in course.studs:
                        print(x.f_name + " " + x.l_name + " (login: " + x.log + ");")
                s_log = input("Please, enter login of a student you want to add: ")
                if s_log not in students.keys():
                    print("Student with such login doen't exist!")
                    continue
                student = students[s_log]
                course.add_student(student)
                print("The student was succesfully added to course!")
            elif choice == "6":
                if len(students) == 0:
                    print("Currently, there are no any students in the system")
                    continue
                c_id = input("Please, enter id of course from which you want to delete a student: ")
                if c_id not in courses.keys():
                    print("Course with such id doen't exist!")
                    continue
                course = courses[c_id]
                if len(course.studs) == 0:
                    print("There is no students in this course")
                    continue
                print("Students you can delete from " + course.title + " course:")
                for x in course.studs:
                    print(x.f_name + " " + x.l_name + " (login: " + x.log + ");")
                s_log = input("Please, enter login of a student you want to delete: ")
                if s_log not in students.keys():
                    print("Student with such login doen't exist!")
                    continue
                student = students[s_log]
                course.delete_student(student)
                print("The student was succesfully deleted from course!")
            elif choice == "7":
                ch = input("Choose one:\n"
                           "1. Check all students\n"
                           "2. Check all teachers\n"
                           "3. Check all courses\n")
                if ch == "1":
                    for x in students.values():
                        print(x.f_name + " " + x.l_name + " (login: " + x.log + ");")
                elif ch == "2":
                    for x in teachers.values():
                        print(x.f_name + " " + x.l_name + " (login: " + x.log + ");")
                elif ch == "3":
                    for x in courses.values():
                        print(x.title + " course (id: " + x.course_id + ", max students number: " + x.max_stud_num + ", "
                              "teacher: "+ x.teacher.f_name + " " + x.teacher.l_name + ");")
                else:
                    print("Incorrect input!")
                    continue
            elif choice == "8":
                break
            else:
                print("Incorrect input!")
                continue
        elif role == "s":
            choice = input("1. Check courses that you can enroll\n"
                           "2. Enroll to free courses\n"
                           "3. Unenroll from free courses\n"
                           "4. See marks (see all marks, see specific subject mark)\n"
                           "5. Check enrolled courses and its teachers\n"
                           "6. Rate teacher (can be done only once)\n"
                           "7. Check own rates\n"
                           "8. Exit\n")
            if choice == "1":
                free_c = user.free_courses()
                if len(free_c) == 0:
                    print("There is no new courses you can enroll to")
                    continue
                print("Free courses you can enroll: ")
                for x in free_c.values():
                    print("Course " + x.title + " (id: " + x.course_id + "), "
                          "Teacher - " + x.teacher.f_name + " " + x.teacher.l_name + ";")
            elif choice == "2":
                free_c = user.free_courses()
                if len(free_c) == 0:
                    print("There is no new courses you can enroll to")
                    continue
                elif len(free_c) == len(courses):
                    print("You are already enrolled to all courses in the system")
                    continue
                print("Free courses you can enroll: ")
                for x in free_c.values():
                    print("Course " + x.title + " (id: " + x.course_id + "), "
                          "Teacher - " + x.teacher.f_name + " " + x.teacher.l_name + ";")
                c_id = input("Please, enter id of a course you want enroll to: ")
                if c_id not in courses.keys():
                    print("Course with such id doen't exist!")
                    continue
                user.enroll(courses[c_id])
            elif choice == "3":
                if len(user.course_mark) == 0:
                    print("Currently, you are not enrolled to any courses")
                    continue
                user.check_courses()
                c_id = input("Please, enter id of a course you want unenroll from: ")
                if c_id not in courses.keys():
                    print("Course with such id doen't exist!")
                    continue
                user.unenroll(courses[c_id])
            elif choice == "4":
                if len(user.course_mark) == 0:
                    print("Currently, you are not enrolled to any courses")
                    continue
                choice = input("Choose an option:\n"
                               "1. Check all marks\n"
                               "2. Check a mark of specific course\n")
                if choice == "1":
                    for x in user.course_mark.keys():
                        user.check_mark(x)
                elif choice == "2":
                    c_id = input("Please, enter id of a course: ")
                    if c_id not in courses.keys():
                        print("Course with such id doen't exist!")
                        continue
                    user.check_mark(courses[c_id])
                else:
                    print("Incorrect input!")
                    continue
            elif choice == "5":
                if len(user.course_mark) == 0:
                    print("Currently, you are not enrolled to any courses")
                    continue
                user.check_courses()
            elif choice == "6":
                user.rate_teacher()
            elif choice == "7":
                if len(user.course_rate) == 0:
                    print("Currently, you are not enrolled to any courses")
                    continue
                for x in user.course_rate.keys():
                    user.check_rate(x)
            elif choice == "8":
                break
            else:
                print("Incorrect input!")
                continue

        elif role == "t":
            choice = input("1. See courses you lead\n"
                           "2. See detailed info about one of your courses\n"
                           "3. Mark student(s)/See students' mark\n"
                           "4. Add a student to a course\n"
                           "5. Delete a student from a course\n"
                           "6. Rate student (can be done only once)\n"
                           "7. Check own rates\n"
                           "8. Exit\n")

            if choice == "1":
                if len(user.crss) == 0:
                    print("Currently, you don't lead any courses")
                    continue
                user.check_courses()
            elif choice == "2":
                if len(user.crss) == 0:
                    print("Currently, you don't lead any courses")
                    continue
                c_id = input("Please, enter id of a course you are interested in: ")
                if c_id not in courses.keys():
                    print("Course with such id doen't exist!")
                    continue
                course = courses[c_id]
                if course not in user.crss:
                    print("You don't lead a course with such id!")
                else:
                    print("Course " + course.title + " (id: " + c_id + ", maximum number of students: " +
                          course.max_stud_num + ")")
                    if len(course.studs) == 0:
                        print("There is no any students in the course yet")
                        continue
                    print("Students enrolled to this course:")
                    for x in course.studs:
                        print(x.f_name + " " + x.l_name + " (login: " + x.log, end=", ")
                        if x.course_mark[course] is None:
                            print("mark wasn't set yet",  end=", ")
                        else:
                            print("mark: " + x.course_mark[course],   end=", ")
                        if x.course_rate[course] is None:
                            print("rate wasn't set yet);")
                        else:
                            print("rate: " + str(x.course_rate[course]) + ");")
            elif choice == "3":
                if len(user.crss) == 0:
                    print("Currently, you don't lead any courses")
                    continue
                c_id = input("Please, enter id of course: ")
                if c_id not in courses.keys():
                    print("Course with such id doen't exist!")
                    continue
                course = courses[c_id]
                if course not in user.crss:
                    print("You don't lead a course with such id!")
                    continue
                if len(course.studs) == 0:
                    print("There is no any students in the course yet")
                    continue
                choice = input("Please, choose an option:\n"
                               "1. Check marks of students in this course (" + course.title + ");\n"
                               "2. Set marks for all students in the course\n"
                               "3. Set marks for one student in the course\n")
                if choice == "1":
                    print("Marks of students in " + course.title + " course: ")
                    user.check_marks(course)
                elif choice == "2":
                    print("Please, enter your marks as 'p' - present/'a' - absent.")
                    user.mark_students(course)
                elif choice == "3":
                    print("Students in " + course.title + " course (id: " + c_id + ") you can mark:")
                    user.course_students(course)
                    s_log = input("Please, enter login of student you want to mark: ")
                    if s_log not in students.keys():
                        print("Student with such login doen't exist!")
                        continue
                    user.mark_student(course, students[s_log])
                else:
                    continue
            elif choice == "4":
                if len(user.crss) == 0:
                    print("Currently, you don't lead any courses")
                    continue
                c_id = input("Please, enter id of course to which you want to add a student: ")
                if c_id not in courses.keys():
                    print("Course with such id doen't exist!")
                    continue
                course = courses[c_id]
                if course not in user.crss:
                    print("You don't lead a course with such id!")
                else:
                    print("Students you can add to " + course.title + " course:")
                    for x in students.values():
                        if x not in course.studs:
                            print(x.f_name + " " + x.l_name + " (login: " + x.log + ");")
                    s_log = input("Please, enter login of a student you want to add: ")
                    if s_log not in students.keys():
                        print("Student with such login doen't exist!")
                        continue
                    student = students[s_log]
                    course.add_student(student)
                    print("The student was succesfully added to course!")

            elif choice == "5":
                if len(user.crss) == 0:
                    print("Currently, you don't lead any courses")
                    continue
                c_id = input("Please, enter id of course from which you want to delete a student: ")
                if c_id not in courses.keys():
                    print("Course with such id doen't exist!")
                    continue
                course = courses[c_id]
                if course not in user.crss:
                    print("You don't lead a course with such id!")
                else:
                    if len(course.studs) == 0:
                        print("There is no any students in the course yet")
                        continue
                    print("Students you can delete from " + course.title + " course:")
                    for x in course.studs:
                        print(x.f_name + " " + x.l_name + " (login: " + x.log + ");")
                    s_log = input("Please, enter login of a student you want to delete: ")
                    if s_log not in students.keys():
                        print("Student with such login doen't exist!")
                        continue
                    student = students[s_log]
                    course.delete_student(student)
                    print("The student was succesfully deleted from course!")
            elif choice == "6":
                if len(user.crss) == 0:
                    print("Currently, you don't lead any courses")
                    continue
                c_id = input("Please, enter id of course: ")
                if c_id not in courses.keys():
                    print("Course with such id doen't exist!")
                    continue
                course = courses[c_id]
                if len(course.studs) == 0:
                    print("There is no any students in the course yet")
                    continue
                user.rate_student(course)
            elif choice == "7":
                if len(user.students_rate) == 0:
                    print("Currently, you are not rated by any student")
                    continue
                for x in user.students_rate.keys():
                    user.check_own_rate(x)
            elif choice == "8":
                break
            else:
                print("Incorrect input!")
                continue