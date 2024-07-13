import random
from typing import List, Dict, Tuple

from utils.constants import *
from utils.logger import get_log
from utils.seating import Student, SeatingTable
from utils.io import get_table


class DSU:
    """The DSU class."""

    def __init__(self, n: int):
        """Create a DSU
        Args:
            n (int): The number of students.
        """
        log = get_log()
        log.debug(f"Creating DSU with n: {n}")
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        """Find the parent of the student x.
        Args:
            x (int): The student you want to find the parent of.
        Returns:
            int: The parent of the student x.
        """
        log = get_log()
        log.debug(f"Finding parent of {x}")
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        log.debug(f"Parent of {x} is {self.parent[x]}")
        return self.parent[x]

    def union(self, x: int, y: int):
        """Union the parent of the student x and the parent of the student y.
        Args:
            x (int): The student you want to union with.
            y (int): The student you want to union with.
        """
        log = get_log()
        log.debug(f"Unioning {x} and {y}")
        x = self.find(x)
        y = self.find(y)
        if x != y:
            if self.size[x] < self.size[y]:
                x, y = y, x
            self.parent[y] = x
            self.size[x] += self.size[y]
        log.debug(f"Union of {x} and {y} completed")


class UndirectedGraph:
    """The UndirectedGraph class."""

    def __init__(self, n: int):
        """Initialize the graph

        Args:
            n (int): The number of students
        """
        self.graph: List[List[int]] = [[]] * n
        self.angle = [0] * n

    def add_edge(self, x: int, y: int):
        """
        Adds a bidirectional edge between two nodes in the graph.
        Args:
            x (int): The index of the first node.
            y (int): The index of the second node.
        """
        log = get_log()
        log.debug(f"Adding bidirectional edge {x} and {y}")
        self.graph[x].append(y)
        self.graph[y].append(x)
        self.angle[x] += 1
        self.angle[y] += 1

    def bfs(self, x: int) -> List[int]:
        """
        Perform a breadth-first search (BFS) starting from the node with index x in the graph.
        Args:
            x (int): The index of the starting node for the BFS.
        Returns:
            List[int]: A list of node indices visited during the BFS traversal.
        """
        log = get_log()
        log.debug(f"Starting BFS from {x}")
        queue = [x]
        visited = [False] * len(self.graph)
        visited[x] = True
        while queue:
            x = queue.pop(0)
            for y in self.graph[x]:
                if not visited[y]:
                    visited[y] = True
                    queue.append(y)
        return [i for i in range(len(visited)) if visited[i]]


def rules_to_graph(
    names: List[Student],
    rules: Dict[str, Dict[int, List[int]]],
) -> List[Student]:
    """
    A function to generate a graph based on rules provided for pairing students.
    Args:
        names (List[Student]): A list of Student objects representing the students.
        rules (Dict[str, Dict[int, List[int]]]): A dictionary containing rules for pairing students.
    Returns:
        List[Student]: A list of Student objects with updated wishes based on the generated graph.

    This function works because of something sort of like 2-sat. When reaches a whitelisted rule,
    we connect themselves. When reaches a blacklisted rule, we union with their opposite. After processing
    the DSU, we can do a BFS and get the result which is the deskmates they might have.
    """

    log = get_log()
    log.info("Start generating pairing graph...")
    log.debug(f"rules: {rules}")
    log.debug(f"Initializing DSU with {len(names)}...")
    dsu = DSU(len(names) * 2)
    graph = UndirectedGraph(len(names))
    # Blacklist: union with their opposite
    log.info("Start unioning blacklist...")
    for u, v in rules["Blacklist"].items():
        for x in v:
            log.debug(f"Blacklist union {x} and {u}(+{len(names)})")
            dsu.union(x, len(names) + u)
    log.info("Blacklist union completed")
    # Whitelist: union with theirselves
    log.info("Start unioning whitelist...")
    for u, v in rules["Whitelist"].items():
        for x in v:
            log.debug(f"Whitelist union {x} and {u}")
            dsu.union(x, u)
    log.info("Whitelist union completed")
    log.info("Start making graphs")
    # Connect them with their parent, which might becomes his deskmate
    for i in range(len(names)):
        if i != dsu.find(i):
            graph.add_edge(i, dsu.find(i))
    # For those with no deskmate, make them deskmates
    single: List[int] = [i for i in range(len(names)) if graph.angle[i] == 0]
    log.debug(f"single: {single}")
    for i in range(len(single) - 1):
        graph.add_edge(single[i], single[i + 1])
    log.info("Done generating pairing graph")

    # Make the graph into Students' wishes
    log.info("Adding wishes...")
    for i in range(len(names)):
        names[i].wish = graph.bfs(i)
        log.debug(f"Wishes of {names[i].name}: {names[i].wish}")
    return names


