from math import isclose ,sqrt

def add_matrices(mat1, mat2):
  if len(mat1) != len(mat2) or len(mat1[0]) != len(mat2[0]):
    raise ValueError("Las matrices deben tener las mismas dimensiones para sumarlas")
  
  result = [[mat1[i][j] + mat2[i][j] for j in range(len(mat1[0]))] for i in range(len(mat1))]
  return result

def subtract_matrices(mat1, mat2):
  if len(mat1) != len(mat2) or len(mat1[0]) != len(mat2[0]):
    raise ValueError("Las matrices deben tener las mismas dimensiones para restarlas")
    
  result = [[mat1[i][j] - mat2[i][j] for j in range(len(mat1[0]))] for i in range(len(mat1))]
  return result
  
def multiply_matrices(mat1, mat2):
  if len(mat1[0]) != len(mat2):
    raise ValueError("El número de columnas de la primera matriz debe coincidir con el número de filas de la segunda matriz")
  
  result = [[sum([mat1[i][k] * mat2[k][j] for k in range(len(mat2))]) for j in range(len(mat2[0]))] for i in range(len(mat1))]
  return result

def multiply_matrix_scalar(matrix, scalar):
  result = [[cell * scalar for cell in row] for row in matrix]
  return result

def multiply_matrix_vector(matrix, vector):
  if len(vector) != len(matrix[0]):
    raise ValueError("La longitud del vector debe coincidir con el número de columnas de la matriz")

  result = [sum([matrix[i][j] * vector[j] for j in range(len(vector))]) for i in range(len(matrix))]
  return result
  
def transpose_matrix(matrix):
  result = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
  return result
    
def bcCoords(A, B, C, P):
    BCP = abs((P[0] * C[1] + C[0] * B[1] + B[0] * P[1]) - (P[1] * C[0] + C[1] * B[0] + B[1] * P[0]))
    CAP = abs((A[0] * C[1] + C[0] * P[1] + P[0] * A[1]) - (A[1] * C[0] + C[1] * P[0] + P[1] * A[0]))
    ABP = abs((A[0] * B[1] + B[0] * P[1] + P[0] * A[1]) - (A[1] * B[0] + B[1] * P[0] + P[1] * A[0]))
    
    ABC = abs((A[0] * B[1] + B[0] * C[1] + C[0] * A[1]) - (A[1] * B[0] + B[1] * C[0] + C[1] * A[0]))

   

    if ABC == 0:
        return None

    u = BCP / ABC
    v = CAP / ABC
    w = ABP / ABC
    #w = 1 - u - v

    if (0 <= u <= 1) and (0 <= v <= 1) and (0 <= w <= 1) and isclose(u + v + w, 1.0):
        return u, v, w
    else:

        return None
    
def bcCoords(A, B, C, P):
    BCP = abs((P[0] * C[1] + C[0] * B[1] + B[0] * P[1]) - (P[1] * C[0] + C[1] * B[0] + B[1] * P[0]))
    CAP = abs((A[0] * C[1] + C[0] * P[1] + P[0] * A[1]) - (A[1] * C[0] + C[1] * P[0] + P[1] * A[0]))
    ABP = abs((A[0] * B[1] + B[0] * P[1] + P[0] * A[1]) - (A[1] * B[0] + B[1] * P[0] + P[1] * A[0]))
    
    ABC = abs((A[0] * B[1] + B[0] * C[1] + C[0] * A[1]) - (A[1] * B[0] + B[1] * C[0] + C[1] * A[0]))

    if ABC == 0:
        return None

    u = BCP / ABC
    v = CAP / ABC
    w = ABP / ABC


    if (0 <= u <= 1) and (0 <= v <= 1) and (0 <= w <= 1) and isclose(u + v + w, 1.0):
        return u, v, w
    else:

        return None
    
def sub(v1, v2):
        if len(v1) != len(v2):
            raise ValueError("Tuples must have the same length.")
        
        subtracted_tuple = tuple(a - b for a, b in zip(v1, v2))
        return subtracted_tuple
    
def add(v1, v2):
        if len(v1) != len(v2):
            raise ValueError("Tuples must have the same length.")
        
        added_tuple = tuple(a + b for a, b in zip(v1, v2))
        return added_tuple    
    
def norm(x, ord=None, axis=None, keepdims=False):
        if axis is not None:
            raise ValueError("Axis argument is not supported.")
        
        if ord is None or ord == 2:
            squared_sum = sum(v ** 2 for v in x)
            norm = sqrt(squared_sum)
            return norm
        else:
            raise ValueError("Only Euclidean norm (ord=2) is supported.")
        
def divTF(t, d):
    if d != 0:
        divided_tuple = tuple(value / d for value in t)
        return divided_tuple
    else:
        return t
    
def cross(v1, v2):
    if len(v1) != 3 or len(v2) != 3:
        raise ValueError("Tuples must be 3-dimensional.")
    
    cross_product = [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]
    return cross_product

def inv(matrix):
        if len(matrix) != len(matrix[0]):
            raise ValueError("Matrix must be square for inversion.")
        
        n = len(matrix)
        augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        
        # Perform Gauss-Jordan elimination
        for i in range(n):
            pivot_row = augmented_matrix[i]
            pivot_element = pivot_row[i]
            
            if pivot_element == 0:
                raise ValueError("Matrix is singular, cannot be inverted.")
            
            pivot_row_normalized = [elem / pivot_element for elem in pivot_row]
            augmented_matrix[i] = pivot_row_normalized
            
            for k in range(n):  # Use k instead of j
                if k != i:
                    factor = augmented_matrix[k][i]
                    row_to_subtract = [elem * factor for elem in pivot_row_normalized]
                    augmented_matrix[k] = [x - y for x, y in zip(augmented_matrix[k], row_to_subtract)]
        
        inverse_matrix = [row[n:] for row in augmented_matrix]
        return inverse_matrix

def dot_product(array1, array2):
        if len(array1) != len(array2):
            raise ValueError("Arrays must have the same length for dot product.")

        dot_product = sum(a * b for a, b in zip(array1, array2))
        return dot_product
    
def multiply(i = 1 , arr = [1]):
    return [i * x for x in arr]

def subtract(arr1, arr2):
    if len(arr1) != len(arr2):
            raise ValueError("Arrays must have the same length for subtraction.")
        
    return [a - b for a, b in zip(arr1, arr2)]