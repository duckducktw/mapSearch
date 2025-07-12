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
    result_duv = soup.select('.bfdHYd')

    print(result_name)

    results = []

    if "DUwDvf" not in driver.page_source:
        for i in range(len(result_name)):
            if( result_duv[i].select_one('.lcr4fd')):
                results.append({
                    "name": result_name[i].text,
                    "address": result_link[i]['href'].split('!3d')[1].split('!4d')[0] + ", " + result_link[i]['href'].split('!4d')[1].split('!16s')[0],
                    "web": result_duv[i].select_one('.lcr4fd')['href']
                })
            else:
                results.append({
                    "name": result_name[i].text,
                    "address": result_link[i]['href'].split('!3d')[1].split('!4d')[0] + ", " + result_link[i]['href'].split('!4d')[1].split('!16s')[0], 
                    "web": None
                })
    elif soup.select('.lfPIob'):
        while "/place/" not in driver.current_url:
            pass
        print(soup.select_one('#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(7) > div:nth-child(5) > a'))
        if (soup.select_one('#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(7) > div:nth-child(5) > a')):
            results.append({
                "name": soup.select_one('.lfPIob').text,
                "address": driver.current_url.split('/@')[1].split(',')[0] + ", " + driver.current_url.split(',')[1].split(',')[0],
                "web": soup.select_one('#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(7) > div:nth-child(5) > a')['href']
            })
        else:
            results.append({
                "name": soup.select_one('.lfPIob').text,
                "address": driver.current_url.split('/@')[1].split(',')[0] + ", " + driver.current_url.split(',')[1].split(',')[0]
            })
    else:
        results.append({"message": "No results found"})

    driver.quit()
    return results