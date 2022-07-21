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
if not os.path.exists("copies"):
    os.mkdir("copies")
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
    # element = driver.find_element(By.CSS_SELECTOR, ".apps")
    # actions = ActionChains(driver)
    # actions.move_to_element(element).perform()
    # driver.find_element(By.CSS_SELECTOR, ".apps").click()
    # time.sleep(3)
    # driver.find_element(By.CSS_SELECTOR, "#capytale2-paris img").click()
    #
    # time.sleep(4)


def dl_every_student_file(assignement_link, n):
    driver.get(assignement_link)
    time.sleep(2)
    for i in range(n):
        try:
            if i % 2 == 0:
                driver.find_element(By.CSS_SELECTOR, f".odd:nth-child({i + 1}) a").click()
            else:
                driver.find_element(By.CSS_SELECTOR, f".even:nth-child({i + 1}) a").click()
        except:
            print("stop")
            break
        time.sleep(5)

        student_name = driver.find_element(By.ID, "capytale-student-info").text
        student_name = inverse(student_name[:-7])
        driver.find_element(By.ID, "download").click()
        print(f"Downloaded {student_name}'s file")
        time.sleep(0.3)
        list_of_files = glob.glob('copies/*.py')
        latest_file = max(list_of_files, key=os.path.getctime)
        os.rename(latest_file, fr"copies\{student_name}.py")
        driver.find_element(By.XPATH, "//a/button/i").click()
        time.sleep(1)
    print("Download success ")
    driver.quit()


def inverse(pre_nom):
    for i in range(len(pre_nom)):
        if pre_nom[i] == " ":
            return pre_nom[i + 1:] + " " + pre_nom[:i]
    return pre_nom


def fct(assignmentlink):
    pattern = re.compile(r"^https:\/\/capytale2.ac-paris.fr\/web\/assignments\/.+$")
    if not pattern.match(assignmentlink):
        return

    auth("magali.andry-chevalerias", "Ecedouced#42t", )
    dl_every_student_file(assignmentlink, 100)
