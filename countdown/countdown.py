from datetime import datetime
import requests

def calcTimeRemaining(deadline):
    return deadline - datetime.now()
    
def convStrToDate(deadlineStr):
    return datetime.strptime(deadlineStr, '%m/%d/%Y')

def main():
    userInput = input("Enter your goal with a deadline seperated by a colon: ")
    inputList = userInput.split(":")
    goal = inputList[0]
    deadline = inputList[1]
    numDays = calcTimeRemaining(convStrToDate(deadline))
    print (f"The number of days for goal: {goal}, on date: {deadline} is " + str(numDays.days))
if __name__ == '__main__':
    main()