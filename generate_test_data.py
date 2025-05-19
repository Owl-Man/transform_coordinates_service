import pandas as pd
import numpy as np
import random

def generate_test_data(num_points: int = 10) -> pd.DataFrame:
    x = np.random.uniform(0, 1000, num_points)
    y = np.random.uniform(0, 1000, num_points)
    z = np.random.uniform(0, 500, num_points)
    
    names = [f"Point_{i+1}" for i in range(num_points)]
    
    df = pd.DataFrame({
        'Name': names,
        'X': x,
        'Y': y,
        'Z': z
    })
    
    return df

test_data = generate_test_data(num_points=20)
    
test_data.to_excel("TEST_EXAMPLE.xlsx", index=False)
print("Test data generated and saved to test_data.xlsx")