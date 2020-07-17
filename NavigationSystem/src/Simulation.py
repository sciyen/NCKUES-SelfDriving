import numpy as np
import Utils
import matplotlib.pyplot as plt

class Car():
    def __init__(self):
        """
        y ^
          |
        lb|_____________ lt 
          |             |   car moving direction
    (0,0) |-------------|------->x
        rb|_____________|rt
           
        unit: m
        """
        self.lt = np.array(( 1.3, 0.5))
        self.rt = np.array(( 1.3, -0.5))
        self.lb = np.array(( 0, 0.5))
        self.rb = np.array(( 0, -0.5))

class Simulation():
    def __init__(self, wayplanner, car_scale):
        self.waypoints = wayplanner.waypoints
        self.car = Car()
        self.scale = car_scale

    def plot_ways(self):
        plt.scatter(self.waypoints[:, 0], self.waypoints[:, 1], marker=".")
        return

    """
    Local coordinate: 
        Car coordinate. X direction is its way direction.
    Global coordinate:
        Buttom line is the X direction.

    Transform from local to global coordinate, which mean
    to rotate the basis with positive theta (x direction 
    in car coordinate).

    Input:
        current_state: car pose in global coordinate.
        point: 1d or 2d nparry, in local coordinate.
            format: [[x, y],
                     [x, y]....]
        scale: Zoom up the point in local coordinate.
    Return:
        point: 1d or 2d nparray in global coordinate.
    """
    def trans_local_to_global(self, current_state, point, scale=1):
        RM = Utils.get_rotation_matrix(current_state[2])
        # Broacasting plus
        new_p = current_state[0:2] + np.matmul(RM, point.T).T * scale
        return np.squeeze(new_p)

    """
    Plot line segment with point given in local coordinate.
    """
    def plot_with_local(self, current_state, start, end, args, scale=1):
        n_start = self.trans_local_to_global(current_state, start, scale)
        n_end   = self.trans_local_to_global(current_state, end, scale)
        plt.plot([n_start[0], n_end[0]], [n_start[1], n_end[1]], args)
        return 

    """
    Plot scatter with points given in local coordinate.
    Input:
        points: 1d or 2d nparray in local coordinate.
            1d for 1 point, 2d for multiple points.
    """
    def scatter_with_local(self, current_state, points, marker, color, scale=1):
        n_points   = self.trans_local_to_global(current_state, points, scale)
        plt.scatter(n_points[:,0], n_points[:,1], color=color, marker=marker)
        return 

    def plot_vehicle(self, current_state, scale=10):
        self.plot_with_local(current_state, self.car.rb, self.car.lb, 'r-', scale)
        self.plot_with_local(current_state, self.car.rt, self.car.lt, 'g-', scale)
        self.plot_with_local(current_state, self.car.lt, self.car.lb, 'k-', scale)
        self.plot_with_local(current_state, self.car.rt, self.car.rb, 'k-', scale)

        vec = current_state[3] * np.array(
                [np.cos(current_state[2]),
                 np.sin(current_state[2])])
        plt.arrow(current_state[0],
                  current_state[1],
                  vec[0], vec[1], width=1)
        return

