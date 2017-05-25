### Auto Forex Monitor with Facetime-Alarm 

This is used for monitoring foreign exchange rate and alarm automatically when it achieve certain threshold, threshold can be changed.    

There are two apple scripts called in python, one is to display notification, another is call the Facetime.    

#### Requirements

* MacOS VERSION >10.09
* Python 3 at least 3.4
* Beautiful Soup
* Requests

#### Running Auto Forex Monitor

1. Put two apple scripts on your `home` directory

2. To run the Monitor:

   ```python
   python3 forexAlarm.py
   ```




#### Some Detail    

I use request libraries to parse the HTML and I extract some info using regular expression, luckily some of the real time forex can be accessed from the website API, which I simply using JSON parser to get the data. One thing need to notice is, if you access the page too frequently like 10 times/second, the website will block your IP address, which I am now trying to use multi thread and  establish an IP pool to solve this problem. Currently I suggest let the program sleep several seconds every time after access. 




#### ScreenShots 

You can change the growing rate here :

![Imgur](http://i.imgur.com/StjYR1h.png) 

And modify your iphone number here:

![Imgur](http://i.imgur.com/OiwRMG0.png)

Additionally, there is a method implemented to send email when alarm triggered:

![Imgur](http://i.imgur.com/WVWHtjl.png)

