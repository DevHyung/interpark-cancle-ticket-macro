from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import json
from collections import OrderedDict
import time
import datetime
import re

dir = './chromedriver'

def find_seat():
    driver.get('http://ticket.interpark.com/')
    selects = []
    with open("select.txt", "r") as f:
        for data in f.readlines():
            event = data.split(':')
            if event[1][0] == "1":
                selects.append(event[0])
    input(">>> 선택창이 뜬 후에 엔터를 눌러주세요.")

    main_window_handle = None
    while not main_window_handle:
        main_window_handle = driver.current_window_handle
    signin_window_handle = None
    while not signin_window_handle:
        for handle in driver.window_handles:
            if handle != main_window_handle:
                signin_window_handle = handle
                break

    driver.switch_to.window(signin_window_handle)
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmSeat"]'))
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmSeatDetail"]'))

    while True:
        for idx in range(1, 10):
            driver.execute_script("top.ifrmSeat.ifrmSeatDetail.GetBlockSeatList('', '', 'RGN00" + str(idx) + "')")
            time.sleep(0.5)
            while True:
                try:
                    seats = driver.find_element_by_xpath('//*[@id="TmgsTable"]/tbody/tr/td').find_elements_by_class_name('stySeat')
                    break
                except:
                    time.sleep(0.2)
            print(len(seats))
            if int(len(seats)) == 0:
                break

            for seat in seats:
                try:
                    alt = str(seat.get_attribute('alt'))
                except:
                    alt = ""
                    pass
                for select in selects:
                    if str(select) in alt:
                        try:
                            print("있다!")
                            # seat.click()
                        except:
                            continue
                        #클릭창 넘어가는거
                        # time.sleep(0.5)
                        # driver.switch_to.default_content()
                        # driver.switch_to.window(signin_window_handle)
                        # driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="ifrmSeat"]'))
                        # driver.find_element_by_xpath('/html/body/form[1]/div/div[1]/div[3]/div/div[4]/a').click()
                        # return

    #마무리 페이지로 가는겨
    # driver.switch_to.window(main_window_handle)



if __name__ == "__main__":
    driver = webdriver.Chrome(dir)
    driver.maximize_window()
    main_cnt = 1
    find_seat()

