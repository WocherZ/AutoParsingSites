from selenium import webdriver
import time
# import sys
# import io
#
# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
# sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


url = "https://fortis-development.ru/flats?result_mode=0&complex_visual_mode=0&property_visual_mode=1&is_free=1&complex=1"
driver = webdriver.Chrome(executable_path=r'C:\Users\woche\PycharmProjects\AutoParsing\chromedriver\chromedriver.exe')

try:
    #driver.maximize_window()
    driver.get(url=url)
    time.sleep(5)
    pageSource = driver.page_source.encode(encoding='utf-8')  # html code
    fileToWrite = open("page_source.html", "w")
    # f = driver.find_elements_by_class_name("container")
    # print(f[0].text)
    fileToWrite.write(str(pageSource))
    fileToWrite.close()

    time.sleep(2)

    # fileToRead = open("page_source.html", "r")
    # print(fileToRead.read())
    # fileToRead.close()


except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

print("End")
