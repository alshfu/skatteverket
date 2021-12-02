import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


def hate_string():
    hello = "Petros&Company"
    string_1 = "Denna e-verktyg är unik och utvecklad för OPAL-Redovisnings"
    print(hello)
    print(string_1)


def write_row_to_file(row):
    with open('full_info_list.csv', 'a', encoding='utf8') as f:
        f.write("\n")
        f.write(row)
    f.close()


def open_org_nr_page(org_nr, driver):
    driver.find_elements_by_class_name('select-filter')[0].send_keys(org_nr)
    driver.find_elements_by_class_name('select-filter')[0].send_keys(Keys.ENTER)
    time.sleep(2)
    saldo_nmbr_kfm = '0'
    if 'saldo-neg' in driver.find_elements_by_class_name('saldo-nmbr')[0].get_attribute('class'):
        saldo_nmbr = driver.find_elements_by_class_name('saldo-nmbr')[0].text
        saldo_nmbr = saldo_nmbr.replace(" ", "")
        saldo_nmbr = '-' + saldo_nmbr
    else:
        saldo_nmbr = driver.find_elements_by_class_name('saldo-nmbr')[0].text
        saldo_nmbr = saldo_nmbr.replace(" ", "")
    try:
        if 'saldo-neg' in driver.find_elements_by_class_name('saldo-nmbr-kfm')[0].get_attribute('class'):
            saldo_nmbr_kfm = driver.find_elements_by_class_name('saldo-nmbr-kfm')[0].text
            saldo_nmbr_kfm = saldo_nmbr_kfm.replace(" ", "")
            saldo_nmbr_kfm = '-' + saldo_nmbr_kfm
        else:
            saldo_nmbr_kfm = driver.find_elements_by_class_name('saldo-nmbr-kfm')[0].text
            saldo_nmbr_kfm = saldo_nmbr_kfm.replace(" ", "")
    except:
        print('')
    return [saldo_nmbr, saldo_nmbr_kfm]


def get_all_links(url, ss_n):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    ############
    hate_string()
    time.sleep(5)
    mbi_link = driver.find_elements_by_class_name('indexlist')[1]
    mbi_url = mbi_link.find_elements_by_tag_name('a')[0].get_attribute("href")
    driver.get(mbi_url)
    #######################################################
    time.sleep(5)
    os.getcwd()
    driver.find_element_by_id('ssn').send_keys(ss_n)
    driver.find_element_by_id('ssn').send_keys(Keys.ENTER)
    input("Tryck Enter när du klart med inloggningen")
    table = driver.find_elements_by_tag_name('table')[0]
    tbody = table.find_elements_by_tag_name('tbody')[0]
    tr = tbody.find_elements_by_tag_name('tr')
    org_list = []
    for td in tr:
        td = td.find_elements_by_tag_name('td')
        org_nr = td[0].text
        name = td[1].text
        org_list.append([org_nr, name])

    for org in org_list:
        time.sleep(5)
        try:
            saldo = open_org_nr_page(org[0], driver)
            row = str(org[0] + ";" + org[1] + ";" + saldo[0] + ";" + saldo[1])
            write_row_to_file(row)
            print(row)
        except IndexError:
            print("Företag saknar kontoinformation")
        driver.get('https://sso.skatteverket.se/sk/ska/listaKtohavare.do')
        time.sleep(10)

    driver.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    hate_string()
    ssn = input('Ange din persson nummer: ')
    get_all_links('https://sso.skatteverket.se/sk/ska/loggedIn.do', ssn)
