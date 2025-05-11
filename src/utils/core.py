import random
from typing import *
from utils import constants, io

def vtk(dct: dict, target) -> str:#find_key_by_value
    """遍历字典，返回第一个包含目标元素的键"""
    for key, container in dct.items():
        if target in container:  # 检查元素是否在键对应的容器中
            return key
    return None  # 未找到时返回 None


def put_musnt(seating: io.SeatingTable) -> io.SeatingTable:
    """Put all the blacklisted in the table"""
    for i, k in seating.rules[io.BLACKLIST].items():
        for j in k:
            if i in seating.rules[io.WHITELIST]:
                continue
            if j in seating.rules[io.WHITELIST]:
                continue
            if seating.status[i] == False:
                column = -1
                row = -1
                pos = random.randint(0, 1)
                while (column == -1 and row == -1) or (
                    seating.table[column][row][0] != ""
                ):
                    column = random.randint(
                        0, len(seating.table) - 1
                    )  # choose a random group
                    row = random.randint(
                        0, len(seating.table[column]) - 1
                    )  # choose a random row
                seating.table[column][row][0] = i
            if seating.status[j] == False:
                column = -1
                row = -1
                pos = random.randint(0, 1)
                while (
                    (column == -1 and row == -1)
                    or (seating.table[column][row][0] != "")
                    or seating.table[column][row][pos ^ 1] == i
                ):  # bumped into the blacklist
                    column = random.randint(
                        0, len(seating.table) - 1
                    )  # choose a random group
                    if column == len(seating.table) - 1:
                        row = random.randint(0, len(seating.table[column]) - 2)
                    else:
                        row = random.randint(
                            0, len(seating.table[column]) - 1
                        )  # choose a random row
                seating.table[column][row][1] = j
                seating.status[i] = seating.status[j] = True
    return seating


def put_must(seating: io.SeatingTable) -> io.SeatingTable:
    """Put all the whitelisted in the table"""
    for i, k in seating.rules[io.WHITELIST].items():
        for j in k:
            if seating.status[i] == True:
                if seating.status[j] == True:
                    continue
            column = -1
            row = -1
            desk = [i, j]
            seating.status[i] = seating.status[j] = True
            random.shuffle(desk)  # randomize the deskmates
            while (column == -1 and row == -1) or (seating.table[column][row][0] != ""):
                column = random.randint(
                    0, len(seating.table) - 1
                )  # choose a random group
                if column == len(seating.table) - 1:
                    row = random.randint(0, len(seating.table[column]) - 2)
                else:
                    row = random.randint(
                        0, len(seating.table[column]) - 1
                    )  # choose a random row
            seating.table[column][row] = desk
    return seating


def rand_others(seating: io.SeatingTable) -> io.SeatingTable:
    """Put all the others in the given table"""
    for names in seating.names.values():
        random.shuffle(names)
        if len(names) % seating.table_num["LineOfGroup"] != 0:
            seating.table[-1][-1][0] = names[0]
            seating.status[names[0]] = True
        start_column = 0
        current_name = 0
        for column in range(start_column, len(seating.table)):
            if current_name >= len(names):
                break
            for row in range(len(seating.table[column])):
                if current_name >= len(names):
                    break
                for pos in (0, 1):
                    while (
                        current_name < len(names)
                        and seating.status[names[current_name]] == True
                    ):
                        current_name += 1
                    if current_name >= len(names):
                        break
                    if seating.table[column][row][pos] == "":
                        seating.table[column][row][pos] = names[current_name]
                        seating.status[names[current_name]] = True
                        current_name += 1
    return seating


def reproduce(seating: io.SeatingTable) -> io.SeatingTable:
    table = []
    for i in range(len(seating.table)):
        for j in range(len(seating.table[i])):
            if len(seating.table[i][j]) <= seating.table_num["LineOfGroup"]:
                continue
            table.append(seating.table[i][j])
    random.shuffle(table)
    cnt = 0
    for i in range(len(seating.table)):
        if cnt >= len(table):
            break
        for j in range(len(seating.table[i])):
            if cnt >= len(table):
                break
            seating.table[i][j] = table[cnt]
            cnt += 1
    lens = max(len(i) for i in seating.table)
    for i in range(len(seating.table)):
        if len(seating.table[i]) <= lens:
            seating.table[i].append([" ", " "])
        seating.table_num["ColumnOfGroup"][i] = lens
    
    return seating


