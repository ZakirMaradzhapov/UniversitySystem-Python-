# UniversitySystem-Python

In this program, I created a mini moodle application running on command line. The idea is that there are three
roles: admin (class), teacher (class), and student(class). Each role can login to the system with
his/her credentials (login, password). All the data is contained in separate json files - courses.json, teachers.json, students.json. 
(I already created some teacher, student accounts and courses for comfortable checking and debugging of the program)

Admin responsibilities are:
1. Create/update/delete teacher accounts.
2. Create/update/delete student accounts.
3. Create/update/delete courses. Attach students and teachers to the courses. Create free
enroll courses with limited number of places.

Teacher responsibilities are:
1. See subjects he/she lead.
2. Mark student
3. Add or Delete student to/from a course
4. Rate student (can be done only once)

Student responsibilities are:
1. Enroll/Unenroll to/from free courses.
2. See marks (see all marks, see specific subject mark)
3. See teachers
4. See free courses to enroll
5. Rate teacher (can be done only once)
