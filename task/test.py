from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import random as rn
import sqlite3 as sq
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

def creardb():
    connection = sq.connect('respuestas.db')
    cursor = connection.cursor()
    cursor.execute("Create table answers (question TEXT,answer TEXT)")
    connection.close()
def adicionar(qs, ans):
    connection = sq.connect('respuestas.db')
    cursor = connection.cursor()
    cursor.execute("Insert into answers values (?,?)",(qs, ans))
    connection.commit()
    connection.close()
def getanswer(s):
    connection = sq.connect("respuestas.db")
    cursor = connection.cursor()
    cursor.execute("Select answer from answers where question like ?", (s,))
    c = cursor.fetchall()
    connection.close()
    return c
def delete(qs):
    connection = sq.connect('respuestas.db')
    cursor = connection.cursor()
    cursor.execute("Delete From answers where question like (?)",(qs,))
    connection.commit()
    connection.close()
br = webdriver.Chrome()

url = "https://www.daypo.com/repaso-inf272.html#test"
br.get(url)
def getnumpreguntas():
    time.sleep(1)
    cant = br.find_element_by_id("datos").find_element_by_class_name("ma").find_elements(By.TAG_NAME, "td")
    return int((cant[1].text).split("/")[1])

def findout(n,ch):
    time.sleep(1)
    npreguntas = getnumpreguntas()
    for a in range(n):
        time.sleep(1)
        for i in range(npreguntas):
            question = br.find_element_by_id('pri1').text
            table = br.find_element_by_id('cuestiones1').find_element_by_class_name("w")
            rows = table.find_elements(By.TAG_NAME, "tr")
            ln = len(rows)
            k = ch
            if("seleccione 3" in question):
                k = 3
            if("seleccione 2" in question):
                k = 2
            c = getanswer(question)
            if(len(c) != 0):
                k = len(c)
            option = rn.sample(range(ln), k)
           
            answ = []
            nrop = 0
            for row in rows:
                b =True
                col = row.find_elements(By.TAG_NAME, "td")
                btn = col[1]
                text = col[2].text
                if(len(c) > 0):
                    b = False
                    for j in c:
                        r = j[0]
                        if(r == text):
                            btn.click()
                elif(nrop in option):
                    answ.append(text)
                    btn.click()
                nrop+=1
            br.find_element_by_id('boton').click()
            correct = br.find_element_by_css_selector("div.fwb.tac.w").text
            if(correct == "C o r r e c t o" and b):
                for l in range(k):
                    adicionar(question,answ[l])
            if(correct != "C o r r e c t o" ):
                 print(question)
                 time.sleep(5)
            br.find_element_by_id('boton').click()
        br.get("https://www.google.com/")
        br.get(url)
def answering():
    time.sleep(1)
    n = getnumpreguntas()
    for i in range(n):
        question = br.find_element_by_id('pri1').text
        table = br.find_element_by_id('cuestiones1').find_element_by_class_name("w")
        rows = table.find_elements(By.TAG_NAME, "tr")
        c = getanswer(question)
        for row in rows:
            col = row.find_elements(By.TAG_NAME, "td")
            btn = col[1]
            text = col[2].text
            if(len(c) > 0):
                for i in c:
                    r = i[0]
                    if(r == text):
                        btn.click()
        br.find_element_by_id('boton').click()
        time.sleep(rn.randrange(2,4))
        br.find_element_by_id('boton').click()

if (__name__ == "__main__"):
    answering()