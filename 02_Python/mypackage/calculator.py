# mypackage/calculator.py (모듈)

# 변수인 셈 (global)
__version = 0.1 # 이런식으로 버전 명시

# 함수
def plus(num1, num2):
    return num1 + num2

def minus(num1, num2):
    return num1 - num2

def multiply(num1, num2):
    return num1 * num2

def divide(num1, num2):
    return num1 / num2

if __name__ == "__main":
    print(">>>>name<<<<", __name__)
    print(plus(10, 20))