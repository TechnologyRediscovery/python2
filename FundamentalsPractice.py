
# coding: utf-8

# In[3]:


import os as os;
def main():
    print("happy birthday")
def singToAnybody(personName):
    print("you are being sung to, " + personName)

singToAnybody("gerry")

    


# In[3]:


def basicMathFun(num1, num2, num3):
    r1 = num1 * num2
    r2 = r1 + num3
    return r2

print(basicMathFun(1,2,3))
dir()

inputFromUser = input("enter a number")

print(processUserInput(inputFromUser))

def processUserInput(i):
    n = i + " never!"
    print(type(n))
    type(n)
    return n



# In[2]:


sumto = input("Enter the upper list bound: ")
firstList = list(range(int(sumto)))
print(firstList)
sum = 0
for x in firstList:
    sum = sum + x
print(str(sum))


# In[2]:


import csv
file = open('jail.csv', newline='')
reader = csv.DictReader(file)
totBlack = 0
totWhite = 0
raceCount = {'white':totWhite, 'black':totBlack}

for row in reader:
    if row['date'] == '2018-01-01':
        if row['race'] == 'B':
            totBlack = totBlack + 1
        elif row['race'] == 'W':
            totWhite = totWhite + 1
file.close()
print("Total whites on Jan 1: " + str(totWhite))
print("Total blacks on Jan 1: " + str(totBlack))



# In[10]:


with open('jailSum.txt', 'w', newline='') as file2:
    writer = csv.writer(file2, )
    writer.writerow("Total blacks: " + str(totBlack))
    writer.writerow("Total Whites: " + str(totWhite))

