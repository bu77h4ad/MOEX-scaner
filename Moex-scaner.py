import proxy_parser
import json
import time
from sys import argv
import requests
import csv
from bs4 import BeautifulSoup
import requests
import telebot


'''
MarkdownV2 style
To use this mode, pass MarkdownV2 in the parse_mode field. Use the following syntax in your message:

*bold \*text*
_italic \*text_
__underline__
~strikethrough~
*bold _italic bold ~italic bold strikethrough~ __underline italic bold___ bold*
[inline URL](http://www.example.com/)
[inline mention of a user](tg://user?id=123456789)
`inline fixed-width code`
```
pre-formatted fixed-width code block
```
```python
pre-formatted fixed-width code block written in the Python programming language
```
'''


#Global Varibles
freq = '4'
TFtitle = '3600'
TF = '3600'
forse   = False
indices = False
stocks  = False
disable_notification = False

TFstring = ['3600','86400','week']
for i in range(0,len(TFstring)):
	if TFstring[i] in argv:
		TF = TFstring[i]		

if '-forse' in argv:
	forse = True

if '-indices' in argv:
	indices = True

if '-stocks' in argv:
	stocks = True

if '-disable_notification' in argv:
	disable_notification = True

print(argv)
#print(TF)
urlBot     = "https://api.telegram.org/bot546038157:AAHZLzQbE-wNix_UWLTE-6vV_m5YfMB1Vpw/"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
proxy123 = proxy_parser.proxy_parser() 
proxy123.get_proxies('https',1)
proxy_now = {
	#'https': '206.221.176.130:3128' # work
	#'https': '51.161.116.223:3128' # work
	#'https':'157.245.222.183:80' 
}

#Functions
def send_message( chat_id , text, parse_mode='Markdown', disable_notification=disable_notification, disable_web_page_preview=True ):  
    params = {
    	'chat_id': chat_id, 
    	'text': text, 
    	'parse_mode': parse_mode, 
    	'disable_notification': disable_notification, 
    	'disable_web_page_preview':disable_web_page_preview
    	}
    response = requests.post(urlBot + 'sendMessage', data=params)
    return response
#send_message(375937375, "☑  TimeFrame: \#1Hour ")
def send_photo(chat_id, photo, caption=None, disable_notification=False, reply_to_message_id=None, reply_markup=None, timeout=20, parse_mode=None, fileb=None, **kwargs):

	params = {'chat_id':chat_id, 'photo':photo}
	response = requests.post(urlBot + 'sendPhoto', data=params)
	print(kwargs)
	return response
#send_photo(375937375,'https://node.finam.ru/imcf3.asp?id=81820&type=3&ma=1&maval=&freq=4&uf=1&indval=&cat=4&cai=14&v=&idxf=&curr=0&mar=1&gifta_mode=1')

def getRSI( pair_id, period=TF ):
	#	1h = period=3600 | 1d = 86400 | 1week = week
	#	pairID=44465&period=18000&viewType=normal
	header = {
	'X-Requested-With': 'XMLHttpRequest',
	'User-Agent': user_agent,
	}
	print (period)
	params = {'pairID': pair_id, 'period': period, 'viewType': 'normal'}
	
	#response = requests.post('https://ru.investing.com/instruments/Service/GetTechincalData' , headers=header, data=params, proxies=proxy_now).content.decode() 
	while True:
		try:
			response = requests.post('https://ru.investing.com/instruments/Service/GetTechincalData' , headers=header, data=params, proxies=proxy_now).content.decode() 
		except Exception:
			alert= "Не удалось подключиться к сайту или что то пошло не так. текуший IP " + str(proxy_now)
			print(alert)
			send_message(375937375, alert)			
			proxy_string = proxy123.next_proxy()
			proxy_now.update({'https': proxy_string['ip']+ ':'+ proxy_string['port']})		
			continue

		if response.find('406 Not Acceptable') != -1:
			alert = '406 Not Acceptable\tСайт забанил бота. Время менять IP. текуший IP '+ str(proxy_now)
			print (alert)
			send_message(375937375, alert)			
			proxy_string = proxy123.next_proxy()
			proxy_now.update({'https': proxy_string['ip']+ ':'+ proxy_string['port']}) 									
			continue

		break

	print (proxy_now)
	soup = BeautifulSoup(response, 'lxml')

	soup = soup.findAll("table", { 'class':"genTbl closedTbl technicalIndicatorsTbl smallTbl float_lang_base_1" })[0]	# нашел таблицу с тех инфой

	RSI =  float(soup.findAll("td")[1].text.replace(',','.').strip())	# спарсил RSI из таблицы
	time.sleep(3)	
	return round(RSI)

