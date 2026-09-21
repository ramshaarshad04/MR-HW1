import pandas as pd
import matplotlib.pyplot as plt

# Load the two scans
scan_a = pd.read_csv('scan_posA.csv')
scan_b = pd.read_csv('scan_posB.csv')

# If your CSVs have no header, use: pd.read_csv('scanA.csv', header=None, names=['x','y'])

plt.figure(figsize=(8, 8))
plt.scatter(scan_a['x'], scan_a['y'], s=5, label='Scan A', alpha=0.7)
plt.scatter(scan_b['x'], scan_b['y'], s=5, label='Scan B', alpha=0.7)

plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Raw LiDAR scans in their own sensor frames')
plt.legend()
plt.axis('equal')  # important so shapes aren't distorted
plt.grid(True)
plt.savefig('scan_plot.png', dpi=200)
plt.show()
