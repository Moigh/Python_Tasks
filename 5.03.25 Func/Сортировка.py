students = [
    {
        "name": "Карл",
        "grades": []
    },
    {
        "name": "Боб", 
        "grades": [
            {"course_name": "Математика", "score": 78},
            {"course_name": "История", "score": 92},
            {"course_name": "Химия", "score": 88}
        ]
    },
    {
        "name": "Алиса",
        "grades": [
            {"course_name": "Математика", "score": 90},
            {"course_name": "Физика", "score": 85}
        ]
    }
]

sorted_students = sorted(students, key=lambda student: (
        -len([grade for grade in student['grades'] if grade['score'] > 80]),
        -sum(grade['score'] for grade in student['grades']) / len(student['grades']) if student['grades'] else 0,
        student['name']
    ))

import pprint
pprint.pprint(sorted_students)