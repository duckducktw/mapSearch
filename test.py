from selenium import webdriver
from bs4 import BeautifulSoup
import time
import fastapi

app = fastapi.FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Map Search API"}

@app.get("/search")
def search_maps(search: str):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/maps/search/" + search)

    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    result_name = soup.select('.qBF1Pd')
    result_link = soup.select('.hfpxzc')

    results = []

    if soup.select('.qBF1Pd'):
        for i in range(len(result_name)):
            results.append({
                "name": result_name[i].text,
                "address": result_link[i]['href'].split('!3d')[1].split('!4d')[0] + ", " + result_link[i]['href'].split('!4d')[1].split('!16s')[0]
            })
    elif soup.select('.lfPIob'):
        while "/place/" not in driver.current_url:
            pass
        results.append({
            "name": soup.select_one('.lfPIob').text,
            "address": driver.current_url.split('/@')[1].split(',')[0] + ", " + driver.current_url.split(',')[1].split(',')[0]
        })
    else:
        results.append({"message": "No results found"})

    driver.quit()
    return results
"""
search = input("Enter search term: ")

driver = webdriver.Chrome()
driver.get("https://www.google.com/maps/search/" + search)

time.sleep(2)

soup = BeautifulSoup(driver.page_source,"html.parser")

result_name = soup.select('.qBF1Pd')
result_link = soup.select('.hfpxzc')

if(soup.select('.qBF1Pd')):
    for i in range(len(result_name)):
        print(result_name[i].text)
        print(result_link[i]['href'].split('!3d')[1].split('!4d')[0], result_link[i]['href'].split('!4d')[1].split('!16s')[0])
elif (soup.select('.lfPIob')):
    print(soup.select_one('.lfPIob').text)
    while "/place/" not in driver.current_url:
        pass
    print(driver.current_url.split('/@')[1].split(',')[0], driver.current_url.split(',')[1].split(',')[0])

else:
    print("No results found")
"""