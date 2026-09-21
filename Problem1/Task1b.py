import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the two scans
scan_a = pd.read_csv('scan_posA.csv')
scan_b = pd.read_csv('scan_posB.csv')

# Transformation matrix (maps A's points into B's frame)
T = np.array([
    [0, 1, -1.3],
    [-1,  0, 0],
    [0,  0, 1]
])

points_a_h = np.vstack([scan_a['x'], scan_a['y'], np.ones(len(scan_a))])  # shape (3, N)
points_a_transformed = T @ points_a_h                                     # T r = r'
a_prime_x = points_a_transformed[0, :]
a_prime_y = points_a_transformed[1, :]


# Plot A' and B together
plt.figure(figsize=(8, 8))
plt.scatter(a_prime_x, a_prime_y, s=5, label="A' (transformed into B's frame)", alpha=0.7)
plt.scatter(scan_b['x'], scan_b['y'], s=5, label='B (original frame)', alpha=0.7)

plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title("Fused scan in B's frame")
plt.legend()
plt.axis('equal')
plt.grid(True)
plt.savefig('fused_plot.png', dpi=200)
plt.show()