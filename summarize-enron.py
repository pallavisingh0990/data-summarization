import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

senderDict = {}
recipientDict = {}
line=[]

# Read the file
fileName = sys.argv[1]

with open(fileName, 'r') as f:
    reader = csv.reader(f)
    line = list(reader)
inputData = np.array(line)[:,[0,2,3]]

for x in inputData:
    sender = x[1]
    recipient = x[2]
    recipientList = recipient.split('|')
    if sender in senderDict:
        senderDict[sender] =  senderDict[sender] + len(recipientList)
    else: 
        senderDict[sender] = len(recipientList)
    for x in recipientList:
        if x in recipientDict:
            recipientDict[x] = recipientDict[x] + 1
        else:
            recipientDict[x] = 1

sortedSenderDict = sorted(senderDict.items(), key=lambda x: x[1], reverse=True)
sortedRecipientDict = sorted(recipientDict.items(), key=lambda x: x[1], reverse=True)       

#delete the files in target folder
targetFiles = glob.glob('target/*')
for f in targetFiles:
    os.remove(f)

#Requirement 1
#Writing into the file named output1.csv
oFile = open('target/output1.csv', 'a')
oFile.truncate(0)
oFile.write("person, sent, received\n");
for key, value in sortedSenderDict:
    recipientCount = "0"
    if key in recipientDict:
        recipientCount = str(recipientDict.get(key))
    oFile.write(key + ", " + str(value) + ", " + recipientCount + "\n")
for key, value in sortedRecipientDict:  
    if key not in senderDict:
        oFile.write(key + ", 0, " + str(value) + ",\n");  

#------
senders, senderMessagesCount = np.unique(inputData[:,1], return_counts=True)
# Array with (name, count) in alphabetic order
sentMessagesArray = np.array([(y,x) for (y,x) in sorted(zip(senders, senderMessagesCount),key=lambda v: v[0].lower())])
# Order (sender ,number of messages sent)
prolificSenders =  np.array([x for (x,y) in sorted(sentMessagesArray, key=lambda v: -int(v[1].lower()))])

#Top 5 Prolific Senders
topN = 5
mostProlificSenders = dict.fromkeys(prolificSenders[:topN])

dataLen = inputData.shape[0]
#convert millisec to months
msToMonth = 1000 * 3600 * 24 * 30
for key in prolificSenders[:topN]:
    timeList = []
    for i in range(dataLen):
        if key == inputData[i,1]:
            time = round((int(inputData[i,0]))/(msToMonth))  
            timeList.append(time)
    
    timeList = np.unique(timeList, return_counts=True)
    mostProlificSenders[key]= timeList

#Plot Graph
senderFigure = plt.figure("Requirement-2")
colors = list("rgbcmyk")
for m in mostProlificSenders:
    x = mostProlificSenders[m][0]
    y = mostProlificSenders[m][1]
    plt.plot(x, y, color=colors.pop(), label = m)

plt.grid(True)
plt.xlabel("Duration (in Months)", fontsize=18, color="Green")
plt.ylabel("Emails Count", fontsize=18, color="Green")
plt.title('Number Of Emails Sent Out Every Month')
plt.legend(loc=2, borderaxespad=0., frameon=False)
senderFigure.savefig('target/output2.png', format='png', dpi=100)
senderFigure.show()

#------
uniqueSenders = dict.fromkeys(prolificSenders[:topN],[])
countSenders = dict.fromkeys(prolificSenders[:topN],[])
for i in range(dataLen):
    recipientList = inputData[i,2].split('|')
    sender = inputData[i,1]
    if not (sender in uniqueSenders):
        for key in recipientList:
            if key in prolificSenders[:topN]:
                time = (int(inputData[i,0]))/(msToMonth) 
                countSenders[key] = np.append(time, countSenders[key])
                uniqueSenders[key] = np.append(sender, countSenders[key])

for e in countSenders:
    countSenders[e] = np.unique(countSenders[e], return_counts=True)

# Plots Graph
recipientFigure = plt.figure("Requirement-3")

colors = list("rgbcmyk")
for m in countSenders:
    x = countSenders[m][0]
    y = countSenders[m][1]
    plt.plot(x, y, color=colors.pop(), label = m)

plt.grid(True)
plt.xlabel("Duration in Months", fontsize=18, color="Green")
plt.ylabel('Senders Count', fontsize=18, color="Green")
plt.title('Number of Unique Email Senders Every Month')
plt.legend(loc=2, borderaxespad=0., frameon=False)
recipientFigure.savefig('target/output3.png', format='png', dpi=100)    
recipientFigure.show()