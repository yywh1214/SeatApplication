from typing import List, Dict, Tuple

from utils.constants import *
from utils.logger import get_log


class Student:
    """The Student class."""

    def __init__(
        self,
        black_list: List[int] = [],
        white_list: List[int] = [],
        id: int = -1,
        name: str = "",
        history: List[List[int]] = [],
        group: str = "",
    ):
        """Create a Student

        Args:
            black_list (List[int], optional): The students who can't sit with it(by id). Defaults to [].
            white_list (List[int], optional): The students who must sit with(by id). Defaults to [].
            id (int, optional): The students' id. Defaults to -1.
            name (str, optional): The students' name. Defaults to "".
            history (List[List[int]], optional): The students' history. Defaults to [].
            group (str, optional): The students' group. Defaults to "".
        """
        log = get_log()
        log.debug(f"Creating student with id: {id}, name: {name}")
        self.black_list = black_list
        self.white_list = white_list
        self.id = id
        self.name = name
        self.history = history
        self.group = group
        self.wish: List[int] = []

    def __str__(self) -> str:
        return str(self.name)

    __repr__ = __str__

    def __eq__(self, other):
        return self.id == other.id


class SeatingTable:
    """The SeatingTable class."""

    def __init__(
        self,
        table_num: Dict[str, int | List[int]] = {},
        rules: Dict[str, Dict[int, List[int]]] = {
            "Whitelist": {},
            "Blacklist": {},
        },
        students: List[Student] = [],
    ):
        """Create a SeatingTable

        Args:
            table_num (Dict[str, int | List[int]], optional): The settings. Defaults to {}.
            rules (Dict[str, Dict[int, List[int]]], optional): The rules for the table. Defaults to { "Whitelist": {}, "Blacklist": {}, }.
            students (List[Student], optional): The students you wish to put. Defaults to [].

        Raises:
            ValueError: When the number of students is more than the seats.
        """
        log = get_log()
        log.info("Creating SeatingTable...")
        log.debug(f"table_num: {table_num}")
        self.table_num = table_num
        self.rules = rules
        self.students: Dict[int, Student] = {
            student.id: student for student in students
        }
        self.table: List[List[List[Student]]] = []
        log.info("Creation of table completed")

        # Start check
        log.info("Starting check...")
        log.debug(f"Table num: {self.table_num}")
        if "GroupNum" not in self.table_num:  # If not defined, use default
            log.warning(
                f"GroupNum is not in table_num, creating a default table with {DEFAULT_GROUP_NUM} groups"
            )
            self.table_num["GroupNum"] = DEFAULT_GROUP_NUM
        if "RowOfGroup" not in self.table_num:
            log.warning(
                f"RowOfGroup is not in table_num, creating a default table with {DEFAULT_ROW_OF_GROUP} rows in each group"
            )
            self.table_num["RowOfGroup"] = DEFAULT_ROW_OF_GROUP
        if "ColumnOfDesk" not in self.table_num:
            log.warning(
                f"ColumnOfDesk is not in table_num, creating a default table with {DEFAULT_COLUMN_OF_DESK} columns in each row"
            )
            self.table_num["ColumnOfDesk"] = DEFAULT_COLUMN_OF_DESK
        students_num = len(self.students)
        log.debug(f"Students num: {students_num}")
        seats_num = sum(self.table_num["RowOfGroup"]) * self.table_num["ColumnOfDesk"]  # type: ignore
        log.debug(f"Seats num: {seats_num}")
        if students_num > seats_num:  # Not enough seats
            log.error(
                f"Not enough seats for students, expect {students_num},found {seats_num}"
            )
            raise ValueError("Not enough seats for students")
        elif students_num < seats_num:  # Not enough students
            log.warning(
                f"Not enough students for seats, expect {seats_num},found {students_num}. Putting placeholders instead"
            )
            students.extend(
                [Student(id=i) for i in range(students_num, seats_num)]
            )
        log.info("Check succeeded")
        # Initialize table
        log.info("Initializing table")
        for i in range(self.table_num["GroupNum"]):  # type: ignore
            self.table.append([])
            for j in range(self.table_num["RowOfGroup"][i]):  # type: ignore
                self.table[i].append([])
                for _ in range(self.table_num["ColumnOfDesk"]):  # type: ignore
                    self.table[i][j].append(None)  # type: ignore
        log.info("Initialization of table completed")

    def parse_rules(self):
        """Parse the rules in the SeatingTable."""
        log = get_log()
        # For black lists
        log.info(f"Putting black list into rules...")
        log.debug(f"Black list: {self.rules['Blacklist']}")
        for id, black in self.rules["Blacklist"].items():
            log.debug(f"Assigning Blacklist for {id} into {black}")
            self.students[id].black_list = black
        log.info("Putting black list into rules completed")
        # For white lists
        log.info(f"Putting white list into rules...")
        log.debug(f"White list: {self.rules['Whitelist']}")
        for id, white in self.rules["Whitelist"].items():
            log.debug(f"Assigning Whitelist for {id} into {white}")
            self.students[id].white_list = white
        log.info("Putting white list into rules completed")

    def __str__(self) -> str:
        """Generate the string representation of the SeatingTable.
        Returns:
            str: The string representation of the SeatingTable.
        """
        result = ""
        for i in range(self.table_num["GroupNum"]):  # type: ignore
            for j in range(self.table_num["RowOfGroup"][i]):  # type: ignore
                for k in range(self.table_num["ColumnOfDesk"]):  # type: ignore
                    result += str(self.table[i][j][k]) + " "
                result += "\n"
            result += "\n"
        return result

    __repr__ = __str__


if __name__ == "__main__":
    pass
