from typing import List, Dict, Tuple

from constants import *
from logger import get_log


class Student:
    """The Student class."""

    def __init__(
        self,
        black_list: List[int] = [],
        white_list: int = -1,
        id: int = -1,
        name: str = "",
        history: List[List[int]] = [],
    ):
        """Create a Student

        Args:
            black_list (List[int], optional): The students who can't sit with it(by id). Defaults to [].
            white_list (int, optional): The students who must sit with(by id). Defaults to -1.
            id (int, optional): The students' id. Defaults to -1.
            name (str, optional): The students' name. Defaults to "".
            history (List[List[int]], optional): The students' history. Defaults to [].
        """
        log = get_log()
        log.debug(f"Creating student with id: {id}, name: {name}")
        self.black_list = black_list
        self.white_list = white_list
        self.id = id
        self.name = name
        self.history = history

    def __str__(self) -> str:
        return self.name

    __repr__ = __str__

    def __eq__(self, other):
        return self.id == other.id


class SeatingTable:

    def __init__(
        self,
        table_num: Dict[str, int | List[int]] = {},
        rules: Dict[str, Dict[int, int | List[int]]] = {
            "whitelist": {},
            "blacklist": {},
        },
        students: List[Student] = [],
    ):
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

        # For black lists
        log.info(f"Putting black list into rules...")
        log.debug(f"Black list: {self.rules['blacklist']}")
        for id, black in self.rules["blacklist"].items():
            log.debug(f"Assigning blacklist for {id} into {black}")
            self.students[id].black_list = black
        log.info("Putting black list into rules completed")
        # For white lists
        log.info(f"Putting white list into rules...")
        log.debug(f"White list: {self.rules['whitelist']}")
        for id, white in self.rules["whitelist"].items():
            log.debug(f"Assigning whitelist for {id} into {white}")
            self.students[id].white_list = white
        log.info("Putting white list into rules completed")

        # Initialize table
        log.info("Initializing table")
        log.debug(f"Table num: {self.table_num}")
        if "GroupNum" in self.table_num:
            log.debug(f"Creating table with {self.table_num['GroupNum']} groups")
            for _ in range(self.table_num["GroupNum"]):
                self.table.append([])
        else:
            raise ValueError("GroupNum is not in table_num")
        if "RowOfGroup" in self.table_num:
            log.debug(
                f"Creating table with {self.table_num['RowOfGroup']} rows in each group"
            )
            if len(self.table) != len(self.table_num["RowOfGroup"]):
                raise ValueError(
                    f"GroupNum and RowOfGroup should be the same, \
                        but got {self.table_num['GroupNum']} \
                            and {self.table_num['RowOfGroup']}"
                )
            for i, row_num in enumerate(self.table_num["RowOfGroup"]):
                log.debug(f"Creating table with {row_num} columns in group {i}")
                for _ in range(self.table_num["RowOfGroup"]):
                    self.table[i].append([])
        else:
            raise ValueError("RowOfGroup is not in table_num")
        if "ColumnOfDesk" in self.table_num:
            log.debug(
                f"Creating table with {self.table_num['ColumnOfDesk']} columns in each row"
            )
            for i in range(len(self.table)):
                for j in range(len(self.table[i])):
                    log.debug(
                        f"Creating table with {self.table_num['ColumnOfDesk']} \
                            empty students in row {i}, column {j}"
                    )
                    for _ in range(self.table_num["ColumnOfDesk"]):
                        self.table[i][j].append(None)
        else:
            raise ValueError("ColumnOfDesk is not in table_num")
        log.info("Initialization of table completed")


if __name__ == "__main__":
    pass
