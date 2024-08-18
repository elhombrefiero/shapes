#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math
import numpy as np


def calculate_length_area_volume(length=None, area=None, volume=None):
    if length is None:
        if area is None or volume is None:
            raise ValueError(f'Cannot calculate length. Missing area ({area}) or volume ({volume})')
        new_length = volume / area
    else:
        new_length = length
    if area is None:
        if length is None or volume is None:
            raise ValueError(f'Cannot calculate area. Missing length ({length}) or volume ({volume})')
        new_flow_area = volume / length
    else:
        new_flow_area = area
    if volume is None:
        if length is None or area is None:
            raise ValueError(f'Cannot calculate volume. Missing length ({length} or area ({area})')
        new_volume = length * area
    else:
        new_volume = volume

    return new_length, new_flow_area, new_volume


class Volume:
    """ Volume comprises a starting elevation, a delta Z, an angle, and a flow area

    Input angle is in degrees
    The x_start and y_start are the inlet coordinates.

    This will be translated to a version that corresponds to the equivalent rectangle in matplotlib.
     MATPLOTLIB uses the bottom left corner as the input to the Rectangle class
    """
    x_bottom_left = None
    y_bottom_left = None

    x_bottom_right = None
    y_bottom_right = None

    x_bottom_middle = None
    y_bottom_middle = None

    x_middle_left = None
    y_middle_left = None

    x_middle_right = None
    y_middle_right = None

    x_top_left = None
    y_top_left = None

    x_top_right = None
    y_top_right = None

    x_top_middle = None
    y_top_middle = None

    inlet_coordinates = (None, None)
    outlet_coordinates = (None, None)

    x_cor = 0
    y_cor = 0
    angle_deg = 0
    angle_rad = 0
    flow_area = 0
    length = 0.0

    rect = None

    def rel_to_mtplt(self, x_start, y_start, r_angle):
        """ Converts the R inputs into a format for the Matplotlib plot rectangle.

            Also calculates the inlet and outlet coordinates"""
        # The angle used in matplotlib is 90 degrees off in the clockwise direction
        # The angle of rotation will be based on the r_angle
        r_angle_rad = math.radians(r_angle)
        m_angle = r_angle - 90.0
        m_angle_rad = math.radians(m_angle)
        m_angle_rad_180 = math.radians(m_angle + 180.0)

        print(f'x_start: {x_start}\ty_start: {y_start}\t')
        print(f'm_angle: {m_angle}')
        print(f'm_angle_180: {m_angle + 180}')

        # The starting position is the inlet of the volume.
        self.inlet_coordinates = (x_start, y_start)
        # The outlet coordinates use the length
        x_outlet = x_start + self.length*np.cos(r_angle_rad)
        y_outlet = y_start + self.length*np.sin(r_angle_rad)
        self.outlet_coordinates = (x_outlet, y_outlet)

        print(f'x_outlet: {x_outlet}\ty_outlet: {y_outlet}\t')

        # Matplotlib needs the corner.
        # These need an additional 90-0degree angle
        x1 = x_start + 0.5*self.flow_area*np.cos(m_angle_rad_180)
        y1 = y_start + 0.5*self.flow_area*np.sin(m_angle_rad_180)
        x2 = x_start + 0.5*self.flow_area*np.cos(m_angle_rad)
        y2 = y_start + 0.5*self.flow_area*np.sin(m_angle_rad)

        # TODO: Temporarily set one of the corners to this DELETE
        self.x_bottom_left = x1
        self.y_bottom_left = y1
        self.x_bottom_right = x2
        self.y_bottom_right = y2

        print(f'x1: {x1}\ty1: {y1}\t')

        self.rect = Rectangle((x1, y1), self.flow_area, self.length, angle=m_angle,
                              rotation_point=(x1, y1))

    def plot_me(self):

        fig, ax = plt.subplots()
        ax.add_patch(self.rect)
        inlet_coor = self.inlet_coordinates[0], self.outlet_coordinates[0]
        outlet_coor = self.inlet_coordinates[1], self.outlet_coordinates[1]
        ax.plot(inlet_coor, outlet_coor, 'o')
        # TODO: Delete

        ax.plot((self.x_bottom_left, self.x_bottom_right), (self.y_bottom_left, self.y_bottom_right), 'o')
        plt.autoscale()
        print(f'x,y: {self.rect.get_xy()}')
        print(f'Corners: {self.rect.get_corners()}')
        print(f'Inlet coordinates: {inlet_coor}')
        print(f'Outlet coordinates: {outlet_coor}')
        plt.show()

    def return_figure(self):
        pass

    def __init__(self, x_start, y_start, angle, length=None, area=None, volume=None):
        """ Initialize a volume.
            Based on the starting x,y coordinates, the angle, the length, and the area, determine the different points of the volume
            x_start and y_start are going to be the middle of the start of the volume
            angle will be in degrees:
                0 for a horizontal volume that is in the positive x-direction
                90 for a vertical volume pointing in the positive y-direction
                180 for a horizontal volume that is in the negative x-direction
                270 for a vertical volume pointing in the negative y-direction
                etc
        """

        # Calculate the length/area based on inputs
        self.length, self.flow_area, self.volume = calculate_length_area_volume(length, area, volume)

        # Figure out direction of angle based on cos/sin
        self.angle_deg = angle
        # self.angle_rad = angle*np.pi/180
        #
        # dx, dy = np.cos(self.angle_rad), np.sin(self.angle_rad)
        #
        # if dx >= 0.0:
        #     x1 = x_start
        #     x2 = x_start + dx*self.length
        # else:
        #     x1 = x_start + dx*self.length
        #     x2 = x_start
        # start_point_x = x1 - dx*self.flow_area/2.0
        # if dy >= 0.0:
        #     y1 = y_start
        #     y2 = y_start + dy*self.length
        # else:
        #     y1 = y_start + dy*self.length
        #     y2 = y_start
        # start_point_y = y1 - dy*self.length/2.0
        #
        self.inlet_coordinates = (x_start, y_start)
        # print(f'Inlet coordinates: {self.inlet_coordinates}')
        # self.outlet_coordinates = (x2, y2)

        self.rel_to_mtplt(x_start, y_start, angle)




if __name__ == '__main__':
    x = 0
    y = 0
    length = 10.0
    area = 2.0
    volume = 50.0
    angle = 15.0
    vol = Volume(x, y, angle, length=length, area=area, volume=volume)
    vol.plot_me()

