cmds = {"read": "R", "write": "W", "execute": "X"}

rights = {}
for _ in range(int(input())):
    parts = input().split()
    rights[parts[0]] = set(parts[1:])

for _ in range(int(input())):
    cmd, file = input().split()
    if cmds[cmd] in rights[file]:
        print("OK")
    else:
        print("Access denied")