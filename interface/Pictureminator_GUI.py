import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QFileDialog
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, pyqtProperty, QSize



class AnimatedButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(AnimatedButton, self).__init__(*args, **kwargs)
        self._iconSize = self.iconSize()
        self.animation = QPropertyAnimation(self, b"iconSize")  # animate the 'iconSize' property
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.OutElastic)
        self.scaleFactor = 0.95

    def enterEvent(self, event):
        # Enlarge the icon
        self._iconSize = self.iconSize()  # Store the original size
        enlargedWidth = int(self._iconSize.width() * self.scaleFactor)
        enlargedHeight = int(self._iconSize.height() * self.scaleFactor)
        self.animation.setStartValue(self._iconSize)
        self.animation.setEndValue(QSize(enlargedWidth, enlargedHeight))
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Restore the original icon size
        self.animation.setStartValue(self.iconSize())
        self.animation.setEndValue(self._iconSize)
        self.animation.start()
        super().leaveEvent(event)



class Ui_MainWindow(object):
    def __init__(self):
        self.sorting_path = ""
        print(self.sorting_path)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Pictureminator")
        MainWindow.resize(850, 650)
        MainWindow.setWindowIcon(QtGui.QIcon('E:/Git&GitHub/Pictureminator/interface/resources/pictureminator_170x170.png'))
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.lower_frame = QtWidgets.QFrame(self.centralwidget)
        self.lower_frame.setGeometry(QtCore.QRect(0, -11, 900, 711))
        self.lower_frame.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.lower_frame.setMouseTracking(False)
        self.lower_frame.setTabletTracking(False)
        self.lower_frame.setFocusPolicy(QtCore.Qt.TabFocus)
        self.lower_frame.setAutoFillBackground(False)
        self.lower_frame.setStyleSheet("background-color: #566D7E; border: 0px solid gray;")
        self.lower_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lower_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lower_frame.setObjectName("lower_frame")

        # Search bar
        self.search_bar = QtWidgets.QLineEdit(self.lower_frame)
        self.search_bar.setGeometry(QtCore.QRect(127, 580, 500, 31))
        self.search_bar.setPlaceholderText("Enter path here or browse to select")

        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Medium")
        font.setPointSize(10)
        font.setItalic(True)
        self.search_bar.setFont(font)
        self.search_bar.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.search_bar.setMouseTracking(True)
        self.search_bar.setFrame(True)
        self.search_bar.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.search_bar.setCursorPosition(20)
        self.search_bar.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.search_bar.setDragEnabled(False)
        self.search_bar.setReadOnly(False)
        self.search_bar.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.search_bar.setClearButtonEnabled(False)
        self.search_bar.setObjectName("search_bar")
        self.search_bar.setStyleSheet("""
            QLineEdit {
                padding-left: 10px;
                border-radius: 14.5px; 
                border: 2px solid rgb(232, 232, 232); 
                background-color: rgb(232, 232, 232);
                font-family: 'Franklin Gothic Medium'; 
                font-size: 10pt; 
                font-style: bold;
            }
        """)

        self.search_bar.textChanged.connect(self.onTextChanged)
        
        # Browse Button
        self.path_find = QtWidgets.QPushButton(self.lower_frame)
        self.path_find.setGeometry(QtCore.QRect(560, 571, 70, 50))
        self.path_find.setStyleSheet("background-color: rgba(255, 255, 255, 0); border: 0px solid gray; opacity: .2;")
        self.path_find.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("E:/Git&GitHub/Pictureminator/interface/resources/search_icon_06.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.path_find.setIcon(icon)
        self.path_find.setIconSize(QtCore.QSize(60, 50))
        self.path_find.setCheckable(False)
        self.path_find.setObjectName("path_find")
        self.path_find.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.path_find.clicked.connect(self.browsefiles)

        ## Switches
        # Monthly Switch
        self.monthly_switch = QtWidgets.QCheckBox(self.lower_frame)
        self.monthly_switch.setGeometry(QtCore.QRect(132, 530, 161, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(232, 232, 232))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(232, 232, 232))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.monthly_switch.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Demi")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.monthly_switch.setFont(font)
        self.monthly_switch.setAutoFillBackground(False)
        self.monthly_switch.setStyleSheet(
"QCheckBox {\n"
"    background-color: rgba(255, 255, 255, 0);\n"
"    border: 0px solid gray;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 50px;\n"
"    height: 50px;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    image: url(\"E:/Git&GitHub/Pictureminator/interface/resources/tw_on_06.png\");\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    image: url(\"E:/Git&GitHub/Pictureminator/interface/resources/tw_off_05.png\");\n"
"}")
        self.monthly_switch.setIconSize(QtCore.QSize(50, 50))
        self.monthly_switch.setCheckable(True)
        self.monthly_switch.setChecked(False)
        self.monthly_switch.setObjectName("monthly_switch")
        # self.monthly_switch.clicked.connect(self.update_switches)

        # Yearly Switch Button
        self.yearly_switch = QtWidgets.QCheckBox(self.lower_frame)
        self.yearly_switch.setGeometry(QtCore.QRect(315, 530, 151, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(232, 232, 232))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(232, 232, 232))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.yearly_switch.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Demi")
        font.setPointSize(11)
        self.yearly_switch.setFont(font)
        self.yearly_switch.setAutoFillBackground(False)
        self.yearly_switch.setStyleSheet(
"QCheckBox {\n"
"    background-color: rgba(255, 255, 255, 0);\n"
"    border: 0px solid gray;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 50px;\n"
"    height: 50px;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    image: url(\"E:/Git&GitHub/Pictureminator/interface/resources/tw_on_06.png\");\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    image: url(\"E:/Git&GitHub/Pictureminator/interface/resources/tw_off_05.png\");\n"
"}")
        self.yearly_switch.setIconSize(QtCore.QSize(50, 50))
        self.yearly_switch.setCheckable(True)
        self.yearly_switch.setChecked(False)
        self.yearly_switch.setObjectName("yearly_switch")
        # self.yearly_switch.clicked.connect(self.update_switches)

        # No Sorting Switch Button
        self.nosorting_switch = QtWidgets.QCheckBox(self.lower_frame)
        self.nosorting_switch.setGeometry(QtCore.QRect(487, 530, 131, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(232, 232, 232))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(232, 232, 232))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.nosorting_switch.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Franklin Gothic Demi")
        font.setPointSize(11)
        self.nosorting_switch.setFont(font)
        self.nosorting_switch.setAutoFillBackground(False)
        self.nosorting_switch.setStyleSheet(
"QCheckBox {\n"
"    background-color: rgba(255, 255, 255, 0);\n"
"    border: 0px solid gray;\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 50px;\n"
"    height: 50px;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    image: url(\"E:/Git&GitHub/Pictureminator/interface/resources/tw_on_06.png\");\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    image: url(\"E:/Git&GitHub/Pictureminator/interface/resources/tw_off_05.png\");\n"
"}")
        self.nosorting_switch.setIconSize(QtCore.QSize(50, 50))
        self.nosorting_switch.setCheckable(True)
        self.nosorting_switch.setChecked(True)
        self.nosorting_switch.setObjectName("nosorting_switch")
        # self.nosorting_switch.clicked.connect(self.update_switches)

        # Main Picture Setup
        self.label = QtWidgets.QLabel(self.lower_frame)
        self.label.setGeometry(QtCore.QRect(105, 60, 640, 420))
        self.label.setStyleSheet("border-radius: 5px; border: 4px solid rgb(232, 232, 232);")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("resources/vid_01_000.jpg"))
        self.label.setObjectName("label")

        # Start Sorting Button
        # self.start_sorting = QtWidgets.QPushButton(self.lower_frame)
        self.start_sorting = AnimatedButton(self.lower_frame)
        self.start_sorting.setGeometry(QtCore.QRect(645, 485, 91, 131))
        self.start_sorting.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("resources/pictureminator_124x204.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.start_sorting.setIcon(icon1)
        self.start_sorting.setIconSize(QtCore.QSize(125, 125))
        self.start_sorting.setObjectName("start_sorting")
        self.start_sorting.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.start_sorting.clicked.connect(self.start_sorting_clicked)

        self.nosorting_switch.clicked.connect(lambda: self.update_switches(self.nosorting_switch))
        self.yearly_switch.clicked.connect(lambda: self.update_switches(self.yearly_switch))
        self.monthly_switch.clicked.connect(lambda: self.update_switches(self.monthly_switch))


        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Change input text and set path variable
    def onTextChanged(self, text):
        self.sorting_path = text  # Update the variable with the current text
        # print(self.sorting_path)  # Print the updated variable for debugging purposes
        if text:  # If there is text entered, change the font style to bold and non-italic
                self.search_bar.setStyleSheet("""
            QLineEdit {
                padding-left: 10px;
                border-radius: 14.5px; 
                border: 2px solid rgb(232, 232, 232); 
                background-color: rgb(232, 232, 232);
                font-family: 'Segoe UI Variable Text'; 
                font-size: 10pt; 
                font-style: normal;
            }
        """)
        else:  # If the text is cleared, revert to the placeholder style
                self.setPlaceholderStyle()

    def setPlaceholderStyle(self):
        placeholderFont = self.search_bar.font()
        placeholderFont.setItalic(True)
        placeholderFont.setBold(False)
        self.search_bar.setFont(placeholderFont)
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pictureminator"))
        # self.search_bar.setText(_translate("MainWindow", "    Select Folder..."))
        self.monthly_switch.setText(_translate("MainWindow", "Monthly Sorting"))
        self.yearly_switch.setText(_translate("MainWindow", "Yearly Sorting"))
        self.nosorting_switch.setText(_translate("MainWindow", "No sorting"))

    def browsefiles(self):
        user_profile_path = os.environ.get('USERPROFILE', '')
        pictures_path = os.path.join(user_profile_path, 'Pictures')
        folder_path = QFileDialog.getExistingDirectory(None, 'Select Folder', pictures_path, QFileDialog.ShowDirsOnly)
        if folder_path:  # Make sure the user didn't cancel the dialog
            self.search_bar.setText(folder_path)

    def update_switches(self, clicked_switch):
        # If a switch is checked, uncheck the others.
        if clicked_switch.isChecked():
            if clicked_switch == self.monthly_switch:
                self.yearly_switch.setChecked(False)
                self.nosorting_switch.setChecked(False)
            elif clicked_switch == self.yearly_switch:
                self.monthly_switch.setChecked(False)
                self.nosorting_switch.setChecked(False)
            elif clicked_switch == self.nosorting_switch:
                self.yearly_switch.setChecked(False)
                self.monthly_switch.setChecked(False)
        else:
            # If a switch is unchecked, check the appropriate switch.
            if clicked_switch == self.monthly_switch or clicked_switch == self.nosorting_switch:
                # If monthly or nosorting is unchecked, check yearly.
                self.yearly_switch.setChecked(True)
            elif clicked_switch == self.yearly_switch:
                # If yearly is unchecked, check nosorting.
                self.nosorting_switch.setChecked(True)

    def start_sorting_clicked(self):
        # Check if self.sorting_path is not empty and is a valid path
        if self.sorting_path and os.path.exists(self.sorting_path):
            print(f"Path: {self.sorting_path}")
            # Check which switch is checked and print the appropriate message.
            if self.nosorting_switch.isChecked():
                print("Sort: No Sorting")
            elif self.yearly_switch.isChecked():
                print("Sort: Yearly Sorting")
            elif self.monthly_switch.isChecked():
                print("Sort: Monthly Sorting")
            else:
                print("No sorting option is selected.")
        else:
            print("No valid path provided.")

  
if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
