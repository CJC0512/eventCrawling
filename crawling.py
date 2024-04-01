import requests
from bs4 import BeautifulSoup
import json

filePath = './jsonFiles/'
pageNum = 1
i = 1
bCode = '030510001'
url = 'https://www.contestkorea.com/sub/list.php?int_gbn=' + str(pageNum) + '&Txt_bcode=' + bCode

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    contents = soup.select_one('#frm > div > div.list_style_2')
    href_tags = contents.select('ul > li > div > a')

    links = []

    for tag in href_tags:
        href_value = tag['href']
        links.append('https://www.contestkorea.com/sub/' + href_value)

    for link in links:
        insideResponse = requests.get(link)

        if insideResponse.status_code == 200:
            insideHtml = insideResponse.text
            insideSoup = BeautifulSoup(insideHtml, 'html.parser')
            insideComponents = insideSoup.select_one(
                '#wrap > div.container.list_wrap > div.left_cont > div.view_cont_area > div.view_top_area.clfx > div.clfx > div.txt_area')
            insideContent = insideSoup.select_one(
                '#wrap > div.container.list_wrap > div.left_cont > div.view_cont_area > div.tab_cont > div > div')

            data = {}

            # omokevent_p(페이지번호)-(인덱스 번호)
            jsonName = 'omokevent_p' + str(pageNum) + '-' + str(i)
            data[jsonName] = []

            # TODO 자료 정리해서 뽑아와야함.
            data[jsonName].append({
                # "OMOKEVENT_ID": "",
                "ORGANIZATION": insideComponents.select_one('table > tbody > tr:nth-child(1) > td').get_text().replace('\t',''),
                "CATEGORY": insideComponents.select_one('table > tbody > tr:nth-child(2) > td').get_text().replace('\t',''),
                "TARGET_PARTICIPANT": insideComponents.select_one('table > tbody > tr:nth-child(3) > td').get_text().replace('\t',''),
                "APPLY_START_DATE": insideComponents.select_one('table > tbody > tr:nth-child(4) > td').get_text().replace('\t',''),
                "APPLY_END_DATE": insideComponents.select_one('table > tbody > tr:nth-child(4) > td').get_text().replace('\t',''),
                "JUDGE_START_DATE": insideComponents.select_one('table > tbody > tr:nth-child(5) > td').get_text().replace('\t',''),
                "JUDGE_END_DATE": insideComponents.select_one('table > tbody > tr:nth-child(5) > td').get_text().replace('\t',''),
                "ANOUNCEMENT_DATE": "",
                "LOCATION": insideComponents.select_one('table > tbody > tr:nth-child(6) > td').get_text().replace('\t',''),
                "AWARD": insideComponents.select_one('table > tbody > tr:nth-child(7) > td').get_text().replace('\t',''),

                # TODO 여기 링크 뽑아야함.
                "HOMEPAGE": insideComponents.select_one('table > tbody > tr:nth-child(8) > td'),
                "APPLY_PROCESS": insideComponents.select_one('table > tbody > tr:nth-child(9) > td').get_text().replace('\t',''),
                "APPLY_FEE": insideComponents.select_one('table > tbody > tr:nth-child(10) > td').get_text().replace('\t',''),

                # TODO 이미지 잘 가져오는지 확인해야함.
                "POST_IMAGE": insideContent.select_one('div > img').get_text(),
                
                # TODO Content 정리해서 가져와야함
                "CONTENT": insideContent.get_text()
                # "HITS": "",
                # "STATUS": ""
            })

            # TODO JSON 저장해야함
            print(data[jsonName])
            break

        else:
            print('상세정보 조회 실패: ' + str(insideResponse.status_code))

    # index 번호 초기화
    i = 1


else:
    print('목록 조회 실패: ' + str(response.status_code))
