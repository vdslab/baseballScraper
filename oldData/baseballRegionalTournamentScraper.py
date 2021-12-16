import json
import requests
from bs4 import BeautifulSoup
from time import sleep


def getFullSchoolName(url):
    sleep(60)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    fullSchoolName = soup.select_one("#school_info > ul > li > a")
    return fullSchoolName.get_text() if fullSchoolName else None


def main():
    url = "https://www.hb-nippon.com/"
    readFileName = "prefecture.json"
    writeFileName = "baseball.json"
    dict = [
        {
            "year": "2017",
            "data": []
        },
        {
            "year": "2016",
            "data": []
        },
        {
            "year": "2015",
            "data": []
        },
        {
            "year": "2014",
            "data": []
        },
        {
            "year": "2013",
            "data": []
        }
    ]

    with open("./" + readFileName, mode="r", encoding="utf-8") as f:
        prefectureList = json.load(f)

    for prefecture in prefectureList:
        print(prefecture)
        res = requests.get(url + prefecture)
        soup = BeautifulSoup(res.text, "html.parser")

        nameDict = {}
        separatePrefecture = soup.select("#past-results > b")
        if not separatePrefecture:
            separatePrefecture.append(BeautifulSoup(
                "<b>" + prefectureList[prefecture] + "</b>", "html.parser"))
        for i in range(len(separatePrefecture)):
            separateTournaments = soup.select(".table_normal > tbody")
            tournaments = separateTournaments[i].select("tr")
            cnt = 0
            for tournament in tournaments:
                schools = tournament.select("td > a")
                l = len(schools)
                if l < 9:
                    print("fuck")
                for j in range(1, l):
                    # if not nameDict.get(schools[j].get_text()):
                    #     nameDict[schools[j].get_text()] = getFullSchoolName(
                    #         schools[j]["href"]
                    #     )
                    # else:
                    #     print("exist" + str(j))
                    # print("ok")
                    dict[cnt]["data"].append(
                        {
                            "shortName": schools[j].get_text(),
                            # "fullName": nameDict[schools[j].get_text()],
                            "fullName": None,
                            "prefecture": separatePrefecture[i].get_text(),
                            "best": 1 if j <= 1 else (2 if j <= 2 else (4 if j <= 4 else 8))
                        }
                    )
                cnt += 1
            # with open("./" + writeFileName, mode="w", encoding="utf-8") as f:
            #     json.dump(dict, f, indent=2, ensure_ascii=False)
            # exit()

        sleep(120)

    with open("./" + writeFileName, mode="w", encoding="utf-8") as f:
        json.dump(dict, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
