from mpi4py import MPI
import datetime

def f(x: float):
    """Defines the function you want to calculate the integration.

    Args:
        x (float): value of variable of integration

    Returns:
        float: The result of 5*x^3 + 3*x^2 + 4*x + 20
    """
    return 5 * pow(x, 3) + 3 * pow (x, 2) + 4 * x + 20

def summation(start: float, end: float, h: float):
    """Sums and return sum value

    Args:
        start (float): x start value
        end (float): x end value
        h (float): h value

    Returns:
        float: sum value
    """
    sum = 0
    x = start
    while (x <= end):
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
            h = (xn - x0) / n
            sum = summation(x0 + h, xn, h)
            r = h * (( f(x0) + f(xn) ) / 2 + sum )
            print("O resultado da integral da função f é", r)

def butterfly_method(x0: float, xn: float, n: int):
    
    if n == 0:
        print("Divisão por zero")
    else:
        if n < 0:
            print("Intervalo inválido")
        else:
            comm = MPI.COMM_WORLD
            size = comm.Get_size()
            rank = comm.Get_rank()

            if rank == 0:
                start_time = datetime.datetime.now()
                
                h = (xn - x0) / n
                
                for i in range(1, size):
                    comm.send([n, h], dest = i, tag = 1)
                    
                portion = int(n / size)
                start = portion * rank + h
                end = portion * (rank + 1)
                if rank == size - 1:
                    end = n

                sum = summation(start, end, h)
                
                half = size
                
                while rank < half and half > 1:
                    half /= 2
                    info = MPI.Status()
                    partial_sum = comm.recv(source = rank + half, tag = 2, status = info)
                    sum += partial_sum
                    print("trabalhador %d recebeu de trabalhador %d" % (rank, info.Get_source()))
                
                r = h * (( f(x0) + f(xn) ) / 2 + sum )
            
                end_time = datetime.datetime.now()
                execution_time = (end_time - start_time).total_seconds() 

                print("Resultado final:", r)
                print("Tempo de execucao em segundos de relogio:", execution_time)
                
            else:
                data = comm.recv(source = 0, tag = 1)
                n = data[0]
                h = data[1]
                print ("trabalhador de rank %d: n %d, h %f" % (rank, n, h))
                
                portion = int(n / size)
                start = portion * rank + h
                end = portion * (rank + 1)
                if rank == size - 1:
                    end = n

                sum = summation(start, end, h)
                
                half = size
                
                while rank < half and half > 1:
                    half /= 2
                    info = MPI.Status()
                    if rank >= half:
                        comm.send(sum, dest = rank - half, tag = 2)
                    else:
                        partial_sum = comm.recv(source = rank + half, tag = 2, status = info)
                        sum += partial_sum
                        print("trabalhador %d recebeu de trabalhador %d" % (rank, info.Get_source()))
