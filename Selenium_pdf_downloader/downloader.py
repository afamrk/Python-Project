import os
import sys
import pkg_resources
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import keyboard
from PIL import Image
import winsound
import os
import shutil
import img2pdf
from selenium.webdriver.common.action_chains import ActionChains
import warnings
import click

header = """

██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗ 
██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║█████╗  ██████╔╝
██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║██╔══╝  ██╔══██╗
██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║
╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                                                                                                     

"""


dependencies = [
    'img2pdf>=0.4.3',
    'keyboard>=0.13.5',
    'Pillow>=7.2.0',
    'pip>=22.0.4',
    'selenium>=4.1.3',
    'click>=8.0.3'
]

try:
    pkg_resources.require(dependencies)
except:
    print(sys.exc_info())
    os.system(('pip install -r requirments.txt'))


warnings.filterwarnings("ignore")


def image_resize(name, full_location, title):
    imgOpen = Image.open(full_location)
    x, y, height, width = 615, 100, 1000, 1300 #left,top,bottom,right
    imgOpen = imgOpen.crop((x, y, width, height))
    full_path = os.path.join(os.getcwd(),title,'cropped')
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    full_path = os.path.join(full_path,f'{name}')
    imgOpen.save(full_path)

def take_screen_shot(driver, number):
    title = driver.find_element(By.XPATH, '//*[@id="lesson-player"]/section[1]/div[2]/div[2]/div/div/h3').text.replace(
        ' ', '_')
    loc = os.path.abspath(title)
    if os.path.exists(loc):
        shutil.rmtree(loc)
    os.mkdir(loc)

    for i in range(number):
        name = f"{title}_screenshot{i}.png"
        full_loc = os.path.join(loc,name)
        driver.save_screenshot(full_loc)
        driver.find_element(By.CSS_SELECTOR,'body').send_keys(Keys.ARROW_RIGHT)
        time.sleep(2)
        image_resize(name, full_loc, title)
    convert_to_pdf(title)
    winsound.Beep(440, 1000)
    zoomout_class = driver.find_element(By.CLASS_NAME, 'css-80zh1h').find_elements(By.XPATH, './..')[0].get_attribute(
        'class')
    driver.find_element(By.CSS_SELECTOR,
                        f'div:nth-child(1) > div > div:nth-child(1) > div > div > div > div > div > div.{zoomout_class} > div.sth-header.css-80zh1h > div:nth-child(2) > div:nth-child(3) > i > svg').click()

def convert_to_pdf(title):
    full_path = os.path.join(os.getcwd(), title, 'cropped')
    with open(f"{title}.pdf", "wb") as f:
        files = sorted(os.listdir(full_path),key=lambda name: int(name.split('screenshot')[1].split('.')[0]))
        all_files = [os.path.join(full_path,i) for i in files if i.endswith(".png")]
        f.write(img2pdf.convert(all_files))

def semi_auto(driver):
    try:
        driver.find_element(By.CLASS_NAME, 'css-f1ogtk').click()
        driver.find_element(By.CLASS_NAME, 'css-f1ogtk').click()
        driver.find_element(By.CLASS_NAME, 'css-f1ogtk').click()
    except:
        pass
    time.sleep(5)
    driver.execute_script("document.querySelector('.css-z2cbq5').style")
    driver.execute_script("document.querySelector('.css-z2cbq5').style.opacity=1")
    zoomin_class = driver.find_element(By.CLASS_NAME, 'css-80zh1h').find_elements(By.XPATH, './..')[0].get_attribute(
        'class')
    driver.find_element(By.CSS_SELECTOR,
                        f'div:nth-child(1) > div > div:nth-child(1) > div > div > div > div > div > div.{zoomin_class} > div.sth-header.css-80zh1h > div:nth-child(2) > div:nth-child(3) > i > svg').click()
    time.sleep(1)
    second_class = driver.find_element(By.CLASS_NAME, 'css-1iayim9').find_elements(By.XPATH, './..')[0].get_attribute(
        'class')
    first_class = driver.find_element(By.CLASS_NAME, second_class).find_elements(By.XPATH, './..')[0].get_attribute(
        'class')
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,
                        f'#lst-lesson-player > div:nth-child(1) > div > div:nth-child(1) > div > div > div > div > div > div.{first_class} > div.{second_class} > div.css-1iayim9 > div > div.pdf-zoom.css-y40kdn > div.css-13353yy > div').click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR,
                        f'#lst-lesson-player > div:nth-child(1) > div > div:nth-child(1) > div > div > div > div > div > div.{first_class} > div.{second_class} > div.css-1iayim9 > div > div.pdf-zoom.css-y40kdn > div.css-13353yy > div.zoom-bar.css-1udphy4 > div:nth-child(3)').click()
    time.sleep(2)
    num = driver.find_element(By.CLASS_NAME, 'css-15kkuz5').text.replace('of ', '')
    time.sleep(5)
    driver.execute_script("document.querySelector('.css-z2cbq5').style.opacity=0")
    time.sleep(1)
    take_screen_shot(driver,int(num))

def down_urls(driver, urls,completed):

    for url in urls:
        driver.get(url)
        time.sleep(2)
        semi_auto(driver)
        completed.append(url)


def login(driver):
    # enter your mail id here
    mail = "############"
    # enter passwd here
    passw = '##########'
    driver.get("#### URL ########")
    driver.maximize_window()
    time.sleep(2)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "// *[ @ id = 'bs-example-navbar-collapse-1'] / ul / li"))).click()
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mynav"]/li[1]/a'))).click()
    username = driver.find_element(By.XPATH, '//*[@id="nav_signin_email"]')
    password = driver.find_element(By.XPATH, '//*[@id="nav_signin_pwd"]')
    time.sleep(1)
    username.send_keys(mail)

    password.send_keys(passw)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="sigupForm"]/form/input[3]').click()
    time.sleep(2)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//*[@id="root-identifier-collection"]/div[1]/div/div[2]/div/div[2]/div[1]/div/div[2]/div'))).click()

    time.sleep(1)
    return


def main():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--deny-permission-prompts')
        options.add_argument('log-level=5')
        chrome_driver_binary = r'chromedriver.exe'
        driver = webdriver.Chrome(chrome_driver_binary, options=options)
        action = ActionChains(driver)
        driver.implicitly_wait(100)  # seconds

        filename = 'urls.txt'
        with open(filename) as f:
            urls = [line.strip() for line in f]
        login(driver)
        completed = []
        down_urls(driver,urls, completed)

    except:
        raise
    finally:
        click.clear()
        print(header)
        print()
        print(f'{"COMPLETED":>35}\n'+'#'*70)
        print()
        for index,url in enumerate(completed):
            print(f'{index+1}) {url} => ✅')
        driver.quit()

if __name__ == "__main__":
    print(header)
    print("#" * 100)
    main()