def getStockInIndices(IDX = "https://ru.investing.com/indices/mcx-components"):
	r = requests.get ( IDX, headers={'User-Agent': user_agent} ).content.decode() 	

	#openIMOEX =  soup.findAll("div", { 'class':"bottom lighterGrayFont arial_11" })[0] # 	открыта ли биржа	
	if forse != True:
		if r.find(" - Закрыт. Цена в ") != -1:
			print ( "\nБиржа закрыта, точнее сайт инвестинг не предоставляет котировки н данный момент")
			send_message(375937375, "Биржа закрыта, точнее сайт инвестинг не предоставляет котировки н данный момент")
			quit()
		else:
			print ( "\nБиржа открыта")	
			send_message(375937375, "Биржа открыта")	
		
	
	soup = BeautifulSoup(r, 'lxml')	
	soup =  soup.findAll("table", { 'id':"cr1" })[0].findAll("tbody")[0] # парсим таблицу с акциями
	#print(a.prettify())	
	
	tr = soup.findAll("tr")	# спарсил строки из таблицы
	#print("\n\n\n\n tr -  ", tr[1].get('id'), "\n")	

	names=[] 
	titles = []
	prices =[]
	pair_ids = []
	for i in range(0, len(tr)):
		a =  tr[i].findAll("a",  { 'href':True, "title":True, 'target': False })[0] # спарсил ссылку
		td = tr[i].findAll("td")[2] 												# спарсил цену
		#print("\n <A> - ", a, "\n")
		#print("\n <td> - ", td, "\n")

		name = a.get('href').replace('/equities/','').split('?')[0]
		title = a.text
		price = td.text.replace('.',' ')
		pair_id = tr[i].get('id').replace('pair_','')

		print (name, title, price ,pair_id)

		names.append(name)
		titles.append(title)	
		prices.append(price)
		pair_ids.append(pair_id)	
	return names, titles, prices, pair_ids

def getIndex( name = 'mcx'):
	dictionary={}
	r = requests.get ( 'https://ru.investing.com/indices/'+name, headers={'User-Agent': user_agent} ).content.decode('UTF-8') 	
	soup = BeautifulSoup(r, 'lxml')		
	title =  soup.findAll("h1", { 'class':"float_lang_base_1 relativeAttr" })[0].text.strip() # тайтл парсинг
	string =  soup.findAll("div", { 'class':"top bold inlineblock" })[0].text.strip().replace('.',' ').replace(',','.').split('\n')	
	price = string[0]
	percent1day = string[-1]
	pair_id =  soup.findAll("div", { 'class':"headBtnWrapper float_lang_base_2 js-add-alert-widget" })[0].get('data-pair-id')

	dictionary.update( { 'title':title, 'price':price , 'percent1day': percent1day, 'pair_id':pair_id } )

	
	time.sleep(3)	
	return dictionary

#BODY

dict_finam =  { "mcx":420450, "rtsi":420445, 'yevroplan-pao':491359 , 'x5-retail-grp':491944, 'alrosa-ao':81820, 'aeroflot':29, 'vtb_rts':19043, "gazprom_rts":16842, "pik_rts":18654, "detskiy-mir-pao":473181,"inter-rao-ees_mm":20516, 
		"lukoil_rts":8, "mvideo_rts":19737,"magnit_rts":17086,"sg-mechel_rts":21018, "moskovskiy-kreditnyi-bank-oao":420694, "mmk_rts":16782, "moskovskaya-birzha-oao":152798, "mts_rts":15523, 
		"nlmk_rts":17046, "nmtp_rts":19629, "novatek_rts":17370, "gmk-noril-nickel_rts":795, "npk-ovk-pao":414560, "polymetal":175924, "polyus-zoloto_rts":17123, "ros-agro-plc":399716, "rosneft_rts":17273,
		"rosseti-ao":20971, "rostelecom":7, "united-company-rusal-plc`":414279, "gidroogk-011d":20266, "ruspetro":465236, "sberbank_rts":3, "sberbank-p_rts":23, "severstal_rts":16136,
		"afk-sistema_rts": 19715, "surgutneftegas_rts":4, "surgutneftegas-p_rts":13, "tatneft_rts": 825, "tatneft-p_rts": 826, "tmk":18441,"transneft-p_rts":1012,"phosagro":81114,
		"fsk-ees_rts":20509, "e.on-russia":18584, "yandex":388383}

