import os
import importlib.util

if importlib.util.find_spec("hou") is None:
    from PySide6 import QtWidgets
else:
    from PySide2 import QtWidgets


class TreePopulation:
    def __init__(self, preset_tree_widget, folder_to_search):
        self.treeWidget = preset_tree_widget
        self.folder_to_search = folder_to_search

        self.grab_tree_list(0)

    def __call__(self, index):
        self.grab_tree_list(index)

    def fill_tree(self, tree_list):
        self.treeWidget.clear()
        parent = None
        for item in tree_list:
            treeWidget_item = QtWidgets.QTreeWidgetItem([item[0], item[1]])
            self.treeWidget.addTopLevelItem(treeWidget_item)

    def grab_tree_list(self, index):
        create_tree = TreeBuilder(self.folder_to_search)
        self.fill_tree(create_tree)


class TreeBuilder:
    def __init__(self, base_folder):
        self.dir_structure_list = []
        self.get_folder(base_folder)

    def __getitem__(self, index):
        return self.dir_structure_list[index]

    def __iter__(self):
        return iter(self.dir_structure_list)

    def __get__(self):
        return self.dir_structure_list

    def get_folder(self, base_folder):
        for root, dirs, files in os.walk(base_folder, topdown=False):

            for name in files:
                try:
                    path = os.path.join(root, name)

                    if root != base_folder:
                        pass
                    else:
                        self.dir_structure_list.append((name, path))

                except ValueError:
                    pass
        self.dir_structure_list.sort(key=lambda x: x[0])
