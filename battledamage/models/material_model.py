import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtWidgets


class MaterialModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._header_data = ['Ftu',
                             'Fty',
                             'Fcy',
                             'Fsu',
                             'E',
                             'Ec',
                             'Fbru',
                             'Fbry']

        self._data = np.array([0, 0, 0, 0, 0, 0, 0, 0])

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return 1

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            element = self._data[index.row()]
            return '{0:.3f}'.format(element)

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            print('Horizontal')
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            print(section, self._header_data[section])
            return self._header_data[section]
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

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

    def flags(self, index):
        flag = super().flags(index)
        flag |= QtCore.Qt.ItemIsEditable
        return flag
