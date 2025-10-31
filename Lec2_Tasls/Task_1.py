classes = int(input())
all_ex = []

for _ in range(classes):
    n = int(input())    
    any_ex = []

    for _ in range(n):
        name, grade = input().split()
        any_ex.append(int(grade) == 5)
    
    all_ex.append(any(any_ex))            

if all(all_ex):
    print("ДА")
else:
    print("НЕТ")