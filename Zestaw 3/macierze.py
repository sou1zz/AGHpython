def multiply_matrices(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Liczba kolumn A musi być równa liczbie kolumn B")
    
    result = [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
    return result

A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
print(multiply_matrices(A, B))
