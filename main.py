import sqlite3


def connect_db():
    conn = sqlite3.connect("university.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        major TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL,
        instructor TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_courses (
        student_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(course_id) REFERENCES courses(course_id),
        PRIMARY KEY(student_id, course_id)
    )""")

    conn.commit()
    return conn


def add_student(conn):
    name = input("Введіть ім'я студента: ")
    age = int(input("Введіть вік студента: "))
    major = input("Введіть спеціальність студента: ")
    conn.execute("INSERT INTO students (name, age, major) VALUES (?, ?, ?)", (name, age, major))
    conn.commit()
    print("Студент доданий успішно.")


def add_course(conn):
    course_name = input("Введіть назву курсу: ")
    instructor = input("Введіть ім'я викладача: ")
    conn.execute("INSERT INTO courses (course_name, instructor) VALUES (?, ?)", (course_name, instructor))
    conn.commit()
    print("Курс доданий успішно.")


def enroll_student(conn):
    student_id = int(input("Введіть ID студента: "))
    course_id = int(input("Введіть ID курсу: "))
    conn.execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
    conn.commit()
    print("Студент записаний на курс успішно.")


def view_students(conn):
    cursor = conn.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Ім'я: {row[1]}, Вік: {row[2]}, Спеціальність: {row[3]}")


def view_courses(conn):
    cursor = conn.execute("SELECT * FROM courses")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Назва курсу: {row[1]}, Викладач: {row[2]}")


def view_students_in_course(conn):
    course_id = int(input("Введіть ID курсу: "))
    cursor = conn.execute("""
    SELECT students.id, students.name, students.age, students.major
    FROM students
    JOIN student_courses ON students.id = student_courses.student_id
    WHERE student_courses.course_id = ?
    """, (course_id,))
    students = cursor.fetchall()
    if students:
        print("Студенти, зареєстровані на цей курс:")
        for student in students:
            print(f"ID: {student[0]}, Ім'я: {student[1]}, Вік: {student[2]}, Спеціальність: {student[3]}")
    else:
        print("На цей курс поки не зареєстровано жодного студента.")


def main():
    conn = connect_db()
    while True:
        print("""
        Меню:
        1. Додати студента
        2. Додати курс
        3. Записати студента на курс
        4. Переглянути всіх студентів
        5. Переглянути всі курси
        6. Переглянути студентів на конкретному курсі
        7. Вихід
        """)
        choice = input("Виберіть опцію: ")
        if choice == "1":
            add_student(conn)
        elif choice == "2":
            add_course(conn)
        elif choice == "3":
            enroll_student(conn)
        elif choice == "4":
            view_students(conn)
        elif choice == "5":
            view_courses(conn)
        elif choice == "6":
            view_students_in_course(conn)
        elif choice == "7":
            conn.close()
            print("Програма завершена.")
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
