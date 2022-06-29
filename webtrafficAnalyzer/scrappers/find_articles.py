import os, sys
import sys
import socket
from selenium import webdriver, common
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import logging
from time import sleep

class BasicBot:
    def TestInternet(self):
        #testing the Internet connection
        try:
            socket.setdefaulttimeout(3)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('8.8.8.8', 53))
            return True
        except socket.error:
            return False

    def loadDriver(self, link):
        #pulls the html from a site specified by the link and returns a bs4 object
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get(link)
            sleep(3)
            print(f"[+] Page {link} loaded succsecfully.")
            return driver
        except common.exceptions.WebDriverException:
            #failing to pull the html will arrise from no internet connection or an invalid link
            if self.TestInternet():
                #If the Link is invalid the program is conntinued with an error message
                logging.error(f"[-] Failed to connect to {link}. Invalid link.")
            else:
                #If the Inter stopped working the program is quit
                sys.exit(f"[-] Failed to connect to {link}. No Internetconnection.")

def Scrap_all(searchterm):
    number_found = []
    for doc in os.listdir('cleaned_lists'):
        with open(os.path.join('cleaned_lists', doc)) as file:
            total = 0
            for line in file.readlines():
                link = line.split(',')[0]
                if link != '':
                    try:
                        driver = BasicBot().loadDriver(link)
                        try:
                            driver.find_element(By.XPATH, f"//*[contains(text(),'{searchterm}')]")
                            total += 1
                        except common.exceptions.NoSuchElementException:
                            print('None found')
                        driver.quit()
                    except:
                        pass
            print(total)
            number_found.append(total)
            break
    return number_found


if __name__ == '__main__':
    Scrap_all('e')
    sys.exit('[+] finished')