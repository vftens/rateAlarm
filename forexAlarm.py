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

def sendEmail(mailmsg):
	content = mailmsg
	message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
	message['From'] = sender
	message['To'] = ",".join(receivers)
	message['Subject'] = title
	smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信 open SSL
	smtpObj.login(user, password)  # 登录验证 login auth
	smtpObj.sendmail(sender, receivers, message.as_string())  # 发送  send 
	print("mail has been send successfully.")
#except smtplib.SMTPException as e:
 #   print(e)
def textrate(item):
	content = requests.post(item).text	#parse webpage
	soup = BeautifulSoup(content,"lxml")
	textRate=soup.find('span', {'class': 'ccOutputRslt'}).text 
	return textRate

def intrate(item):
	return float(re.search(r"\d+\.?\d*",item).group()) #get rate of type float

def ringAlarm(rate):
	os.system("osascript /Users/Sam_Du/alarm.scpt"+" "+rate)	#run applescript to call FaceTime
	os.system("osascript /Users/Sam_Du/alarm1.scpt")			#for simulate the mouse click

pound="http://www.x-rates.com/calculator/?from=GBP&to=CNY&amount=1"	#GBP TO CNY
dollar="http://www.x-rates.com/calculator/?from=USD&to=CNY&amount=1" #USD TO CNY
gbptousd="http://www.x-rates.com/calculator/?from=GBP&to=USD&amount=1"	#GBP TO USD
array=[pound,dollar,gbptousd]
i=0	#counter
while i<5:	#alarm will not excess 5 times, otherwise its too noisy
	textRate=list(map(textrate,array))
	intRate=list(map(intrate, textRate))
	print (textRate) #for check reason
	mailmsg = "\r\n\r\n".join(["\r\n",time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))+" 英镑 "+textRate[0]+" 美元 "+textRate[1]])
	if intRate[0]<=8.12 or intRate[0]>=8.33: #this can set by yourselves
		ringAlarm("大事不好，机会来了！")# Ring FaceTime. Shit! Hurry up! Your Fortune comes!
		sendEmail(mailmsg)	#send email to your box
		time.sleep(45)
		i+=1
		continue
	elif intRate[0]<=8.3 or intRate[0]>=8.28:
		sendEmail(user,mailmsg)
		ringAlarm(textRate[0])
		time.sleep(30)
		continue
	else:
		time.sleep(15)

