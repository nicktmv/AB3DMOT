import numpy as np
from filterpy.kalman import KalmanFilter

"""
Kalman filter-based tracker for 3D object detection.

This module contains the Kalman filter-based tracker class, which is used to track objects in 3D space. The tracker
maintains the state vector and covariance matrix for each object, and provides methods to update the state based on
measurements and predict the state forward in time.

The tracker is implemented using the filterpy library, which provides a KalmanFilter class that can be used to
implement a Kalman filter with a constant velocity model. The tracker uses this class to maintain the state and
covariance matrix, and provides methods to update the state based on measurements and predict the state forward in time.

The tracker is designed to be used with 3D object detection data, where each object is represented by a bounding box in
3D space. The tracker maintains the state vector for each object, which includes the position and velocity of the object
in 3D space, and provides methods to update the state based on measurements of the object's position and predict the
state forward in time.

Author: 
"""
# Constants for dimensions
DIM_X = 10  # State vector dimension
DIM_Z = 7  # Measurement vector dimension
VELOCITY_INDICES = slice(7, 10)  # Indices for velocity components in state vector

# Constants for initial uncertainties
INITIAL_POSITION_UNCERTAINTY = 10.0
INITIAL_VELOCITY_UNCERTAINTY = 1000.0

# Constants for process noise
VELOCITY_PROCESS_NOISE = 0.01


class Filter(object):
    """Base class for Kalman filter-based trackers."""
    def __init__(self, bbox3D, info, ID):
        self.initial_pos = bbox3D
        self.time_since_update = 0
        self.id = ID
        self.hits = 1  # number of total hits including the first detection
        self.info = info  # other information associated


class KF(Filter):
    def __init__(self, bbox3D, info, ID):
        super().__init__(bbox3D, info, ID)

        self.kf = KalmanFilter(dim_x=DIM_X, dim_z=DIM_Z)

        # State transition matrix for constant velocity model
        self.kf.F = np.eye(DIM_X)
        self.kf.F[0, 7] = self.kf.F[1, 8] = self.kf.F[2, 9] = 1

        # Measurement function, assuming direct observation of the first 7 state variables
        self.kf.H = np.zeros((DIM_Z, DIM_X))
        np.fill_diagonal(self.kf.H[:DIM_Z, :DIM_Z], 1)

        # Uncomment and adjust if measurement data is noisy
        # self.kf.R[0:, 0:] *= 10

        # Initial state uncertainty
        self.kf.P *= INITIAL_POSITION_UNCERTAINTY
        self.kf.P[VELOCITY_INDICES, VELOCITY_INDICES] *= INITIAL_VELOCITY_UNCERTAINTY

        # Process uncertainty, particularly for the velocity components
        self.kf.Q[VELOCITY_INDICES, VELOCITY_INDICES] *= VELOCITY_PROCESS_NOISE

        # Initialize state vector with initial position
        self.kf.x[:7] = self.initial_pos.reshape((7, 1))

    def compute_innovation_matrix(self):
        """Compute the innovation matrix for association with Mahalanobis distance."""
        return np.matmul(np.matmul(self.kf.H, self.kf.P), self.kf.H.T) + self.kf.R

    def get_velocity(self):
        """Return the object's velocity from the state vector."""
        return self.kf.x[VELOCITY_INDICES]
