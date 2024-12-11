from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from random import choice
from art import tprint

import constatnts as ct
import yaml



def set_repr(dumper, value):
    return dumper.represent_list(sorted(value))


yaml.add_representer(set, set_repr)
ignored_exceptions = (StaleElementReferenceException, NoSuchElementException)


def on_load_elem(driver, by: str, value: str, timeout: int):
    return WebDriverWait(
        driver,
        timeout=timeout,
        ignored_exceptions=ignored_exceptions,
    
    ).until(expected_conditions.presence_of_element_located((by, value)))


def on_load_all(driver, by: str, value: str, timeout: int):
    return WebDriverWait(
        driver,
        timeout=timeout,
        ignored_exceptions=ignored_exceptions,
    
    ).until(expected_conditions.presence_of_all_elements_located((by, value)))


def save_db(results, path=ct.DEF_DB_FILE) -> None:
    print(f"[*] Saving results into {path}")
    with open(path, 'w') as file:
        yaml.dump(results, file, default_flow_style=False)

def load_db(path=ct.DEF_DB_FILE) -> dict:
    try:
        with open(path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return dict()
    

def print_banner():
    tprint(f"{ct.BANNER}", font=choice(ct.ART_FONTS))
    print(f"[*] Font-Family Finder ({ct.VERSION})\n[*] Para el Pana más fresco\n[*] By {ct.AUTHOR}")

