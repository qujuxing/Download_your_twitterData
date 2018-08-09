import re 
import json
import pandas as pd

tweets_file = open('twitter-2018-08-04/tweet.json','r') #打开json文件，从twitter上下载下来的文件，需要简单处理一下，把下载下来的js文件里面的前缀去掉，改文件后缀名为json
tweets_str = tweets_file.read() #将文件读取为string
data = json.loads(tweets_str)  
#print(type(data)) #查看data的类型
#print(data[1]['full_text']) #测试数据是否和想要的数据相符
#print(len(data))
timeStamp = [] #初始化一个list
tweetsFullText = [] 
for i in range(len(data)): #迭代data数据，将json数据里面的时间和内容相关的值赋给两个变量，在压入队列中
    a = data[i]['created_at']
    b = data[i]['full_text']
    timeStamp.append(a)
    tweetsFullText.append(b)
dict = {'created_at':timeStamp,'tweets':tweetsFullText} #构造一个字典，用于生成dataframe
df = pd.DataFrame(data=dict)    
#df.to_csv('tweets_data.csv')  #生成原始未处理的数据，保存为csv文件
#print('the 2715 row is : {}'.format(df.iloc[2715,1])) #实验了一下新学的语法
timeTemp = [] #初始化一个list用于保存处理后的时间的值
weekTemp = [] #初始化一个list用于保存星期的值
for i in df.iloc[:,0]: #遍历df的第一列，即时间的值
    a = re.sub(r'\w{3}','',i,count=1) #正则一个类似'Mon Feb 18 11:55:27 +0000 2008'的string，删除前三个字母，得到后面年月日的值
    b = re.search(r'\w{3}',i).group() #取前三个字母，即星期的值
    timeTemp.append(a) #将时间和星期的值分别压入两个list钟
    weekTemp.append(b)
timeTempPro = pd.to_datetime(timeTemp) #将年月日的值格式化为标准时间显示
#print('time is ',timeTempPro[:2],'\n','week is ', weekTemp[:2] ) #测试下得到的值是否准确
dict_clean = {'created_at':timeTempPro,'week':weekTemp,'tweets':tweetsFullText}  #构造一个dictionary
df_clean = pd.DataFrame(data=dict_clean) #生成dataframe
#df_clean.sort_values(by='created_at',ascending=False) #这个没有成功排序
df_clean.to_csv('tweets_data_clean.csv')

tweets_file.close() #关闭json文件