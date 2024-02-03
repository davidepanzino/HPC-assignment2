#using lists
from timeit import default_timer as timer
import sys
import matplotlib.pyplot as plt

STREAM_ARRAY_SIZE = 10

a = []
b = []
c = []
times = []
bandwidth = []

for i in range(8):
    times.append([None, None, None, None])
    bandwidth.append([None, None, None, None])
    for j in range(STREAM_ARRAY_SIZE):
        a.append(1.0) 
        b.append(2.0)
        c.append(0.0)
    scalar = 2.0

    # copy
    times[i][0] = timer()
    for j in range(STREAM_ARRAY_SIZE):
        c[j] = a[j]
    times[i][0] = timer() - times[i][0]

    # scale
    times[i][1] = timer()
    for j in range(STREAM_ARRAY_SIZE):
        b[j] = scalar*c[j]
    times[i][1] = timer() - times[i][1]

    #sum
    times[i][2] = timer()
    for j in range(STREAM_ARRAY_SIZE):
        c[j] = a[j]+b[j]
    times[i][2] = timer() - times[i][2]

    # triad
    times[i][3] = timer()
    for j in range(STREAM_ARRAY_SIZE):
        a[j] = b[j]+scalar*c[j]
    times[i][3] = timer() - times[i][3]

    bandwidth[i][0] = (2*sys.getsizeof(a)*STREAM_ARRAY_SIZE)/times[i][0]
    bandwidth[i][1] = (2*sys.getsizeof(a)*STREAM_ARRAY_SIZE)/times[i][1]
    bandwidth[i][2] = (3*sys.getsizeof(a)*STREAM_ARRAY_SIZE)/times[i][2]
    bandwidth[i][3] = (3*sys.getsizeof(a)*STREAM_ARRAY_SIZE)/times[i][3]

    STREAM_ARRAY_SIZE *= 10

titles = ["Copy Operation", "Scale Operation", "Sum Operation", "Triad Operation"]

# Plot each index against the list index
for i in range(4):  # Assuming 4 indices
    plt.figure()  # Create a new figure for each plot
    index_data = [sublist[i] for sublist in bandwidth]
    plt.plot([10**j for j in range(len(bandwidth))], index_data, marker='o')
    plt.xscale('log')  # Set the x-axis scale to logarithmic
    plt.yscale('log')  # Set the y-axis scale to logarithmic
    plt.title(titles[i])  # Set plot title
    plt.xlabel('STREAM_ARRAY_SIZE (log scale)')  # Set x-axis label
    plt.ylabel('Bandwidth [Byte/s] (log scale)')  # Set y-axis label

plt.show()

 


#using arrays

from array import array
from timeit import default_timer as timer
import sys
import matplotlib.pyplot as plt

STREAM_ARRAY_SIZE = 10

a = array('f')
b = array('f')
c = array('f')
times = []
bandwidth = []

for i in range(8):

    times.append([None, None, None, None])
    bandwidth.append([None, None, None, None])
    for j in range(STREAM_ARRAY_SIZE):
        a.append(1.0) 
        b.append(2.0)
        c.append(0.0)
    scalar = 2.0

    # copy
    times[i][0] = timer()
    for j in range(STREAM_ARRAY_SIZE):
        c[j] = a[j]
    times[i][0] = timer() - times[i][0]

    # scale
    times[i][1] = timer()
    for j in range(STREAM_ARRAY_SIZE):
        b[j] = scalar*c[j]
    times[i][1] = timer() - times[i][1]

    #sum
    times[i][2] = timer()
    for j in range(STREAM_ARRAY_SIZE):
        c[j] = a[j]+b[j]
    times[i][2] = timer() - times[i][2]

    # triad
    times[i][3] = timer()
    for j in range(STREAM_ARRAY_SIZE):
        a[j] = b[j]+scalar*c[j]
    times[i][3] = timer() - times[i][3]

    bandwidth[i][0] = (2*sys.getsizeof(a)*STREAM_ARRAY_SIZE)/times[i][0]
    bandwidth[i][1] = (2*sys.getsizeof(a)*STREAM_ARRAY_SIZE)/times[i][1]
    bandwidth[i][2] = (3*sys.getsizeof(a)*STREAM_ARRAY_SIZE)/times[i][2]
    bandwidth[i][3] = (3*sys.getsizeof(a)*STREAM_ARRAY_SIZE)/times[i][3]

    STREAM_ARRAY_SIZE *= 10


titles = ["Copy Operation", "Scale Operation", "Sum Operation", "Triad Operation"]

# Plot each index against the list index
for i in range(4):  # Assuming 4 indices
    plt.figure()  # Create a new figure for each plot
    index_data = [sublist[i] for sublist in bandwidth]
    plt.plot([10**j for j in range(len(bandwidth))], index_data, marker='o')
    plt.xscale('log')  # Set the x-axis scale to logarithmic
    plt.yscale('log')  # Set the y-axis scale to logarithmic
    plt.title(titles[i])  # Set plot title
    plt.xlabel('STREAM_ARRAY_SIZE (log scale)')  # Set x-axis label
    plt.ylabel('Bandwidth [Byte/s] (log scale)')  # Set y-axis label

plt.show()