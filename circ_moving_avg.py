import numpy as np

# def movAvg(vals,points):
    
#     # performs a cyclic moving average on an array or list with <points> values
#     # averaged per output point.  the return value is an array where the first
#     # (<vals> - <points> + 1) points are the data with the moving avg applied.
    
#     def shifty(arr,num):
#         part2 = arr[:,:-num]
#         if len(part2.shape) == 0:
#             part2 = np.expand_dims(part2,1)
            
#         return np.hstack((arr[:,-num:],part2))
    
#     size_vals = len(vals)
    
#     sumsies = np.eye(size_vals)
#     for nn in range(points - 1):
#         sumsies += shifty(np.eye(size_vals),nn + 1)
        
#     return np.matmul(sumsies,vals) / points



def movAvg(vals,num_points, crop = True):
    
    # performs a cyclic moving average on an array or list with <num_points> values
    # averaged per output point.  the return value is an array where the first
    # (len(<vals>) - <num_points> + 1) points are the data with the moving avg applied.
    
    def shifty(arr,num):
        part2 = arr[:,:-num]
        if len(part2.shape) == 0:
            part2 = np.expand_dims(part2,1)
            
        return np.hstack((arr[:,-num:],part2))
    
    size_vals = len(vals)
    
    sumsies = np.eye(size_vals)
    for nn in range(num_points - 1):
        sumsies += shifty(np.eye(size_vals),nn + 1)
    
    outMat = np.matmul(sumsies,vals) / num_points
    
    if crop:
        outMat = outMat[:size_vals - num_points + 1]
    
    return outMat


test_vals = [1,2,3,4,5]
num_points = 3
crop = True
print(movAvg(test_vals, num_points))