def generate():
    """Generates a table by assigning students to desks based on their wishes.
    Returns:
        table (SeatingTable): The generated table with students assigned to desks.

    This function starts by getting the table and splitting it into groups.
    It then generates a pairing graph for each group using the rules provided.
    The pairing graph is used to assign desks to students.
    The function then generates a dictionary of desks,
    where each student's ID is mapped to their deskmate's ID.
    If a student has no deskmate, their ID is mapped to -1.
    The function then randomly shuffles the desks and puts them into the table.
    Finally, it returns the generated table.
    """
    log = get_log()
    log.info("Start generating table...")
    table = get_table()
    groups, group_rules = split_group(table)
    names: List[Student] = []
    for group_name in groups.keys():
        log.debug(f"Make graph for groups: {group_name}")
        names.extend(rules_to_graph(groups[group_name], group_rules[group_name]))
    desks = get_deskmates(names)
    desks = list(desks.items())
    log.info("Start putting desks into table...")
    random.shuffle(desks)
    for i in range(table.table_num["GroupNum"]):
        for j in range(table.table_num["RowOfGroup"][i]):
            current_desk = desks.pop()
            if current_desk[0] != -1 and current_desk[1] != -1:
                table.table[i][j] = [
                    table.students[current_desk[0]],
                    table.students[current_desk[1]],
                ]
            elif current_desk[0] == -1 and current_desk[1] != -1:
                table.table[i][j] = [None, table.students[current_desk[1]]]
            elif current_desk[1] == -1 and current_desk[0] != -1:
                table.table[i][j] = [table.students[current_desk[0]], None]
            else:
                table.table[i][j] = [None, None]
            log.debug(
                f"Put {current_desk[0]} and {current_desk[1]} \
                    into table at ({i}, {j})"
            )
    log.debug(f"table: {table.table}")
    log.info("Done generating table")
    return table


def split_group(
    table: SeatingTable,
) -> Tuple[Dict[str, List[Student]], Dict[str, Dict[str, Dict[int, List[int]]]]]:
    """
    Splits the students in the given SeatingTable into groups based on their group names.
    Also splits the rules in the SeatingTable into groups based on the group names of the students.
    Args:
        table (SeatingTable): The SeatingTable containing the students and rules.
    Returns:
        Tuple[Dict[str, List[Student]], Dict[str, Dict[str, Dict[int, List[int]]]]]:
            A tuple containing two dictionaries. The first dictionary maps group names to lists of students.
            The second dictionary maps group names to dictionaries that map rule types to dictionaries
            that map lead students to lists of students.
    Raises:
        ValueError: If the number of groups and rules is not equal.
    """
    log = get_log()
    # Split students into groups
    groups: Dict[str, List[Student]] = {}
    log.info("Start spliting students into groups")
    for student in table.students.values():
        if groups.get(student.group) == None:
            groups[student.group] = [student]
        else:
            groups[student.group].append(student)
    log.info("Done spliting students into groups")
    # Split rules into groups
    log.info("Start split rules into groups")
    group_rules: Dict[str, Dict[str, Dict[int, List[int]]]] = {}
    for typ, rules in table.rules.items():
        for lead, student in rules.items():
            if group_rules.get(table.students[lead].group) == None:
                group_rules[table.students[lead].group] = {
                    "Blacklist": {},
                    "Whitelist": {},
                }
            group_rules[table.students[lead].group][typ][lead] = student
    log.debug(f"group_rules: {group_rules}")
    if len(groups) != len(group_rules):
        log.warning(
            f"Number of groups and rules is not equal, which is {len(groups)} and {len(group_rules)}. Adding placehoder instead."
        )
        for key in groups.keys():
            group_rules[key] = {"Blacklist": {}, "Whitelist": {}}
    log.info("Done split rules into groups")
    return groups, group_rules


def get_deskmates(names: List[Student]):
    """Given a list of Student objects, this function assigns deskmates to each student based on
        their wish list.
    Args:
        names (List[Student]): A list of Student objects representing the students.
    Returns:
        result (Dict[int, int]): A dictionary mapping each student's ID to their deskmate's ID.
        If a student has no deskmate, their ID is mapped to -1.
    """
    log = get_log()
    log.info("Start getting deskmates...")
    checked = [False] * len(names)
    result: Dict[int, int] = {}
    # Get deskmates randomly from the wishes
    for name in names:
        if checked[name.id]:
            continue
        checked[name.id] = True
        found = False
        random.shuffle(name.wish)
        log.debug(f"Trying to find deskmate for {name.id}: {name.wish}")
        for deskmate in name.wish:
            if not checked[deskmate]:
                log.debug(f"{name.id} has {deskmate} as deskmate")
                checked[deskmate] = True
                result[name.id] = deskmate
                found = True
                break
        if not found:
            log.warning(f"id: {name.id} has no deskmate")
            result[name.id] = -1
    # Change half of them, swap their left and right
    log.info("Randomize left and right")
    items = list(result.items())
    random.shuffle(items)
    for i in range(len(items) // 2):
        log.debug(f"swaped left: {items[i][0]}, right: {items[i][1]}")
        result[items[i][1]] = items[i][0]
        result.pop(items[i][0])
    log.debug(f"result: {result}")
    log.info("Done randomizing left and right")
    log.info("Done getting deskmates")
    return result


if __name__ == "__main__":
    generate()
