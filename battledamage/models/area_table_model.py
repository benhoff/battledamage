import enum

from PyQt5 import QtCore
import numpy as np


# NOTE: Only for rectangles currently
class AreaTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = np.ndarray(shape=(3,6), dtype=float)
        self._data.fill(0)
        self._header_data = ['X',
                             'Y',
                             'X-Centroid',
                             'Y-Centroid',
                             'X Dist Common Ref',
                             'Y Dist Common Ref']

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            element = self._data[index.row()][index.column()]
            return str(element)

    def insertRow(self, row, parent=None):
        self._data = np.insert(self._data,
                               row,
                               np.zeros(shape=(0,3)),
                               axis=0)

        upper_index = self.index(row-1, 0, QtCore.QModelIndex())
        lower_index = self.index(row,
                                 self._data.shape[1],
                                 QtCore.QModelIndex())

        self.dataChanged.emit(upper_index, lower_index)

    def removeRow(self, row, parent=None):
        self._data = np.delete(self._data,
                               row,
                               axis=0)

        upper_index = self.index(row-1, 0, QtCore.QModelIndex())
        lower_index = self.index(self._data.shape[0],
                                 self._data.shape[1],
                                 QtCore.QModelIndex())

        self.dataChanged.emit(upper_index, lower_index)

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            try:
                value = eval(value)
                value = float(value)
            # TODO: Implement some sort of error handeling
            except (ValueError, SyntaxError):
                return False
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)

            if index.row() == self._data.shape[0] and index.column() == 1:
                self.insertRow(index.row() + 1)

            return True
        return False

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._header_data[section]
        elif orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return str(section + 1)
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

    def flags(self, index):
        flag = super().flags(index)
        flag |= QtCore.Qt.ItemIsEditable
        return flag
