def f(x: float):
    """Defines the function you want to calculate the integration.

    Args:
        x (float): value of variable of integration

    Returns:
        float: The result of 5*x^3 + 3*x^2 + 4*x + 20
    """
    return 5 * pow(x, 3) + 3 * pow (x, 2) + 4 * x + 20

def summation(n: int, x: float, h: float):
    """Sums and return sum value

    Args:
        n (int): discretization value
        x (float): x value
        h (float): h value

    Returns:
        float: sum value
    """
    sum = 0
    for i in range (1, n):
        sum += f(x)
        x += h
    return sum

def trapezoidal_rule(x0: float, xn: float, n: int):
    """Trapezoidal rule for integration calculus.

    Args:
        x0 (float): lower bound of integration
        xn (float): upper bound of integration
        n (int): discretization value
    """
    if n == 0:
        print("Divisão por zero")
    else:
        if n < 0:
            print("Intervalo inválido")
        else:
            h = (xn - x0)/n
            x = x0 + h
            sum = summation(n, x, h)
            r = h * (( f(x0) + f(xn) ) / 2 + sum )
            print("O resultado da integral da função f é", r)
