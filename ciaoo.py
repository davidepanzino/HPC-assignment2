from array import array
import sys

# Matrix size

@profile
def array_function(A, B, C, N):
    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i * N + j] += A[i * N + k] * B[k * N + j]
    return C

@profile
def list_function(A,B,C, N):
    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i][j] += A[i][k] * B[k][j]
    return C



if __name__ == "__main__":

    N = 5

    for i in range(7):

        # Create double precision arrays for A, B, and C
        A = array('d', [0.0] * (N * N))
        B = array('d', [0.0] * (N * N))
        C = array('d', [0.0] * (N * N))

        # Fill matrices A and B with values (for demonstration purposes, you should populate your matrices accordingly)
        for i in range(N):
            for j in range(N):
                A[i * N + j] = i + j  # Example value for A
                B[i * N + j] = i - j  # Example value for B

        C = array_function(A,B,C, N)

        # Print resulting matrix C (for demonstration purposes)
        for i in range(N):
            for j in range(N):
                print(C[i * N + j], end=" ")
            print()



        A = [[0.0] * N for _ in range(N)]
        B = [[0.0] * N for _ in range(N)]
        C = [[0.0] * N for _ in range(N)]

        # Fill matrices A and B with values (for demonstration purposes, you should populate your matrices accordingly)
        for i in range(N):
            for j in range(N):
                A[i][j] = i + j  # Example value for A
                B[i][j] = i - j  # Example value for B

        # Perform matrix multiplication C = C + A * B

        C = list_function(A,B,C, N)

        # Print resulting matrix C (for demonstration purposes)
        for row in C:
            print(" ".join(str(element) for element in row))

        N *= 2