if TF=='3600':
	TFtitle   = '#1Hour'
	freq = '4'
if TF=='86400':
	TFtitle   = '#1Day'
	freq = '5'
if TF=='week':
	TFtitle   = '#1Week'
	freq = '6'	
post = '☑  TimeFrame: ' + TFtitle + ' '

if indices == True:
	indexArray=['mcx','rtsi'] #13666 13665 - PTS
	#title, price, percent1day = 
	post = post + '\n#Индексы'
	for i in range(0,len(indexArray)):
		IDX  = getIndex(indexArray[i])	
		if IDX['pair_id'] == "13666":
			IDX['title'] = 'ММВБ'
		if IDX['pair_id'] == "13665":
			IDX['title'] = 'РТС'

		post = post + '\n   [' +IDX['title']+ '](https://node.finam.ru/imcf3.asp?id='+ str(dict_finam[indexArray[i]]) + '&type=3&ma=2&maval=14&freq=' + freq+ '&uf=1&indval=&cat=4&cai=14&v=&idxf=&curr=0&mar=1&gifta_mode=1): ' +IDX['price']+ '   rsi:' + str( getRSI(IDX['pair_id']) )

if stocks == True:
	names, titles, prices, pair_ids = getStockInIndices()
	RSIs =[]
	targets=[]
	
	for i in range(0, len(names)):

		print(titles[i], prices[i] )
		RSI = getRSI(pair_ids[i], TF)
		RSIs.append(RSI)
		print(RSI)

		if  RSI < 30:
			targets.append(i)
	if len(targets) != 0 :
		post = post + '\n#АкцииПерепроданы'
	for i in range(0,len(targets)) :				
			stringSkobka=''
			stringLink=''
			if names[targets[i]] in dict_finam :	#Если такой ключ есть в словаре, то делаем ссылку на график	
				stringSkobka='['
				stringLink='](https://node.finam.ru/imcf3.asp?id='+ str(dict_finam[names[targets[i]]]) + '&type=3&ma=2&maval=14&freq=' + freq+ '&uf=1&indval=&cat=4&cai=14&v=&idxf=&curr=0&mar=1&gifta_mode=1): '
				pass
			post = post + '\n   ' + stringSkobka + titles[targets[i]] + stringLink + prices[targets[i]] + 'р   rsi:'+ str(RSIs[targets[i]]) + '  '		
			#
			#	post = post + '[real_time](https://node.finam.ru/imcf3.asp?id='+ str(dict_finam[names[targets[i]]]) + '&type=3&ma=2&maval=14&freq=' + freq+ '&uf=1&indval=&cat=4&cai=14&v=&idxf=&curr=0&mar=1&gifta_mode=1) '

	if len(targets) != 0:
		print ("Send message\n post", post)
		#print(send_message(375937375 ,  post ).content)
	else:
		print ("Send message\n нет перепроданностей")
		send_message(375937375,  "нет перепроданностей" )

		
if '\n' in post : #Если в посте есть что то кроме шапки то отправляем смс
	print(send_message(-1001185231809 ,  post ).content)
	#post = post + '[real_time](https://node.finam.ru/imcf3.asp?id='+ str(dict_finam['mcx']) + '&type=3&ma=2&maval=14&freq=' + freq+ '&uf=1&indval=&cat=4&cai=14&v=&idxf=&curr=0&mar=1&gifta_mode=1) \n'

# 375937375 мой ид  ; -1001185231809 группа
