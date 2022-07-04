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

def butterfly_method(x0: float, xn: float, n: int):
    """Trapezoidal rule for integration calculus using butterfly method.
    
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

            if rank == 0:
                start_time = datetime.datetime.now()
                
                h = (xn - x0) / n
                
                for i in range(1, size):
                    comm.send(h, dest = i, tag = 1)
                    print("ENVIO | id %d enviou h %f para id %d\n" % (rank, h, i))
                    
                portion = int(n / size)
                start = portion * rank + 1
                end = portion * (rank + 1) + 1
                if rank == size - 1:
                    end = n

                sum = summation(start, end, x0, h, rank)
                
                half = size
                
                while rank < half and half > 1:
                    half /= 2
                    info = MPI.Status()
                    partial_sum = comm.recv(source = rank + half, tag = 2, status = info)
                    sum += partial_sum
                    print("RECEPCAO | id %d recebeu sum de id %d\n" % (rank, rank + half))
                
                r = h * (( f(x0) + f(xn) ) / 2 + sum )
            
                end_time = datetime.datetime.now()
                execution_time = (end_time - start_time).total_seconds() 

                print("Resultado final: %f" % (r))
                print("Tempo de execucao em segundos:", execution_time)
                
            else:
                h = comm.recv(source = 0, tag = 1)
                print("RECEPCAO | id %d recebeu h %f de id %d\n" % (rank, h, 0))
                
                portion = int(n / size)
                start = portion * rank + 1
                end = portion * (rank + 1) + 1
                if rank == size - 1:
                    end = n

                sum = summation(start, end, x0, h, rank)
                
                half = size
                
                while rank < half and half > 1:
                    half /= 2
                    info = MPI.Status()
                    if rank >= half:
                        comm.send(sum, dest = rank - half, tag = 2)
                        print("ENVIO | id %d enviou sum para id %d\n" % (rank, rank - half))
                    else:
                        partial_sum = comm.recv(source = rank + half, tag = 2, status = info)
                        sum += partial_sum
                        print("RECEPCAO | id %d recebeu sum de id %d\n" % (rank, rank + half))

butterfly_method(0, 100000, 1000000)
