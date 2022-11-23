from machine import Pin,Timer,I2C
import utime
from ssd1306 import SSD1306_I2C
import framebuf

debug=True

i2c = I2C(0, scl=Pin(21), sda=Pin(20), freq=40000)
oled = SSD1306_I2C(128, 64, i2c)

keyName = [['1','2','3','+','a'],
           ['4','5','6','-','b'],
           ['7','8','9','*','c'],
           ['s','0','.','/','=']]
keypadRowPins = [13,12,11,10]
keypadColPins = [14,15,16,17,18]

row = []
col = []
keypadState = [];
for i in keypadRowPins:
    row.append(Pin(i,Pin.IN,Pin.PULL_UP))
    keypadState.append([0,0,0,0,0])
for i in keypadColPins:
    col.append(Pin(i,Pin.OUT))

def solve(oprt, oprdA, oprdB):
    if(oprt == "+"):
        return oprdA + oprdB
    elif(oprt == "-"):
        return oprdA - oprdB
    elif(oprt == "*"):
        return oprdA * oprdB
    elif(oprt == "/"):
        return round(oprdA / oprdB , 6)

def calc(lst):
    operand = []
    operator = []
    
    for i in lst:
        if(debug):
            print(i)
        if(i=='+'):
            while (len(operator)!=0 and (operator[-1] == '*' or operator[-1] == '/' or operator[-1] == '-' or operator[-1] == '+')):
                b = operand.pop(-1)
                a = operand.pop(-1)
                c = operator.pop(-1)
                operand.append(solve(c,a,b))
            operator.append(i)
        elif(i=='-'):
            while (len(operator)!=0 and (operator[-1] == '*' or operator[-1] == '/' or operator[-1] == '-' or operator[-1] == '+')):
                b = operand.pop(-1)
                a = operand.pop(-1)
                c = operator.pop(-1)
                operand.append(solve(c,a,b))
            operator.append(i)
        elif(i=='*'):
            while (len(operator)!=0 and (operator[-1] == '*' or operator[-1] == '/')):
                b = operand.pop(-1)
                a = operand.pop(-1)
                c = operator.pop(-1)
                operand.append(solve(c,a,b))
            operator.append(i)
        elif(i=='/'):
            while (len(operator)!=0 and (operator[-1] == '*' or operator[-1] == '/')):
                b = operand.pop(-1)
                a = operand.pop(-1)
                c = operator.pop(-1)
                operand.append(solve(c,a,b))
            operator.append(i)

        elif(i=='('):
            operator.append(i)

        elif(i==')'):
            while(operator[-1] !='('):
                b = operand.pop(-1)
                a = operand.pop(-1)
                c = operator.pop(-1)
                operand.append(solve(c,a,b))
            operator.pop(-1)
        else:
            operand.append(i)
            
    while(len(operator) != 0):
        b = operand.pop(-1)
        a = operand.pop(-1)
        c = operator.pop(-1)
        operand.append(solve(c,a,b))

    return operand[0]

def keypadRead():
    global row
    j_ifPressed = -1
    i_ifPressed = -1
    for i in range(0,len(col)):
        col[i].low()
        utime.sleep(0.005) #settling time
        for j in range(0,len(row)):
            pressed = not row[j].value()
            if(pressed and (keypadState[j][i] != pressed)): #state changed to high
                keypadState[j][i] = pressed
            elif(not pressed and (keypadState[j][i] != pressed)): # state changed to low
                keypadState[j][i] = pressed
                j_ifPressed = j
                i_ifPressed = i
        col[i].high()
    if(j_ifPressed != -1 and i_ifPressed != -1):
        return keyName[j_ifPressed][i_ifPressed]
    else:
        return -1

def printOled(lst):
    oledPos = {
            "x" : 0,
            "y" : 0
          }
    
    oled.fill(0)
    string = ''
    for i in lst:
        string += str(i)
    l = 0
    while(l<len(string)):
        oled.text(string[l:l+16],oledPos["x"], oledPos["y"])
        oledPos["y"] =oledPos["y"] + 10
        l = l+16
    oled.show()
    
shiftFlag = False
signFlag = False
inputList = ['']

