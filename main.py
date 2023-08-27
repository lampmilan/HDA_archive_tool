import importlib.util
import os
import sys
import shutil
from tree_pop import TreePopulation


HOUDINI_CALL = False

if importlib.util.find_spec("hou") is None:
    from PySide6 import QtWidgets, QtUiTools, QtCore, QtGui
else:
    from PySide2 import QtWidgets, QtUiTools, QtCore, QtGui
    import hou

    HOUDINI_CALL = True

SCRIPT_LOC = os.path.abspath(sys.argv[0])
SCRIPT_DIR = os.path.dirname(SCRIPT_LOC)
UI_FILE = SCRIPT_DIR + "\\static\\ui\\archive_main_gui.ui"

print(UI_FILE)
VALID_FOLDER = (
    'C:\\Users\\lampm\\Documents\\houdini19.5\\otls',
    'C:\\Users\\lampm\\Documents\\houdini19.5\\otls\\archive'
)


def get_selected_path(tree_widget):
    selected_items = tree_widget.selectedItems()
    if selected_items:
        selected_item_path = selected_items[0].text(1)
        return selected_item_path
    else:
        return None


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        file_interface = os.path.join(UI_FILE)
        self.ui = QtUiTools.QUiLoader().load(file_interface, parentWidget=self)
        self.setWindowTitle("HDA Archive tool")
        if HOUDINI_CALL:
            stylesheet = hou.qt.styleSheet()
            self.setStyleSheet(stylesheet)

        #os.chmod(VALID_FOLDER[0], 0o777)
        #os.chmod(VALID_FOLDER[1], 0o777)

        self.ui.otls_treeWidget.setColumnHidden(1, True)
        self.ui.archive_treeWidget.setColumnHidden(1, True)

        self.otls_tree_pop = TreePopulation(self.ui.otls_treeWidget, VALID_FOLDER[0])
        self.archive_tree_pop = TreePopulation(self.ui.archive_treeWidget, VALID_FOLDER[1])

        self.ui.archive_treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.archive_treeWidget.customContextMenuRequested.connect(self._show_context_menu)

        self.ui.toArchiveButton.clicked.connect(self.move_to_archive)
        self.ui.toOtlsButton.clicked.connect(self.move_to_otls)

    def _show_context_menu(self, position):
        if HOUDINI_CALL:
            display_action1 = QtWidgets.QAction("Copy HDA to my pub")
        else:
            display_action1 = QtGui.QAction("Copy HDA to my pub")

        display_action1.triggered.connect(self.display_selection)
        menu = QtWidgets.QMenu(self.ui.archive_treeWidget)
        menu.addAction(display_action1)

        menu.exec_(self.ui.archive_treeWidget.mapToGlobal(position))

    def display_selection(self):
        column = self.ui.archive_treeWidget.currentColumn()
        text = self.ui.archive_treeWidget.currentItem().text(column)
        print("Copy " + text + " to my pub")

    def reset_trees(self):
        self.otls_tree_pop = TreePopulation(self.ui.otls_treeWidget, VALID_FOLDER[0])
        self.archive_tree_pop = TreePopulation(self.ui.archive_treeWidget, VALID_FOLDER[1])

    def move_to_archive(self):
        file = get_selected_path(self.ui.otls_treeWidget)
        shutil.move(file, VALID_FOLDER[1])
        self.reset_trees()
        if HOUDINI_CALL:
            hou.hda.reloadAllFiles(rescan=True)

    def move_to_otls(self):
        file = get_selected_path(self.ui.archive_treeWidget)
        shutil.move(file, VALID_FOLDER[0])
        self.reset_trees()
        if HOUDINI_CALL:
            hou.hda.reloadAllFiles(rescan=True)


# Create UI Window
if HOUDINI_CALL:

    my_window = MyWindow()
    my_window.show()

else:
    if __name__ == '__main__':
        app = QtWidgets.QApplication([])
        fb = MyWindow()
        fb.show()
        app.exec()
