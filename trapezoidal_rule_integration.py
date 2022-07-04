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
    print("SUMMATION | start: %d, end: %d, x0: %f, h: %f\n" % (start, end, x0, h))
    print("SUMMATION | initial x: %f\n" % (x))
    for i in range(start, end):
        sum += f(x)
        x = round(x + h, 6)
    print("SUMMATION | final x: %f\n" % (x))
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
            print("INICIANDO | x0: %f, xn: %f, n: %f\n" % (x0, xn, n))
            start_time = datetime.datetime.now()
            
            h = (xn - x0) / n
            sum = summation(1, n, x0, h)
            r = h * (( f(x0) + f(xn) ) / 2 + sum )
            
            end_time = datetime.datetime.now()
            execution_time = (end_time - start_time).total_seconds() 
            
            print("Resultado final: %f" % (r))
            print("Tempo de execucao em segundos:", execution_time)

trapezoidal_rule(0, 100000, 1000000)
