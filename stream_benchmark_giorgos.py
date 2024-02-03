from timeit import default_timer as timer
import numpy as np
import array as arr
import sys
import matplotlib.pyplot as plt

def main(args, tests):

    STREAM_LENGTH = args.STREAM_LENGTH
    bandwidth_lists = []
    bandwidth_arrays = []
    for i in range(STREAM_LENGTH):
        STREAM_ARRAY_SIZE = args.STREAM_ARRAY_SIZE[i]
        NTIMES = args.NTIMES
        STREAM_TYPE = args.STREAM_TYPE

        #Python Lists
        a = STREAM_ARRAY_SIZE * [0]
        b = STREAM_ARRAY_SIZE * [0]
        c = STREAM_ARRAY_SIZE * [0]

        #Python arrays
        d = arr.array ('f', [0]*STREAM_ARRAY_SIZE)
        e = arr.array ('f', [0]*STREAM_ARRAY_SIZE)
        f = arr.array ('f', [0]*STREAM_ARRAY_SIZE)

        avgtime = np.zeros((4,), dtype='double')
        maxtime = np.zeros((4,), dtype='double')
        FLT_MAX = np.finfo('single').max
        mintime = np.array([FLT_MAX, FLT_MAX, FLT_MAX, FLT_MAX])

        stream = STREAM_LENGTH * [0]

        stream = [1000, 10000, 50000, 100000]

        label = ["Copy:      ", "Scale:     ", "Add:       ", "Triad:     "]

        tbytes = np.array([2 * sys.getsizeof(STREAM_TYPE) * STREAM_ARRAY_SIZE,
                        2 * sys.getsizeof(STREAM_TYPE) * STREAM_ARRAY_SIZE,
                        3 * sys.getsizeof(STREAM_TYPE) * STREAM_ARRAY_SIZE,
                        3 * sys.getsizeof(STREAM_TYPE) * STREAM_ARRAY_SIZE],
                        dtype='float')
        
        BytesPerWord = 0
        times = np.zeros((4, NTIMES))

        BytesPerWord = np.nbytes[STREAM_TYPE]
        print("Bytes per array element: %d" % BytesPerWord)
        print("Array size: %d (elements)" % STREAM_ARRAY_SIZE)
        print("Memory per array: %.2f MiB." %
            (BytesPerWord * (STREAM_ARRAY_SIZE / 1024.0 / 1024.0))) #The division by 1024.0 / 1024.0 converts the result from bytes to megabytes
        print("Total memory required: %.2f MiB" %
            (3.0 * BytesPerWord * (STREAM_ARRAY_SIZE / 1024.0 / 1024.0)))
        print("Number of reps: %d" % NTIMES)

        #Initializing python lists
        for j in range(STREAM_ARRAY_SIZE):
            a[j] = 1.0
            b[j] = 2.0
            c[j] = 0.0
        scalar = 2.0

        for j in range(STREAM_ARRAY_SIZE):
            d[j] = 1.0
            e[j] = 2.0
            f[j] = 0.0

        for test in tests: 

            print('## %s' % test)
            times[:] = 0.0

            if test == 'python_lists':
                for k in range(NTIMES):
                    # copy
                    times[0][k] = timer()
                    for j in range(STREAM_ARRAY_SIZE):
                        c[j] = a[j]
                    times[0][k] = timer() - times[0][k]

                    # scale
                    times[1][k] = timer()
                    for j in range(STREAM_ARRAY_SIZE):
                        b[j] = scalar*c[j]
                    times[1][k] = timer() - times[1][k]
                        
                    #sum
                    times[2][k] = timer()
                    for j in range(STREAM_ARRAY_SIZE):
                        c[j] = a[j] + b[j]
                    times[2][k] = timer() - times[2][k]

                    # triad
                    times[3][k] = timer()
                    for j in range(STREAM_ARRAY_SIZE):
                        a[j] = b[j] + scalar*c[j]
                    times[3][k] = timer() - times[3][k]
                
                avgtime = times[:, 1:].mean(axis=1)  # note -- skip first iteration
                mintime = times[:, 1:].min(axis=1)
                maxtime = times[:, 1:].max(axis=1)

                print("```")
                print("Function    Best Rate GB/s  Avg time     Min time     Max time")
                for j in range(4):
                    bandwidth_lists.append(1.0e-09 * tbytes[j]/mintime[j])
                    print("%s%12.1f  %11.6f  %11.6f  %11.6f" %
                            (label[j],
                            1.0e-09 * tbytes[j]/mintime[j],
                            avgtime[j],
                            mintime[j],
                            maxtime[j]))
                    print("```\n")
                
            elif test == 'python_arrays': 
                for k in range(NTIMES):
                    # copy
                    times[0][k] = timer()
                    for j in range(STREAM_ARRAY_SIZE):
                        f[j] = d[j]
                    times[0][k] = timer() - times[0][k]

                    # scale
                    times[1][k] = timer()
                    for j in range(STREAM_ARRAY_SIZE):
                        e[j] = scalar*f[j]
                    times[1][k] = timer() - times[1][k]
                        
                    #sum
                    times[2][k] = timer()
                    for j in range(STREAM_ARRAY_SIZE):
                        f[j] = d[j] + e[j]
                    times[2][k] = timer() - times[2][k]

                    # triad
                    times[3][k] = timer()
                    for j in range(STREAM_ARRAY_SIZE):
                        d[j] = e[j] + scalar*f[j]
                    times[3][k] = timer() - times[3][k]

                avgtime = times[:, 1:].mean(axis=1)  # note -- skip first iteration
                mintime = times[:, 1:].min(axis=1)
                maxtime = times[:, 1:].max(axis=1)

                print("```")
                print("Function    Best Rate GB/s  Avg time     Min time     Max time")
                for j in range(4):
                    bandwidth_arrays.append(1.0e-09 * tbytes[j]/mintime[j])
                    print("%s%12.1f  %11.6f  %11.6f  %11.6f" %
                            (label[j],
                            1.0e-09 * tbytes[j]/mintime[j],
                            avgtime[j],
                            mintime[j],
                            maxtime[j]))
                    print("```\n")

    plt.plot(stream, bandwidth_lists[0::4], color = 'r', label = 'Copy')
    plt.plot(stream, bandwidth_lists[1::4], color = 'g', label = 'Scale')
    plt.plot(stream, bandwidth_lists[2::4], color = 'y', label = 'Sum')
    plt.plot(stream, bandwidth_lists[3::4], color = 'b', label = 'Scale')

    plt.xscale('log')
    plt.xlabel("Stream Size")
    #plt.xticks([1000, 100000, 250000, 500000])
    plt.ylabel("Bandwidth [Gb/sec]")
    plt.yscale('log')
    plt.title("Change of Bandwidth for different stream size")

    plt.legend()
    plt.show()



    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='pystream')
    parser.add_argument('--STREAM_ARRAY_SIZE', action='store',
                        dest='STREAM_ARRAY_SIZE', type=int,
                        default= [1000, 10000, 50000, 100000])
    parser.add_argument('--STREAM_LENGTH', action='store',
                        dest='STREAM_LENGTH', type=int,
                        default = 4)
    parser.add_argument('--NTIMES', action='store', dest='NTIMES', type=int,
                        default=3)
    parser.add_argument('--STREAM_TYPE', action='store', dest='STREAM_TYPE',
                        default='float')
    parser.add_argument('--test', nargs="*", default=['all'])
    args = parser.parse_args()

    tests = ['python_lists', 'python_arrays']

    main(args, tests)
