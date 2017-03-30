from PyQt5 import QtCore
from battledamage.database_models import get_session, Material, Properity


# Material, temper, thickness ranges
class MaterialTreeModel(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.my_index = {}
        Session = get_session()
        self.session = Session()

    def index(self, row, column, parent=None):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        if parent.isValid():
            index_pointer = parent.internalPointer()
            # TODO: Implement?
        else:
            pass

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()
        # child_key_list = index.internalPointer()

    def rowCount(self, parent):
        if parent.isValid():
            pass
        else:
            pass

    def columnCount(self, parent):
        if not parent.isValid():
            return 1
        else:
            return 1

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            if index.parent == QtCore.QModelIndex():
                materials = self._blah()
                return materials[index.row()]

    def _blah(self):
        materials = self.session.query(Material.name).unique().sort()
        return materials
