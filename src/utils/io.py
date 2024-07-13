import yaml
from typing import List, Dict

from utils.constants import *
from utils.logger import get_log
from utils.seating import Student, SeatingTable


def read_name():
    """Read student names from a YAML file and return a dictionary of students.

    Returns:
        List[Student]: The list of students in their groups.
    """
    log = get_log()
    log.info("Reading name...")
    log.debug(f"Reading from {NAME_FILE}...")
    with open(NAME_FILE, "r") as file:
        name = yaml.safe_load(file)
    log.info("Reading name completed")
    log.info("Adding students...")

    result_students: List[Student] = []
    for id, cur in enumerate(name["Students"]):
        log.debug(f"Creating student with id: {id}, name: {cur['name']}...")
        result_students.append(Student(id=id, **cur))

    for group_name, members in name["Groups"].items():
        for member in members:
            log.debug(f"Adding member: {member} to group: {group_name}...")
            result_students[member].group = group_name
    log.info("Adding students completed")
    return result_students


def read_rules():
    """Read rules from a YAML file and return a dictionary of rules.

    Returns:
        Dict[str, Dict[int, List[int]]]: The rules for the table.
    """
    log = get_log()
    log.info("Reading rules...")
    log.debug(f"Reading from {RULES_FILE}...")
    with open(RULES_FILE, "r") as file:
        rules = yaml.safe_load(file)
    log.info("Reading rules completed")
    log.debug(f"Whitelist: {rules['Whitelist']}")
    log.debug(f"Blacklist: {rules['Blacklist']}")
    return rules


def read_table():
    """Read the size of the table

    Returns:
        Dict[str, int | List[int]]: The settings of the table.
    """
    log = get_log()
    log.debug(f"Reading from {TABLE_FILE}...")
    log.info("Reading table...")
    with open(TABLE_FILE, "r") as file:
        table = yaml.safe_load(file)
    log.info("Reading table completed")
    return table


def get_table() -> SeatingTable:
    """Create a SeatingTable object by reading the names, rules, and table settings from their respective files.

    Returns:
        SeatingTable: The created SeatingTable object.
    """
    log = get_log()
    names = read_name()
    rules = read_rules()
    tables = read_table()
    log.info("Creating SeatingTable...")
    log.debug(f"tables: {tables}")
    log.debug(f"rules: {rules}")
    seating = SeatingTable(tables, rules, names)
    log.info("Creation of table completed")
    return seating
