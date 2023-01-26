from login_gui import Login_window
from PyQt5.QtWidgets import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

user_username = Login_window().Username
user_password = Login_window().Password
remember_me = Login_window().Remember_me

crn_list = []
lecture_codes = []
lecture_names = []
lecture_times = []
wrapper_list = [[], crn_list, lecture_codes, [], lecture_names, lecture_times]
lecture_credits = []

driver = webdriver.Firefox()
driver.minimize_window()
url = "https://kepler-beta.itu.edu.tr"
driver.get(url)

username = driver.find_element(By.XPATH, "//*[@id='ContentPlaceHolder1_tbUserName']")
password = driver.find_element(By.XPATH, "//*[@id='ContentPlaceHolder1_tbPassword']")
login = driver.find_element(By.XPATH, "//*[@id='ContentPlaceHolder1_btnLogin']")
username.send_keys(user_username)
password.send_keys(user_password)
login.click()

time.sleep(0.6)

general_gpa = float(driver.find_element(By.XPATH, "//*[@id='page-wrapper']/div[2]/div/div/div[1]/div[2]/div/div/div[1]/div[4]/div/div[2]/span").text)
total_credit = float((driver.find_element(By.XPATH, "//*[@id='page-wrapper']/div[2]/div/div/div[1]/div[2]/div/div/div[1]/div[1]/div/div[2]/div[2]/div").text)[14:])

driver.get("https://kepler-beta.itu.edu.tr/ogrenci/DersKayitIslemleri/KayitliDersler")

time.sleep(5)

time.sleep(0.6)

found_lecture = True
try:
    outer_table = driver.find_element(By.XPATH, "//*[@id='page-wrapper']/div[2]/div/div/div[3]/div/div/table/tbody")
except:
    found_lecture = False
else:
    inner_tables = outer_table.find_elements(By.TAG_NAME, "tr")
    for rows in inner_tables:
        for i in range(1,6):
            row = rows.find_elements(By.TAG_NAME, "td")[i]
            if i == 2:
                lecture_codes.append(row.text + " " + rows.find_elements(By.TAG_NAME, "td")[3].text)
            elif i == 3:
                continue
            else:
                wrapper_list[i].append(row.text)

driver.get("https://kepler-beta.itu.edu.tr/ogrenci/NotBilgileri/DonemSonuNotlari")
found_grade = True
grades = [None]*len(wrapper_list[1])
time.sleep(10)
try:
    grade_outer_table = driver.find_element(By.XPATH, "//*[@id='page-wrapper']/div[2]/div/div/div[3]/div/div/div/table/tbody")
except:
    found_grade = False
else:
    grade_inner_table = grade_outer_table.find_elements(By.TAG_NAME, "tr")
    for rows in grade_inner_table:
        crn = rows.find_elements(By.TAG_NAME, "td")[0].text
        idx = wrapper_list[1].index(crn)
        grades[idx] = rows.find_elements(By.TAG_NAME, "td")[3].text

logout = driver.find_element(By.XPATH, "//*[@id='app']/header/nav/div[2]/ul/li[3]/div[1]/i")
logout.click()

driver.get("https://www.sis.itu.edu.tr/TR/ogrenci/lisans/ders-bilgileri/ders-bilgileri.php")
code_input = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/form/div[1]/input")
number_input = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/form/div[2]/input")
show_button = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/form/input")
first = True
for i in lecture_codes:
    code = i[:3]
    number = i[4:]
    if first == True:
        code_input = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/form/div[1]/input")
        number_input = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/form/div[2]/input")
        show_button = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/form/input")
        code_input.send_keys(code)
        number_input.send_keys(number)
        show_button.click()
        out_table = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/table/tbody/tr/td/table[2]")
        in_tables = out_table.find_elements(By.TAG_NAME, "td")
        lecture_credits.append(in_tables[5].text)
        first = False
    else:
        code_input = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[1]/form/div[1]/input")
        number_input = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[1]/form/div[2]/input")
        show_button = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[1]/form/input")
        code_input.clear()
        code_input.send_keys(code)
        number_input.clear()
        number_input.send_keys(number)
        show_button.click()
        out_table = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div[2]/table/tbody/tr/td/table[2]")
        in_tables = out_table.find_elements(By.TAG_NAME, "td")
        lecture_credits.append(in_tables[5].text)
driver.close()

term_total_credit = 0
for i in lecture_credits:
    term_total_credit += float (i)
