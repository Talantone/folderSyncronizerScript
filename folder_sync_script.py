import os
import filecmp
import shutil
import sys
import logging
import time


class Node:
    def __init__(self, path):
        self.root_path = os.path.abspath(path)
        self.file_list = os.listdir(self.root_path)


class Synchronizer:
    def __init__(self):
        self.node_list = []

    def compare_folders(self):
        for node in self.node_list:
            if self.node_list.index(node) < len(self.node_list) - 1:
                node2 = self.node_list[self.node_list.index(node) + 1]
                self._compare_directories(node.root_path, node2.root_path)

    def _compare_directories(self, left, right):
        compare = filecmp.dircmp(left, right)
        if compare.common_dirs:
            for directory in compare.common_dirs:
                self._compare_directories(os.path.join(left, directory), os.path.join(right, directory))

        if compare.left_only:
            self._copy(compare.left_only, left, right)
        if compare.right_only:
            self._remove(compare.right_only, right)

        left_update = []

        if compare.diff_files:
            for difference in compare.diff_files:
                l_modified = os.stat(os.path.join(left, difference)).st_mtime
                r_modified = os.stat(os.path.join(right, difference)).st_mtime
                if l_modified > r_modified:
                    left_update.append(difference)

        self._copy(left_update, left, right)

    def _copy(self, file_list, src, destination):
        for file in file_list:
            path = os.path.join(src, os.path.basename(file))
            if os.path.isdir(path):
                shutil.copytree(path, os.path.join(destination, os.path.basename(file)))
                logging.info('Copied directory {} from {} to {}'.format(os.path.basename(path), os.path.dirname(path), destination))
                print('Copied directory {} from {} to {}'.format(os.path.basename(path), os.path.dirname(path), destination))
            else:
                shutil.copy2(path, destination)
                logging.info('Copied {} from {} to {}'.format(os.path.basename(path), os.path.dirname(path), destination))
                print('Copied {} from {} to {}'.format(os.path.basename(path), os.path.dirname(path), destination))


    def _remove(self, file_list, src):
        for file in file_list:
            path = os.path.join(src, os.path.basename(file))
            if os.path.isdir(path):
                shutil.rmtree(path)
                logging.info('Deleted directory {} from {}'.format(os.path.basename(path), os.path.dirname(path)))
                print('Deleted directory {} from {}'.format(os.path.basename(path), os.path.dirname(path)))
            else:
                os.remove(path)
                logging.info('Deleted {} from {}'.format(os.path.basename(path), os.path.dirname(path)))
                print('Deleted directory {} from {}'.format(os.path.basename(path), os.path.dirname(path)))


if __name__ == "__main__":
    synchrinizer = Synchronizer()
    folder1 = Node(sys.argv[1])
    folder2 = Node(sys.argv[2])
    synchrinizer.node_list.append(folder1)
    synchrinizer.node_list.append(folder2)
    logging.basicConfig(level=logging.INFO, filename=sys.argv[3], filemode="w")
    while True:
        synchrinizer.compare_folders()
        time.sleep(float(sys.argv[4]))