buffer1 = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\xff\xe8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xff\xff\xff\xf0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xff\xff\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xff\xff\xff\xff\x00\x00\x00\x03\xc0\x00\x00\x04\x00\x00\x00\xff\xe8\x00\x00\x07\xc0\x00\x00\x0f\xe0\x00\x00\x1e\x00\x00\x03\xff\x80\x00\x00\x03\xf0\x00\x00>`\x00\x00>\x00\x00\x07\xfe\x00\x00\x00\x07\xf8\x00\x00x \x00\x00v\x00\x00\x0f\xfe\x00\x00\x00\x03\xfc\x00\x00\xf0`\x00\x00\xc6\x00\x00\x1f\xfc\x00\x00\x00\x07\xfe\x00\x01\xc0`\x00\x00\xcc\x00\x00?\xfc~\x7f\x87\xff\xff\x00\x03\xc0`\x00\x01\x8c\x00\x00\x7f\xf8\xfc?\x83\xff\xff\x80\x07\x00\xc0\x00\x03\x18\x00\x00\xff\xf9\xfe\x7f\x87\xff\xff\x80\x0f\x01\xc0\x00\x07\x18\x00\x00\xff\xfb\xfc\x7f\x87\xff\xff\xc0\x0e\x03\x80\x00\x060\x00\x01\xff\xf7\xfc\x7f\x87\xff\xff\xe0\x1c\x07\x00\x00\x0c`\x00\x01\xff\xff\xfc\x7f\x07\xff\xff\xe08\x0f\x00\x00\x0c`\x00\x03\xff\xff\xfc\x7f\x87\xff\xff\xe0p\x1e\x00\x00\x18\xc0\x00\x03\xff\xff\xfc\x7f\x07\xff\xff\xf0p\x1c\x00\x009\x80\x00\x03\xff\xff\xfc\x7f\x07\xff\xff\xf0\xe0\x08\x00\x003\x00\x00\x07\xff\xff\xf8\x7f\x07\xff\xff\xf0\xc0\x00\x00\x80c\x00\x00\x03\xff\xff\xf8\xff\x07\xff\xff\xf1\xc0\x00\x03\xe0n\x03\x80\x07\xff\xff\xf8\x7f\x0f\xff\xff\xf3\x80\x00\x0f\xe0\xec\x0f\x80\x03\xff\xff\xf8\xff\x07\xff\xff\xf3\x80\x00\x0e`\xd8\x1f\x80\x03\xff\xff\xf0\x7f\x0f\xff\xff\xf7\x00\x00\x18a\xf08\x80\x03\xff\xff\xf0\xff\x07\xff\xff\xf7\x00\x008\xe1\xe01\x80\x03\xff\xff\xe0\xff\x0f\xff\xff\xe6\x00\x04p\xc3\xc0s\x00\x01\xff\xff\xe0\xfe\x07\xff\xff\xee\x00\x0ca\xc3\x00\xe2\x00\x01\xff\xff\xc0\xff\x0f\xff\xff\xee\x00\x08\xe1\x83\x08\xc0@\x00\xff\xff\xc0\xfe\x07\xf3\xff\xce\x00\x18\xc3\x87\x19\xc0\xc0\x00\xff\xff\x80\xff\x07\xf7\xff\x9c\x001\xc7\x861\x80\xc0\x00\x7f\xff\x01\xfe\x03\xe7\xff\x9c\x00a\x87\x0e3\x81\x80\x00?\xff\x01\xff\x01\x87\xff\x1c\x00\xe1\xcf\x0cc\x03\x00\x00\x1f\xfe\x01\xff\x00\x0f\xfe\x1e\x01\x81\xdb\x0f\xc3\x86\x00\x00\x0f\xfe\x01\xff\x00\x0f\xfc\x0c\x03\x81\xfb\x8f\x83\xdc\x00\x00\x07\xfe\x03\xff\x80\x1f\xf8\x0e\x07\x00\xf1\xc7\x01\xf8\x00\x00\x03\xff\x03\xff\xc0?\xe0\x0f\xbe\x00A\xc0\x00\xe0\x00\x00\x00\xff\x8f\xff\xe0\xff\xc0\x07\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xff\xff\xff\xff\x00\x03\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x0f\xff\xff\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xff\xff\xff\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xff\xd0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

fb1 = framebuf.FrameBuffer(buffer1, 128, 64, framebuf.MONO_HLSB)

oled.blit(fb1,0,0)
oled.show()

while True:
    key = keypadRead()

    if(key != -1):
        if((key <= '9' and key >='0') or key == '.'):
            inputList[-1] = inputList[-1] + key            
        elif(key == '+' or key == '-' or key == '*' or key == '/'):
            if(inputList != ['']):
                if(inputList[-1] == '' and (inputList[-2] == '+' or inputList[-2] == '-' or inputList[-2] == '*' or inputList[-2] == '/')):
                    inputList[-2] = key
                elif(inputList[-1]==''):
                    inputList[-1]=key
                    inputList.append('')
                else:
                    inputList[-1] = float(inputList[-1])
                    inputList.append(key)
                    inputList.append('')
                
        elif(key == 's'):
            shiftFlag = not shiftFlag
        elif(key == 'a'):
            if(shiftFlag):      #means ')' key is pressed
                if(inputList[-1] != ''):
                    inputList[-1] = float(inputList[-1])
                    inputList.append(')')
                    inputList.append('')
                else:
                    inputList[-1] = ')'
                    inputList.append('')
                shiftFlag = False
            else:              #means '+-' sign change key is pressed
                signFlag = not signFlag
                if(inputList[-1] == ''):
                    inputList[-1] = '-'
                else:
                    if(inputList[-1][0] == '-'):
                       inputList[-1]  = inputList[-1][1:]
                    else:
                        inputList[-1] = '-' + inputList[-1]
            
        elif(key == 'b'):
            if(shiftFlag):      #means '(' key is pressed
                if(inputList[-1] == ''):
                    inputList[-1] = '('
                else:
                    inputList.append('(')
                inputList.append('')
                shiftFlag = False
            else:               #means 'pi' key is pressed
                if(inputList[-1] == ''):
                    inputList[-1] = 3.14
                else:
                    inputList.append(3.14)
                inputList.append('')
        elif(key == 'c'):
            if(shiftFlag):      #means 'CE' key is pressed it will erase complete history
                inputList = ['']
                shiftFlag = False
            else:               #means 'C' key is pressed it will erase one digit
                if(inputList == ["error"]):
                    inputList = ['']
                if(inputList != ['']):   #move into only if the list is not empty
                    if(inputList[-1] == ''):
                        inputList.pop()
                        inputList[-1] = str(inputList[-1])[:-1]
                    else:
                        inputList[-1] = str(inputList[-1])[:-1]
        elif(key == '='):
            if(inputList[-1] == ''):
                inputList.pop(-1)
            elif(inputList[-1] != ')'):
                inputList[-1] = float(inputList[-1])
            try:
                ans = calc(inputList)
                inputList = [str(ans)]
            except:
                ans = ''
                inputList = []
                inputList.append("error")
            
        printOled(inputList)
        print(inputList)
            
        
