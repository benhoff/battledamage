import sys
import enum
from os import path

import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from battledamage.models import (AreaTableModel,
                                 CalculatedAreaModel,
                                 MaterialModel)


class DamageCategory(enum.Enum):
    Category_1 = 1
    Category_2 = 2
    Category_3 = 3
    Category_4 = 4
    Category_5 = 5


class SubstructureWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # To be used for calculating the Irepair
        # calc is: Area * length**2
        self.repair_x = 0
        self.repair_y = 0
        self.category = None


class SkinWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.skin_material = None
        self.skin_thickness = None

        self.skin_running_load = None

        self.patch_material = None
        # Patch min thickness?
        self.patch_thickness = None
        self.repair_running_load = None

        self.possible_fasteners_selection = []
        # desired number of rows?
        self.category = None

    def rows_of_fasteners(self, fastener):
        pass


# STEP 1) EVAL DAMAGE

# STEP 2) MATERIALS

# STEP 3) Original structure capabilities

# Substructure
    # Tension = Ptu = Ftu X area
    # Compression
    # Bending

def calc_slenderness_ratio():
    pass

def calc_beaded_panel_moment_of_inertia():
    # see page 21 of ABDR handbook
    pass

# Skin
    # Max running load

# STEP 4) Repair Components
# Substructure
    # Tension
    # compression
    # bending

# STEP 5) Fastener
# Determine failure loads, shear and bearing
# Determine if other failure modes are safe
# transition, inter-fastener shear, tear-out, net section

# substrucutre: calculate the number of fasteners required
# and margin of safety

# skin calculate number of rows required
# margin of safety

# Step 6: Draw the repair

# Step 7: sanity check

# Step 8: repair instructions


def running_load(tensile_ultimate, thickness):
    return tensile_ultimate * thickness


def calc_original(original_ultimate,
                  original_thickness,
                  repair_ultimate,
                  repair_thickness):

    original_running_load = running_load(original_ultimate, original_thickness)
    repair = running_load(repair_ultimate, repair_thickness)

    margin_safety = (original_running_load/repair) - 1
    return margin_safety * 100


class MaterialDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add Material')
        model = MaterialModel()
        material_widget = QtWidgets.QTableView()
        material_widget.setModel(model)

        ok_push = QtWidgets.QPushButton('Ok')
        cancel_push = QtWidgets.QPushButton('Cancel')
        layout = QtWidgets.QGridLayout()
        layout.addWidget(material_widget, 0, 0)
        layout.addWidget(cancel_push, 1, 0)
        layout.addWidget(ok_push, 1, 1)

        self.setLayout(layout)
# REMOVE
class MomentOfInertia(enum.Enum):
    Rectangle = 0
    Circle = 1

# Might not need a delegate. See:
# http://doc.qt.io/qt-4.8/qt-itemviews-coloreditorfactory-example.html
class ComboBoxDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        # Only create an editor in column 1
        if index.column() != 1:
            return QtWidgets.QStyledItemDelegate.createEditor(parent,
                                                              option,
                                                              index)

        editor = QtWidgets.QComboBox()
        for m in MomentOfInertia:
            editor.addItem(m.name)
        return editor

    def setEditorData(self, editor, index):
        pass

    def setModelData(self):
        pass


class AreaMasterWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._area_model = AreaTableModel()
        self._calculated_area_model = CalculatedAreaModel()

        self.area_table_widget = QtWidgets.QTableView()
        # Item delegate
        # self.area_table_widget.setItemDelegateForColumn(
        # TODO: setitemdelegate
        self.area_table_widget.setModel(self._area_model)

        self.calculated_area_widget = QtWidgets.QTableView()
        self.calculated_area_widget.setModel(self._calculated_area_model)
        self.calculated_area_widget.horizontalHeader().hide()

        self.area_table_label = QtWidgets.QLabel('Rectangle Area Calcs')

        self.calculate_button = QtWidgets.QPushButton('Calc')
        self.calculate_button.clicked.connect(self.calc)

        self.material_button = QtWidgets.QPushButton('Material')
        self.material_button.clicked.connect(self.material)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.area_table_label, 0, 0)
        layout.addWidget(self.area_table_widget, 1, 0)
        layout.addWidget(self.calculated_area_widget, 1, 1)
        layout.addWidget(self.material_button, 2, 0)
        layout.addWidget(self.calculate_button, 3, 0)

        self.setLayout(layout)

    def material(self):
        dialog = MaterialDialog()
        dialog.exec_()

    def calc(self):
        d = self._area_model._data
        area_properties = self._calculated_area_model.calc_area_properties(d)
        if area_properties is None:
            return
        self._calculated_area_model.set_data(area_properties)
        self._calculated_area_model.update_all()


app = QtWidgets.QApplication(sys.argv)
main_window = QtWidgets.QMainWindow()
main_window.setWindowTitle('Battle Damage Repair')
main_tab_widget = QtWidgets.QTabWidget()


main_tab_widget.addTab(AreaMasterWidget(), 'Area')

main_window.setCentralWidget(main_tab_widget)
main_window.show()

app.exec_()
