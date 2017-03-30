import enum
import numpy as np
from PyQt5 import QtCore


class MomentOfInertia(enum.Enum):
    Rectangle = 0
    Circle = 1


# For rectangles only
class CalculatedAreaModel(QtCore.QAbstractTableModel):
    def __init__(self, editable=False, parent=None):
        super().__init__(parent)
        self._header_data = ['Ixx',
                             'Iyy',
                             'Area',
                             'X Centroid',
                             'Y Centroid',
                             'X Gyration Radius',
                             'Y Gration Radius']

        self._data = np.array([0, 0, 0, 0, 0, 0, 0])
        self._editable = editable

    def flags(self, index):
        if self._editable:
            # TODO: Implement
            pass
        else:
            return super().flags(index)

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return self._header_data[section]
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return 1

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            element = self._data[index.row()]
            return '{0:.3f}'.format(element)

    def set_data(self, data):
        self._data = data

    def update_all(self):
        left_most_index = self.index(0, 0, QtCore.QModelIndex())
        bottom_index = self.index(self._data.shape[0], 0, QtCore.QModelIndex())
        self.dataChanged.emit(left_most_index, bottom_index)

    def calc_area_properties(self, dimensions):
        # Do a copy so that we can manipulate the data without reprecussions
        dimensions = np.copy(dimensions)
        # Remove all rows that have an x or y with a value of zero
        x = dimensions[:, 0]

        x_zero_indicies = np.where(x == 0)[0]
        dimensions = np.delete(dimensions, x_zero_indicies, axis=0)

        y = dimensions[:, 1]
        y_zero_indicies = np.where(y == 0)[0]
        dimensions = np.delete(dimensions, x_zero_indicies, axis=0)
        if not dimensions.any():
            return

        # Get x and y again after the rows have been cleaned.
        x = dimensions[:, 0]
        y = dimensions[:, 1]

        area = x * y
        x_bar = dimensions[:, 2]
        y_bar = dimensions[:, 3]
        # x distance from common reference
        x_dist_common_ref = dimensions[:, 4]
        # y distance from common reference
        y_dist_common_ref = dimensions[:, 5]

        sum_area = np.sum(area)

        centroid_x = np.sum(x_bar*area)/sum_area
        centroid_y = np.sum(y_bar*area)/sum_area

        # TODO: Verify this calc
        ixx = x*y**3/12 + (area * y_dist_common_ref**2)
        iyy = x**3*y/12 + (area * x_dist_common_ref**2)

        ixx_centroid = np.sum(ixx) + np.sum(area*y_bar**2) - (centroid_y* np.sum(area*y_bar))
        iyy_centroid = np.sum(iyy) + np.sum(area*x_bar**2) - (centroid_x*np.sum(area*x_bar))

        rhoxx = np.sqrt(ixx_centroid/sum_area)
        rhoyy = np.sqrt(iyy_centroid/sum_area)
        data = np.array([ixx_centroid,
                         iyy_centroid,
                         sum_area,
                         centroid_x,
                         centroid_y,
                         rhoxx,
                         rhoyy])

        return data
