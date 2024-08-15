# Julia and Mandelbrot Set Visualization Project

This project involves the generation and visualization of the Mandelbrot and Julia sets, including 3D projections onto a sphere and calculation of pre-images. The code is organized into different directories, each with specific functionality.

## Directory Structure

├── double_window

│ └── work.py

├── julia_cheio

│ └── julia_cheio.py

├── multibrot

│ └── new_version.py

├── pre_images

│ ├── contorno.py

│ └── pre.py

└── sphere

├── md1.py

└── ju1.py


## File Descriptions

### 1. Directory `double_window`
#### File: `work.py`
This script generates simultaneous visualizations of the Julia set in two separate windows, allowing for visual comparison between different parameterizations or rendering methods.

### 2. Directory `julia_cheio`
#### File: `julia_cheio.py`
This script visualizes the full Julia set using a conventional rendering approach in the complex plane. It generates a 2D visualization of the Julia set with coloring that reflects the number of iterations required for point divergence.

### 3. Directory `multibrot`
#### File: `new_version.py`
This code implements the generation of Multibrot sets, a generalization of the Mandelbrot set for exponents other than 2. The script generates 2D visualizations of these sets, allowing exploration of the complex dynamics produced by different exponent values.

### 4. Directory `pre_images`
#### File: `contorno.py`
This script visualizes the boundaries of the Julia set, focusing on delineating areas where the behavior of points changes from convergent to divergent. The visualization highlights regions of interest in the set.

#### File: `pre.py`
This script allows visualization of the pre-images of a specific point in the Julia set. Users can click on a point in the Julia set visualization, and the script calculates and displays the pre-images of that point, generating a visual representation of the values that iterate to the selected point.

### 5. Directory `sphere`
#### File: `md1.py`
This script projects the Mandelbrot set onto a three-dimensional sphere, providing a unique visualization of the set’s geometry. The projection is achieved by mapping each point in the complex plane to the sphere's surface using spherical coordinates. The 3D visualization is colored based on the number of iterations needed for divergence.

#### File: `ju1.py`
Similar to `md1.py`, this script projects the Julia set onto a three-dimensional sphere. The Julia set is mapped onto the sphere's surface, and the resulting 3D visualization is colored based on iteration counts, allowing exploration of the set’s complexity from a new geometric perspective.

## How to Run

1. **Install Dependencies**  
   Ensure you have Python 3.x installed along with the required libraries. You can install the dependencies using pip:
   ```bash
   pip install numpy matplotlib numba
   ```

2. **Navigate to the Directory**  
   Change to the directory containing the script you want to execute. For example, to run `work.py`, navigate to the `double_window` directory:
   ```bash
   cd double_window
   ```

3. **Run the Script**  
   Execute the script using Python:
   ```bash
   python work.py
   ```

4. **Interact with Visualizations**  
   Follow the on-screen instructions to interact with the visualizations. Depending on the script:
   - **`work.py`**: Allows simultaneous visualizations of Julia sets.
   - **`julia_cheio.py`**: Provides a full Julia set visualization.
   - **`new_version.py`**: Generates Multibrot sets.
   - **`contorno.py`**: Visualizes the boundaries of the Julia set.
   - **`pre.py`**: Calculates and displays pre-images for a point in the Julia set.
   - **`md1.py`**: Projects the Mandelbrot set onto a 3D sphere.
   - **`ju1.py`**: Projects the Julia set onto a 3D sphere.

## Requirements

- Python 3.x
- Numpy
- Matplotlib
- Numba
