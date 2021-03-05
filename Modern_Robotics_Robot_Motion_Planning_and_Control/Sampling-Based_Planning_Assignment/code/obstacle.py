from math import sqrt

class Obstacle():
    """Obstacle class"""
    
    def __init__(self, x_, y_, r_):
        self.x = x_
        self.y = y_
        self.r = r_

        self.pos = [self.x, self.y]

    def is_in_collision_point(self, pos):
        """Checks if point is in collision with object

        Parameters
        ----------
        pos : float
            x,y position of point to check collision for

        Returns
        -------
        b : bool
            True if in collision
            False if not in collision
        """
        x, y = pos
        return sqrt((self.x - x)**2 + (self.y - y)**2) < self.r

    def is_in_collision_line(self, a, b):
        """Checks line collision between two points for obstacle

        Parameters
        ----------
        a, b : float 2-tuples
            points to check for collision between

        Returns
        -------
        b : bool
            True if line between two points would be invalid,
            False if line between two points would be valid
        """
        return abs((b[0]-a[0])*self.x + (a[1]-b[1])*self.y + (a[0]-b[0])*b[1] + (b[1]-a[1])*a[0]) /\
                    sqrt((b[0]-b[1])**2 + (a[1]-b[1])**2 + 0.0000001)< self.r

    def __repr__(self):
        return (
            f"x: {self.x}\n" +
            f"y: {self.y}\n" +
            f"r: {self.r}\n"
        )