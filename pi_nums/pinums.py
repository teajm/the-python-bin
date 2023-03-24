#need to calc pi up to in digits received from user
from math import acos

def calcPi(digs):
    pi = round(2*acos(0.0), int(digs))
    return pi

def main():
    while(True):
        print("How many digits you wanna see.. ")
        nthDig = input()
        if nthDig == "e":
            break
        if not nthDig.isdigit():
            print("Enter a digit...")
        else:
            print (f"Pi to {nthDig} values is {calcPi(nthDig)}")
if __name__ == '__main__':
    main()