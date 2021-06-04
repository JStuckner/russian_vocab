import random
import sys
import glob
import json
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5 import QtGui
from PyQt5 import QtCore


def load_vocab():
    with open("vocab\\all_vocab.json", encoding='utf-8-sig') as j:
        vocab = json.load(j)
    return vocab


class QLabelClickable(QtWidgets.QLabel):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QLabel.__init__(self, parent)

    def mousePressEvent(self, ev):
        self.clicked.emit()


class App(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.unlearned_vocab = []
        self.all_vocab = []
        self.index = 0
        self.grouped = False
        self.group_size = 6
        self.current_book = "All"
        self.current_chapter = "All"
        self.current_part = "All"
        self.skipped = -1

        self.load_vocab()

        # GUI
        self.title = 'Russian Vocab App'
        self.left = 500
        self.top = 500
        self.width = 320
        self.height = 200
        self.initUI()

        self.initShortcuts()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # buttons
        but_prev = QtWidgets.QPushButton("Previous", self)
        but_prev.clicked.connect(self.but_prev_click)
        but_next = QtWidgets.QPushButton("Next", self)
        but_next.clicked.connect(self.but_next_click)
        hbox_buttons = QtWidgets.QHBoxLayout()
        hbox_buttons.addWidget(but_prev)
        hbox_buttons.addWidget(but_next)

        # labels
        self.left_label = QLabelClickable("")
        self.right_label = QLabelClickable("")
        self.left_label.clicked.connect(self.left_label_click)
        self.right_label.clicked.connect(self.right_label_click)
        hbox_labels = QtWidgets.QHBoxLayout()
        hbox_labels.addWidget(self.left_label)
        hbox_labels.addWidget(self.right_label)
        hbox_labels.addStretch(2)
        for l in [self.left_label, self.right_label]:
            l.setStyleSheet(
                "border: 2px solid black; min-width: 300; max-width:300; background-color: white; min-height: 350")
            l.setWordWrap(True)
            l.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        # options
        self.rad_all = QtWidgets.QRadioButton("Show all")
        self.rad_russian = QtWidgets.QRadioButton("Russian only")
        self.rad_english = QtWidgets.QRadioButton("English only")
        vbox_radios = QtWidgets.QVBoxLayout()
        vbox_radios.addWidget(self.rad_all)
        vbox_radios.addWidget(self.rad_english)
        vbox_radios.addWidget(self.rad_russian)
        self.rad_all.setChecked(True)

        # learned
        but_learned = QtWidgets.QPushButton("Learned", self)
        but_reset_learned = QtWidgets.QPushButton("Reset", self)
        but_learned.clicked.connect(self.but_learned_click)
        but_reset_learned.clicked.connect(self.reset_learned)
        hbox_learned = QtWidgets.QHBoxLayout()
        hbox_learned.addWidget(but_reset_learned)
        hbox_learned.addWidget(but_learned)
        hbox_learned.setStretch(1, 2)

        # grouping
        self.but_group = QtWidgets.QPushButton("Group", self)
        self.but_group.clicked.connect(self.but_group_clicked)
        vbox_group = QtWidgets.QVBoxLayout()
        vbox_group.addWidget(self.but_group)

        # # chapter and part select
        # # get number of chapters.
        # num_chapters = len(set([x['chapter'] for x in self.all_vocab]))
        # # get number of parts.
        # self.num_parts = []
        # for c in range(num_chapters):
        #     self.num_parts.append(len(set(x['part'] for x in self.all_vocab if x['chapter'] == c+1)))
        # # create chapter list box
        # self.list_chapters = QtWidgets.QComboBox(self)
        # self.list_chapters.addItem("All")
        # for c in range(num_chapters):
        #     self.list_chapters.addItem(''.join(('Chapter ', str(c+1))))
        # self.list_chapters.currentIndexChanged.connect(self.chapter_select)
        # self.list_parts = QtWidgets.QComboBox(self)
        # self.list_parts.addItem("All")
        # self.list_parts.currentIndexChanged.connect(self.part_select)
        # # layout

        self.list_books = QtWidgets.QComboBox(self)
        self.list_chapters = QtWidgets.QComboBox(self)
        self.list_parts = QtWidgets.QComboBox(self)
        self.list_books.addItem("All")
        self.list_chapters.addItem("All")
        self.list_parts.addItem("All")
        for b in self.all_vocab:
            self.list_books.addItem(b)
        self.list_books.currentIndexChanged.connect(self.book_select)
        self.list_chapters.currentIndexChanged.connect(self.chapter_select)
        self.list_parts.currentIndexChanged.connect(self.part_select)
        chapter_layout = QtWidgets.QVBoxLayout()
        chapter_layout.addWidget(self.list_books)
        chapter_layout.addWidget(self.list_chapters)
        chapter_layout.addWidget(self.list_parts)


        # layout
        master_layout = QtWidgets.QVBoxLayout()
        master_layout.addLayout(hbox_buttons)
        master_layout.addLayout(hbox_labels)
        master_layout.addLayout(hbox_learned)
        options_layout = QtWidgets.QHBoxLayout()
        options_layout.addLayout(chapter_layout)
        options_layout.addLayout(vbox_radios)
        options_layout.addLayout(vbox_group)
        master_layout.addLayout(options_layout)
        self.setLayout(master_layout)
        self.show()

    def initShortcuts(self):
        next = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Right),
                                   self)
        next.activated.connect(self.but_next_click)
        prev = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Left),
                                   self)
        prev.activated.connect(self.but_prev_click)
        show = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Space),
                                   self)
        show.activated.connect(self.show_answer)
        learn = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Up),
                                   self)
        learn.activated.connect(self.but_learned_click)

    def load_vocab(self):
        self.all_vocab = load_vocab()
        self.reset_learned()

    @pyqtSlot()
    def but_next_click(self):
        self.skipped += 1
        print(self.index, 'out of', len(self.unlearned_vocab))
        if len(self.unlearned_vocab) == 0:
            self.all_learned()
        else:
            self.index = self.index + 1
            if self.grouped is False:
                if self.index == len(self.unlearned_vocab):
                    self.index = 0
            else:
                if self.index == self.group_size or self.index == len(self.unlearned_vocab):
                    # try:
                    #     section = self.unlearned_vocab[0:self.group_size]
                    #     random.shuffle(section)
                    #     self.unlearned_vocab[0:self.group_size] = section
                    # except:
                    #     pass
                    self.index = 0
            self.update_text()

    @pyqtSlot()
    def but_prev_click(self):
        if len(self.unlearned_vocab) == 0:
            self.all_learned()
        else:
            self.index -= 1
            if self.index < 0:
                if self.grouped is False:
                    self.index = len(self.unlearned_vocab) - 1
                else:
                    self.index = self.group_size - 1
            self.update_text()

    def book_select(self):
        self.current_book = self.list_books.currentText()
        chapter_list = ["All"]
        self.list_chapters.clear()
        if self.current_book != "All":
            for c in self.all_vocab[self.current_book]:
                chapter_list.append(c)
        chapter_list.sort()
        self.list_chapters.addItems(chapter_list)
        #self.chapter_select()

    def chapter_select(self):
        self.current_chapter = self.list_chapters.currentText()
        if self.current_chapter == "":
            return
        part_list = ["All"]
        self.list_parts.clear()
        if self.current_chapter not in ["All", ""]:
            for p in self.all_vocab[self.current_book][self.current_chapter]:
                part_list.append(p)
        part_list.sort()
        self.list_parts.addItems(part_list)
        #self.reset_learned()

    def part_select(self):
        self.index = 0
        self.current_part = self.list_parts.currentText()
        if self.current_part == "":
            return
        self.reset_learned()

    def update_text(self):
        if self.rad_all.isChecked():
            self.right_label.setText(self.unlearned_vocab[self.index]['english'])
            self.left_label.setText(self.unlearned_vocab[self.index]['russian'])
        elif self.rad_english.isChecked():
            self.right_label.setText(self.unlearned_vocab[self.index]['english'])
            self.left_label.setText("")
        elif self.rad_russian.isChecked():
            self.right_label.setText("")
            self.left_label.setText(self.unlearned_vocab[self.index]['russian'])
        self.size_text()

    def size_text(self):
        for l in [self.left_label, self.right_label]:
            l.setFont(QtGui.QFont("Arial", 26))
            t = l.text()
            if len(t) > 50:
                l.setFont(QtGui.QFont("Arial", 20))
            for w in t.split():
                for word in w.split('<br>'):
                    if len(word) > 13:
                        l.setFont(QtGui.QFont("Arial", 20))

    def show_answer(self):
        self.right_label.setText(self.unlearned_vocab[self.index]['english'])
        self.left_label.setText(self.unlearned_vocab[self.index]['russian'])
        self.size_text()

    def left_label_click(self):
        self.left_label.setText(self.unlearned_vocab[self.index]['russian'])
        self.size_text()

    def right_label_click(self):
        self.right_label.setText(self.unlearned_vocab[self.index]['english'])
        self.size_text()

    @pyqtSlot()
    def but_learned_click(self):
        del self.unlearned_vocab[self.index]
        self.index = self.index - 1
        if self.index >= len(self.unlearned_vocab):
            self.index = len(self.unlearned_vocab) - 1
        self.skipped -= 1
        self.but_next_click()

    @pyqtSlot()
    def reset_learned(self):
        self.skipped = -1
        if self.current_chapter == "" or self.current_book == "" or self.current_part == "":
            return
        self.unlearned_vocab = []
        if self.current_book == "All":
            for b in self.all_vocab:
                for c in self.all_vocab[b]:
                    for p in self.all_vocab[b][c]:
                        for w in self.all_vocab[b][c][p]:
                            self.unlearned_vocab.append(
                                {"russian" : w["russian"],
                                 "english" : w["english"]})
        elif self.current_chapter == "All":
            b = self.current_book
            for c in self.all_vocab[b]:
                for p in self.all_vocab[b][c]:
                    for w in self.all_vocab[b][c][p]:
                        self.unlearned_vocab.append(
                            {"russian": w["russian"],
                             "english": w["english"]})
        elif self.current_part == "All":
            b = self.current_book
            c = self.current_chapter
            for p in self.all_vocab[b][c]:
                for w in self.all_vocab[b][c][p]:
                    self.unlearned_vocab.append(
                        {"russian": w["russian"],
                         "english": w["english"]})
        else:
            b = self.current_book
            c = self.current_chapter
            p = self.current_part
            for w in self.all_vocab[b][c][p]:
                self.unlearned_vocab.append(
                    {"russian": w["russian"],
                     "english": w["english"]})

        random.shuffle(self.unlearned_vocab)

    def all_learned(self):
        QtWidgets.QMessageBox.about(self,"Russian Vocab App",
                    ''.join(("Congradulations you learned all the words!\n",
                             str(self.skipped), " skip(s).   Reseting...")))
        print("Skipped: ", self.skipped)
        self.reset_learned()
        #self.but_next_click()

    @pyqtSlot()
    def but_group_clicked(self):
        if self.grouped:
            self.grouped = False
            self.group_index = 0
            self.but_group.setText('Group')
        else:
            self.grouped = True
            self.group_index = 0
            self.but_group.setText('Ungroup')


if __name__ == '__main__':
    load_vocab()
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
