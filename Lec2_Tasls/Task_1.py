classes = int(input())

all_ex = True

for _ in range(classes):
    n = int(input())
    has_ex = False

    for _ in range(n):
        name, grade = input().split()
        grade = int(grade)
        if grade == 5:
            has_ex = True
            
    all_ex *= has_ex            

if all_ex:
    print("ДА")
else:
    print("НЕТ")