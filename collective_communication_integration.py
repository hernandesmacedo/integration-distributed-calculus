from mpi4py import MPI
import datetime

def f(x: float):
    """Defines the function you want to integrate.

    Args:
        x (float): value of integration variable

    Returns:
        float: The result of 5*x^3 + 3*x^2 + 4*x + 20
    """
    return 5 * x**3 + 3 * x**2 + 4 * x + 20

def summation(start: int, end: int, x0: float, h: float, rank: int):
    """Sums results of a function

    Args:
        start (int): loop start value
        end (int): loop end value
        x0 (float): x start value
        h (float): height value
        rank (int): id

    Returns:
        float: sum value
    """
    sum = 0
    x = round(x0 + h * start, 6)
    print("SUMMATION (id %d) | start: %d, end: %d, x0: %f, h: %f\n" % (rank, start, end, x0, h))
    print("SUMMATION (id %d) | initial x: %f\n" % (rank, x))
    for i in range(start, end):
        sum += f(x)
        x = round(x + h, 6)
    print("SUMMATION (id %d) | final x: %f\n" % (rank, x))
    return sum

def collective_communication(x0: float, xn: float, n: int):
    """Trapezoidal rule for integration calculus using
    broadcast and reduce as collective communication.

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
            comm = MPI.COMM_WORLD
            size = comm.Get_size()
            rank = comm.Get_rank()
            
            h = 0

            if rank == 0:
                start_time = datetime.datetime.now()
                
                h = (xn - x0) / n
                
                h = comm.bcast(h, root = 0)
                print("BROADCAST | id %d\n" % (rank))
                    
                portion = int(n / size)
                start = portion * rank + 1
                end = portion * (rank + 1) + 1
                if rank == size - 1:
                    end = n

                sum = summation(start, end, x0, h, rank)
                
                sum = comm.reduce(sum, op = MPI.SUM, root = 0)
                print("REDUCE TO SUM | id %d\n" % (rank))
                
                r = h * (( f(x0) + f(xn) ) / 2 + sum )
            
                end_time = datetime.datetime.now()
                execution_time = (end_time - start_time).total_seconds() 

                print("Resultado final: %f" % (r))
                print("Tempo de execucao em segundos:", execution_time)
                
            else:
                h = comm.bcast(h, root = 0)
                print("BROADCAST | id %d\n" % (rank))
                
                portion = int(n / size)
                start = portion * rank + 1
                end = portion * (rank + 1) + 1
                if rank == size - 1:
                    end = n

                sum = summation(start, end, x0, h, rank)
                
                sum = comm.reduce(sum, op = MPI.SUM, root = 0)
                print("REDUCE TO SUM | id %d\n" % (rank))

collective_communication(0, 100000, 1000000)