def revamp(seating: io.SeatingTable) -> io.SeatingTable:
    #DIY
    #shuffle
    ttp=[(0,3),(1,2),(0,2),(1,3)]
    for sf in ttp:
        _tmp=[_ for __ in sf for _ in seating.table[__] if _!=[" "," "] and _!=['','']]
        random.shuffle(_tmp)
        for _ in sf:
            for __ in range(seating.table_num["ColumnOfGroup"][_]):
                seating.table[_][__]=_tmp.pop()
    
   
    #PutOther
    
    for i in range(seating.table_num["GroupNum"]):
        for j in range(seating.table_num["ColumnOfGroup"][i]):
            for _ in [0,1]:
                if seating.table[i][j][_] in seating.priory:
                    _tmp=seating.table[i][j][_]
                    _key=vtk(seating.names,_tmp)
                    seating.group[_key].append(_tmp)
                    seating.table[i][j][_]="$"
    for i in range(seating.table_num["GroupNum"]):
        for j in range(seating.table_num["ColumnOfGroup"][i]):
            if seating.table[i][j]==['$','$']:
                continue
            if '$' in seating.table[i][j]:
                _tmp=0
                if seating.table[i][j][_tmp]=='$':
                    _tmp=1
                
                _key=vtk(seating.names,seating.table[i][j][_tmp])
                seating._gro[_key].append(seating.table[i][j][_tmp])
                seating.table[i][j][_tmp]='$'
    grp=[]
    for key,val in seating.group.items():
        if len(val)%2!=0:
            random.shuffle(seating._gro[key])
            seating.group[key].append(seating._gro[key].pop())

    for lst in seating.group.values():
        for _ in range(0,len(lst)//2):
            random.shuffle(lst)
            _tmp=[]
            _tmp.append(lst.pop())
            _tmp.append(lst.pop())
            grp.append(_tmp)
    
    all=len(grp)
    other_grp=[]
    for lst in seating._gro.values():
        for _ in range(0,len(lst)//2):
            random.shuffle(lst)
            other_grp.append([lst.pop(),lst.pop()])
    for j in range(max(seating.table_num["ColumnOfGroup"])):
        if all<=0:
            break
        for i in range(seating.table_num["GroupNum"]):
            if all<=0:
                break
            if not seating.amend[i][j] and seating.table[i][j]!=['$','$']:
                other_grp.append(seating.table[i][j])
                seating.table[i][j]=['$','$']
                all-=1
        
    all=len(grp)
    for j in range(max(seating.table_num["ColumnOfGroup"])):
        if all<=0:
            break
        for i in range(seating.table_num["GroupNum"]):
            if all<=0:
                break
            if seating.amend[i][j]:
                continue
            if seating.table[i][j]==['$','$']:
                random.shuffle(grp)
                seating.table[i][j]=grp.pop()
                if constants.DEBUG:
                    print(f"x:{i},y:{j}->{seating.table[i][j]} ====[amend[{i}][{j}]=>{seating.amend[i][j]}]\n")
                all-=1
            
        
    all=len(other_grp)
    for i in range(seating.table_num["GroupNum"]):
        for j in range(seating.table_num["ColumnOfGroup"][i]):
            if all>0 and seating.table[i][j]==['$','$']:
                random.shuffle(other_grp)
                seating.table[i][j]=other_grp.pop()
                all-=1
            if all<=0:
                break
        if all<=0:
            break
    return seating


def rdesk():
    seating = io.SeatingTable()
    if constants.DEBUG:
        print("Start: ", seating.table)
    seating = put_musnt(seating)
    if constants.DEBUG:
        print("Put Musnt: ", seating.table)
    seating = put_must(seating)
    if constants.DEBUG:
        print("Put Must: ", seating.table)
    seating = rand_others(seating)
    if constants.DEBUG:
        print("Rand Others: ", seating.table)
    seating = reproduce(seating)
    if constants.DEBUG:
        print("Reproduce: ", seating.table)
    seating = revamp(seating)
    if constants.DEBUG:
        print("Revamp: ", seating.table)
    seating.save()
    return seating
