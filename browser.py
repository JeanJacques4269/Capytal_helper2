import shutil
import os
import time
import glob
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from constants import *

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain")

path = 'copies'
if os.path.exists(path):
    pass
else:
    os.mkdir(path)

profile.set_preference("browser.download.dir", rf"{os.getcwd()}\copies")

options = Options()

options.headless = True

driver = webdriver.Firefox(firefox_profile=profile, options=options, executable_path=path_driver)


def auth(identifiant, password):
    driver.get("https://ent.iledefrance.fr/auth/login")
    time.sleep(5)
    driver.find_element(By.ID, "email").send_keys(identifiant)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
    time.sleep(2)
    print("Authentifiaction succes")
    driver.get("https://capytale2.ac-paris.fr/web/c-auth/pvd/mln/connect")
    time.sleep(2)


def dl_every_student_file(assignement_link, n):
    driver.get(assignement_link)
    time.sleep(2)
    chosen_file_path = ""
    for i in range(2, n):
        try:

            element = driver.find_element(By.XPATH, f"//tr[{i}]/td[4]/a")
            driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(1)
            element.click()

        except Exception as e:
            print(e)
            continue

        time.sleep(2)
        bitch = False
        done = False
        student_name = "None"
        while not done:
            try:
                time.sleep(0.2)
                student_name = driver.find_element(By.ID, "capytale-student-info").text
                if len(student_name) < 3:
                    continue
                done = True

                student_name = inverse(student_name[:-7])
                student_name = student_name.replace(" ", "_")

                if rf"copies\{student_name}.py" in glob.glob("copies/*.py"):
                    print(f"Skipping {student_name}")
                    bitch = True

                else:
                    driver.find_element(By.ID, "download").click()
            except:
                done = False
        if bitch:
            driver.find_element(By.XPATH, "//a/button/i").click()
            time.sleep(2)

        time.sleep(0.5)
        print(f"Downloaded {student_name}'s file")
        if chosen_file_path == "":
            list_of_files = glob.glob('copies/*.py')
            latest_file = max(list_of_files, key=os.path.getctime)
            chosen_file_path = latest_file

        os.rename(chosen_file_path, fr"copies\{student_name}.py")
        driver.find_element(By.XPATH, "//a/button/i").click()
        time.sleep(2)
    print("Successfully downloaded every file.")
    driver.quit()


def inverse(pre_nom):
    for i in range(len(pre_nom)):
        if pre_nom[i] == " ":
            return pre_nom[i + 1:] + " " + pre_nom[:i]
    return pre_nom


def fct(assignmentlink):
    auth("", "")  # MODIFY HERE : username, password
    dl_every_student_file(assignmentlink, 100)
