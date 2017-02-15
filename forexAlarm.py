####-------Producer: wasamisam0119--------#   
import sys
import time
import requests
from bs4 import BeautifulSoup
import re
import os
import smtplib
from email.mime.text import MIMEText  
from email.header import Header
  
mail_host = "smtp.163.com" #Your mail sever host, this is an example
user = 'xxx'
password = 'xxx'
sender = 'xxx@xxx.com'# 发件人邮箱(最好写全, 不然会失败)
receivers = ['xxx@xxx.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
title = 'Rate Alarm'  # 邮件主题

def sendEmail(user, mailmsg):
    content = mailmsg
    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = sender
    message['To'] = ",".join(receivers)
    message['Subject'] = title
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信
    smtpObj.login(user, password)  # 登录验证
    smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
    print("mail has been send successfully.")


def getRate(item):
    content = requests.get(item).text
    return float(re.search(r"\d+.\d+",content).group())

def intrate(item):
    return float(re.search(r"\d+\.?\d*", item).group())


def ringAlarm(rate):
    os.system("osascript ~/alarm.scpt" + " " + str(rate))
    os.system("osascript ~/alarm1.scpt")

pound = "http://www.x-rates.com/calculator/?from=GBP&to=CNY&amount=1"
dollar = "http://www.x-rates.com/calculator/?from=USD&to=CNY&amount=1"
currency=["GBP","EUR","XAU","USX"]
gbptousd="https://www.easymarkets.com/chartsweb/ChartsHandler.ashx?mn=getLastRate&buyCurrency=GBP&sellCurrency=USD&productType=3&uid=1"
eurtousd="https://www.easymarkets.com/chartsweb/ChartsHandler.ashx?mn=getLastRate&buyCurrency=EUR&sellCurrency=USD&productType=3&uid=1"

def getrateArray(currArray):
    price=[]
    for item in currArray:
        url="https://www.easymarkets.com/chartsweb/ChartsHandler.ashx?mn=getLastRate&buyCurrency="+item+"&sellCurrency=USD&productType=3&uid=1"
        price.append(getRate(url))
    return dict(zip(currArray,price))


def getGold():
    string = "http://data-asg.goldprice.org/GetData/USD-XAU/1"
    req = requests.get(string).text
    responseJson = json.loads(req)
    # print(responseJson.get("f")[1].get("f"))
    return responseJson[0]
i = 0
j = 0
goldPrice = getGold()
startRate = getRate(gbptousd)
alarm_goldh = float(goldPrice[8:]) * 1.0010
alarm_goldl = float(goldPrice[8:]) * 0.9990
alarm_rateh = startRate * 1.0008
alarm_ratel = startRate * 0.9992
while i < 3 and j < 3:
    forexDict=getrateArray(currency)
    print(forexDict)
    print("\n")
    #mailmsg = "\r\n\r\n".join(["\r\n", time.strftime(
    #   '%Y-%m-%d %H:%M', time.localtime(time.time())) + " 英镑 " + textRate[0] + " 美元 " + textRate[1]])
    if forexDict['XAU'] <= 1200 or forexDict['XAU'] >= 1230:
        sendEmail(user, mailmsg)
        ringAlarm("大事不好，GOLD机会来了！")
        time.sleep(35)
        i += 1
        continue
    elif forexDict['GBP']<=alarm_ratel or forexDict['GBP']>=alarm_rateh or forexDict['XAU']>alarm_goldh or forexDict['XAU']<alarm_goldl:
        ringAlarm(forexDict['GBP'])
        time.sleep(12)
        alarm_goldh*=1.0012
        alarm_goldl*=0.9988
        alarm_rateh*=1.0015
        alarm_ratel*=0.9985
        j+=1
    else:
        time.sleep(10)

