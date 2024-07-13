import yaml
from typing import List, Dict

from utils.constants import *
from utils.logger import get_log
from utils.seating import Student, SeatingTable


def read_name():
    """Read student names from a YAML file and return a dictionary of students.

    Returns:
        Dict[str, List[Student]]: The list of students in their groups.
    """
    log = get_log()
    log.info("Reading name...")
    log.debug(f"Reading from {NAME_FILE}...")
    with open(NAME_FILE, "r") as file:
        name = yaml.safe_load(file)
    log.info("Reading name completed")
    log.info("Adding students...")

    result_students: List[Student] = []
    for id, cur in enumerate(name["Student"]):
        log.debug(f"Creating student with id: {id}, name: {cur['name']}...")
        result_students.append(Student(id=id, **cur))

    result_groups: Dict[str, List[Student]] = {}
    for group_name in name["Group"].keys():
        log.debug(f"Creating group: {group_name}...")
        result_groups[group_name] = []
    for group_name, members in name["Group"].items():
        log.debug(f"Adding members: {members} to group: {group_name}...")
        result_groups[group_name].append(result_students[id] for id in members)
    log.info("Adding students completed")
    return result_groups


def read_rules():
    log = get_log()
    log.info("Reading rules...")
    with open(RULES_FILE, "r") as file:
        rules = yaml.safe_load(file)
    log.info("Reading rules completed")
    return rules


def read_table():
    log = get_log()
    log.info("Reading table...")
    with open(TABLE_FILE, "r") as file:
        table = yaml.safe_load(file)
    log.info("Reading table completed")
    return table


def get_table():
    names = read_name()
    rules = read_rules()
    tables = read_table()
