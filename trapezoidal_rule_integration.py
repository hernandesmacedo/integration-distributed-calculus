import datetime

def f(x: float):
    """Defines the function you want to integrate.

    Args:
        x (float): value of integration variable

    Returns:
        float: The result of 5*x^3 + 3*x^2 + 4*x + 20
    """
    return 5 * x**3 + 3 * x**2 + 4 * x + 20

def summation(start: int, end: int, x0: float, h: float):
    """Sums results of a function

    Args:
        start (int): loop start value
        end (int): loop end value
        x0 (float): x start value
        h (float): height value

    Returns:
        float: sum value
    """
    sum = 0
    x = round(x0 + h * start, 6)
    for i in range(start, end):
        sum += f(x)
        x = round(x + h, 6)
    return sum

def trapezoidal_rule(x0: float, xn: float, n: int):
    """Trapezoidal rule for integration calculus.

    Args:
        x0 (float): lower bound of integration
        xn (float): upper bound of integration
        n (int): discretization value
    """
    if n == 0:
        print("Divisao por zero")
    else:
        if n < 0:
            print("Intervalo invalido")
        else:
            start_time = datetime.datetime.now()
            
            h = (xn - x0) / n
            sum = summation(1, n, x0, h)
            r = h * (( f(x0) + f(xn) ) / 2 + sum )
            
            end_time = datetime.datetime.now()
            execution_time = (end_time - start_time).total_seconds() 
            
            print("O resultado da integral da funcao f eh", r)
            print("Tempo de execucao em segundos:", execution_time)

trapezoidal_rule(0, 100000, 1000000)
