#-*- coding: utf-8 -*-
import sys, imp, os
import pymel.all as pm
import maya.mel as mel
from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial

import skinHelpTool_Core as core
imp.reload(core)

icon_path = "/home/jioh.kim/Desktop/pipe/skinHelpTool/modules/icons/"


class SkinWindow(QtWidgets.QMainWindow):
    TITLE = 'SkinHelpTool'
    VERSION  = '001'

    def __init__(self, parent=None):
        super(SkinWindow, self).__init__()

        self.setWindowTitle("{}_v{}".format(self.TITLE, self.VERSION))
        self.setGeometry(1600,400,400,500)
        self.center()
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(self.SkinUI())
        # main_layout.addLayout(self.popupItem_TEST1())
        
        widget = QtWidgets.QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
        
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def SkinUI(self):
        
        #FONT
        nfont = QtGui.QFont()
        nfont.setPointSize(11)
        nfont.setBold(True)
        
        # WIDGET
        self.driver_text = QtWidgets.QLabel("[    driver    ]", self, alignment=QtCore.Qt.AlignCenter)
        self.driver_scroll = QtWidgets.QListWidget(self, minimumHeight=200, minimumWidth=160)
        self.driver_replace_btn = QtWidgets.QPushButton("Add", self)
        self.driver_remove_btn = QtWidgets.QPushButton("Remove", self)
        self.to_text = QtWidgets.QLabel(">>", self)
        self.driven_text = QtWidgets.QLabel("[    driven    ]", self, alignment=QtCore.Qt.AlignCenter)
        self.driven_scroll = QtWidgets.QListWidget(self, minimumHeight=200, minimumWidth=160)
        self.driven_replace_btn = QtWidgets.QPushButton("Add", self)
        self.driven_remove_btn = QtWidgets.QPushButton("Remove", self)
        self.copyToOne_btn = QtWidgets.QPushButton("One to One", self, fixedHeight=40, fixedWidth=110, styleSheet="background: rgb(110,110,140);")
        self.copyToAll_btn = QtWidgets.QPushButton("One to All", self, fixedHeight=40, fixedWidth=110, styleSheet="background: rgb(110,110,140);")
        
        self.flood_btn = QtWidgets.QPushButton("Flood", self, fixedHeight=40, styleSheet="background: rgb(140,90,120);")
        self.replace_btn = QtWidgets.QPushButton("Replace", self, fixedHeight=35)
        self.smooth_btn = QtWidgets.QPushButton("Smooth", self, fixedHeight=35)
        self.toInteractive_btn = QtWidgets.QPushButton("Interactive", self)
        self.toPost_btn = QtWidgets.QPushButton("Post", self)
        self.lockAll_btn = QtWidgets.QPushButton("Lock All", self)
        self.unlockAll_btn = QtWidgets.QPushButton("UnLock All", self)
        self.avgSmooth_plg_btn = QtWidgets.QPushButton("AvgVtx(X)", self, fixedHeight=45, font=nfont)
        self.avgWeight_plg_btn = QtWidgets.QPushButton("AvgSkin", self, fixedHeight=45, font=nfont)
        self.smoothSkin_plg_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path+"/brSmoothWeights.svg"), iconSize=QtCore.QSize(31,35))
        self.ngSkin_plg_btn = QtWidgets.QPushButton(self, icon=QtGui.QIcon(icon_path+"/ngSkinTool.png"), iconSize=QtCore.QSize(31,35))
        
        self.opacity_text = QtWidgets.QLabel(" opacity :  ")
        self.opacity01 = QtWidgets.QPushButton("0.0", fixedHeight=35, styleSheet="background: rgb(0,0,0);")
        self.opacity02 = QtWidgets.QPushButton("0.05", fixedHeight=35, styleSheet="background: rgb(50,50,50);")
        self.opacity03 = QtWidgets.QPushButton("0.1", fixedHeight=35, styleSheet="background: rgb(75,75,75);")
        self.opacity04 = QtWidgets.QPushButton("0.3", fixedHeight=35, styleSheet="background: rgb(130,130,130);")
        self.opacity05 = QtWidgets.QPushButton("0.5", fixedHeight=35, styleSheet="background: rgb(175,175,175);")
        self.opacity06 = QtWidgets.QPushButton("1.0", fixedHeight=35, styleSheet="background: rgb(255, 255, 255);")
        self.value_text = QtWidgets.QLabel("    value :  ")
        self.value01 = QtWidgets.QPushButton("0.0", fixedHeight=35, styleSheet="background: rgb(0,0,0);")
        self.value02 = QtWidgets.QPushButton("0.1", fixedHeight=35, styleSheet="background: rgb(50,50,50);")
        self.value03 = QtWidgets.QPushButton("0.25", fixedHeight=35, styleSheet="background: rgb(75,75,75);")
        self.value04 = QtWidgets.QPushButton("0.5", fixedHeight=35, styleSheet="background: rgb(130,130,130);")
        self.value05 = QtWidgets.QPushButton("0.75", fixedHeight=35, styleSheet="background: rgb(175,175,175);")
        self.value06 = QtWidgets.QPushButton("1.0", fixedHeight=35, styleSheet="background: rgb(255, 255, 255);")
        
        # CONNECT
        self.driver_replace_btn.clicked.connect(partial(core.ReplaceItemList, self.driver_scroll))
        self.driver_remove_btn.clicked.connect(partial(core.RemoveItemList, self.driver_scroll))
        self.driven_replace_btn.clicked.connect(partial(core.ReplaceItemList, self.driven_scroll))
        self.driven_remove_btn.clicked.connect(partial(core.RemoveItemList, self.driven_scroll))
        self.copyToOne_btn.clicked.connect(partial(core.CopySkinOneToOne, self.driver_scroll, self.driven_scroll))
        self.copyToAll_btn.clicked.connect(partial(core.CopySkinOneToAll, self.driver_scroll, self.driven_scroll))
        
        self.flood_btn.clicked.connect(partial(core.artFlood))
        self.replace_btn.clicked.connect(partial(core.Re))
        self.smooth_btn.clicked.connect(partial(core.Sm))
        self.toInteractive_btn.clicked.connect(partial(core.artToInteractive))
        self.toPost_btn.clicked.connect(partial(core.artToPost))
        self.lockAll_btn.clicked.connect(partial(core.AL))
        self.unlockAll_btn.clicked.connect(partial(core.AUL))
        self.avgSmooth_plg_btn.clicked.connect(partial(core.AvSm))
        self.avgWeight_plg_btn.clicked.connect(partial(core.AvSW))
        self.smoothSkin_plg_btn.clicked.connect(partial(core.SmSkin))
        self.ngSkin_plg_btn.clicked.connect(partial(core.ngSkin))
        self.opacity01.clicked.connect(partial(core.P0))
        self.opacity02.clicked.connect(partial(core.P1))
        self.opacity03.clicked.connect(partial(core.P2))
        self.opacity04.clicked.connect(partial(core.P3))
        self.opacity05.clicked.connect(partial(core.P4))
        self.opacity06.clicked.connect(partial(core.P5))
        self.value01.clicked.connect(partial(core.AvP0))
        self.value02.clicked.connect(partial(core.AvP1))
        self.value03.clicked.connect(partial(core.AvP2))
        self.value04.clicked.connect(partial(core.AvP3))
        self.value05.clicked.connect(partial(core.AvP4))
        self.value06.clicked.connect(partial(core.AvP5))
        
        # LAYOUT
        skinDriverAdd_layout = QtWidgets.QHBoxLayout()
        skinDriverAdd_layout.addWidget(self.driver_replace_btn)
        skinDriverAdd_layout.addWidget(self.driver_remove_btn)
        
        skinDriver_layout = QtWidgets.QVBoxLayout()
        skinDriver_layout.addWidget(self.driver_text)
        skinDriver_layout.addWidget(self.driver_scroll)
        skinDriver_layout.addLayout(skinDriverAdd_layout)
        
        skinDrivenAdd_layout = QtWidgets.QHBoxLayout()
        skinDrivenAdd_layout.addWidget(self.driven_replace_btn)
        skinDrivenAdd_layout.addWidget(self.driven_remove_btn)
        
        skinDriven_layout = QtWidgets.QVBoxLayout()
        skinDriven_layout.addWidget(self.driven_text)
        skinDriven_layout.addWidget(self.driven_scroll)
        skinDriven_layout.addLayout(skinDrivenAdd_layout)
        
        scrollArea_layout = QtWidgets.QHBoxLayout()
        scrollArea_layout.addLayout(skinDriver_layout)
        scrollArea_layout.addWidget(self.to_text)
        scrollArea_layout.addLayout(skinDriven_layout)
        
        copyTo_layout = QtWidgets.QHBoxLayout()
        copyTo_layout.addWidget(self.copyToOne_btn, alignment=QtCore.Qt.AlignRight)
        copyTo_layout.addWidget(self.copyToAll_btn, alignment=QtCore.Qt.AlignLeft)
        
        skinCopy_layout = QtWidgets.QVBoxLayout()
        skinCopy_layout.addLayout(scrollArea_layout)
        skinCopy_layout.addLayout(copyTo_layout)
        
        opacity_layout = QtWidgets.QHBoxLayout(spacing=0)
        opacity_layout.addWidget(self.opacity_text)
        opacity_layout.addWidget(self.opacity01)
        opacity_layout.addWidget(self.opacity02)
        opacity_layout.addWidget(self.opacity03)
        opacity_layout.addWidget(self.opacity04)
        opacity_layout.addWidget(self.opacity05)
        opacity_layout.addWidget(self.opacity06)
        
        value_layout = QtWidgets.QHBoxLayout(spacing=0)
        value_layout.addWidget(self.value_text)
        value_layout.addWidget(self.value01)
        value_layout.addWidget(self.value02)
        value_layout.addWidget(self.value03)
        value_layout.addWidget(self.value04)
        value_layout.addWidget(self.value05)
        value_layout.addWidget(self.value06)

        paintOp_layout = QtWidgets.QHBoxLayout()
        paintOp_layout.addWidget(self.replace_btn)
        paintOp_layout.addWidget(self.smooth_btn)
        
        nomarlize_layout = QtWidgets.QHBoxLayout()
        nomarlize_layout.addWidget(self.toInteractive_btn)
        nomarlize_layout.addWidget(self.toPost_btn)
        
        lock_layout = QtWidgets.QHBoxLayout()
        lock_layout.addWidget(self.lockAll_btn)
        lock_layout.addWidget(self.unlockAll_btn)
                
        skinning_layout = QtWidgets.QVBoxLayout()
        skinning_layout.addLayout(paintOp_layout)
        skinning_layout.addLayout(opacity_layout)
        skinning_layout.addLayout(value_layout)
        skinning_layout.addWidget(self.flood_btn)
        skinning_layout.addLayout(nomarlize_layout)
        skinning_layout.addLayout(lock_layout)
        
        skinTool_layout = QtWidgets.QHBoxLayout()
        skinTool_layout.addWidget(self.avgSmooth_plg_btn)
        skinTool_layout.addWidget(self.avgWeight_plg_btn)
        skinTool_layout.addWidget(self.smoothSkin_plg_btn)
        skinTool_layout.addWidget(self.ngSkin_plg_btn)
        
        # GROUPBOX
        skinCopy_gb = QtWidgets.QGroupBox('Copy Skin Weights')
        skinCopy_gb.setLayout(skinCopy_layout)
        
        skinning_gb = QtWidgets.QGroupBox('Paint Skin Weights')
        skinning_gb.setLayout(skinning_layout)
        
        skinTool_gb = QtWidgets.QGroupBox('Skin Tool')
        skinTool_gb.setLayout(skinTool_layout)
                
        # FINAL
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(skinCopy_gb)
        main_layout.addWidget(skinning_gb)
        main_layout.addWidget(skinTool_gb)
        main_layout.addStretch(1)
        
        return main_layout

    #########################################################################
    
    
    def popupItem_TEST1(self):

        # WIDGET
        self.test_btn = QtWidgets.QPushButton("TEST", self, fixedHeight=50, fixedWidth=110)

        self.menuA = QtWidgets.QMenu()
        self.menuB = QtWidgets.QMenu()
        
        self.itemA = QtWidgets.QAction('A')
        self.itemB = QtWidgets.QAction('B')

        # CONNECT
        self.test_btn.pressed.connect(self.popup_press)
        self.test_btn.released.connect(self.popup_release)
        self.itemA.triggered.connect(print('trigger A'))
        self.itemB.triggered.connect(print('trigger B'))
        
        # FINAL
        TEST_lay = QtWidgets.QHBoxLayout()
        TEST_lay.addWidget(self.test_btn)

        return TEST_lay

    def popup_press(self):
        print('pressed')
        
        cursor_pos = QtGui.QCursor.pos()
        x = cursor_pos.x()
        y = cursor_pos.y()
        
        self.menuA.addAction(self.itemA)
        self.menuB.addAction(self.itemB)

        self.menuA.popup(QtCore.QPoint(x-120,y-80), self.itemA)
        self.menuB.popup(QtCore.QPoint(x+10,y-80), self.itemB)
        
    def popup_release(self):
        print('released')
                
        self.menuA.removeAction(self.itemA)
        self.menuB.removeAction(self.itemB)


    def popupItem_TEST2(self):

        self.button = QtWidgets.QPushButton("Show Menu", self)
        self.menu = QtWidgets.QMenu()
        self.actionA = QtWidgets.QAction('A')
        self.actionB = QtWidgets.QAction('B')
        
        self.menu.addAction(self.actionA)
        self.menu.addAction(self.actionB)
        self.button.clicked.connect(self.showMenu)
        
        TEST_lay = QtWidgets.QHBoxLayout()
        TEST_lay.addWidget(self.button)

        return TEST_lay


    def popupItem_TEST(self):
        
        test_btn = pm.button(l='TEST', w=70)
        pm.popupMenu(mm=1, b=1, p=test_btn)
        pm.menuItem('All', rp='NW')
        pm.menuItem('Sel', rp='NE')
        
        return test_btn