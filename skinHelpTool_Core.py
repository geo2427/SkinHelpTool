#-*- coding: utf-8 -*-
import os, sys, imp, re
import maya.cmds as cmds
import maya.mel as mel
import pymel.all as pm


def AddItemList(scroll):

    '''
    for sel in pm.ls(sl=1):
        if sel.getShape() == None and pm.nodeType(sel) == 'transform':
            for grp in pm.ls(sel, dag=True):
                if pm.nodeType(grp)=='mesh':
                    obj = pm.pickWalk(grp, d='up')[0]
                    scroll.addItem(str(obj))
        else:
            scroll.addItem(str(sel))
    '''
    
    for sel in pm.ls(sl=1):
    
        if sel.getShape()==None and pm.nodeType(sel)=='transform':
            
            for x in pm.ls(sel, dag=True):
                if x.listRelatives(c=1, s=1, type='mesh'):
                    if x.intermediateObject.get() == 0:
                        scroll.addItem(str(x))
                        print(x)
        
        else:
            scroll.addItem(str(sel))
        

def ReplaceItemList(scroll):

    scroll.clear()
            
    for sel in pm.ls(sl=1):
    
        if sel.getShape()==None and pm.nodeType(sel)=='transform':
            
            for x in pm.ls(sel, dag=True):
                if x.listRelatives(c=1, s=1, type='mesh'):
                    if x.intermediateObject.get() == 0:
                        scroll.addItem(str(x))
        
        else:
            scroll.addItem(str(sel))
    

def RemoveItemList(scroll):
    scroll.clear()


############################################################################### 


def AvSm():
    
    print("Not Workin Yet")
    
    path = '/home/jioh.kim/Desktop/pipe/skinHelpTool/modules/plug-ins/averageVertexSkinWeight/'
    if path not in sys.path:
        sys.path.append(path)
    
    import averageVertexSkinWeightBrush
    imp.reload(averageVertexSkinWeightBrush)
    averageVertexSkinWeightBrush.paint()


def SmSkin():
    
    mel.eval('brSmoothWeightsToolCtx;')
    

def ngSkin():
    
    # path = '/home/jioh.kim/Desktop/pipe/skinHelpTool/modules/plug-ins/ngskintools-2.0.22-win64.msi'
    import ngSkinTools2;
    ngSkinTools2.open_ui()


def AvSW():
    
    # path = '/home/jioh.kim/Desktop/pipe/skinHelpTool/modules/plug-ins/AverageSkinWeights.py'
    from util.Tools.skinHelpTool import AverageSkinWeights as AvSW
    imp.reload(AvSW)
    AvSW.AverageSkinWeights()
    
    
def CopySkinOneToOne(driver, driven):
    
    tslNewShape = [driver.item(x).text() for x in range(driver.count())]
    tslOldShape = [driven.item(x).text() for x in range(driven.count())]
    
    if len(tslNewShape) == len(tslOldShape):

        for i in range(len(tslNewShape)):
            
            GoodSkin = pm.listHistory(pm.PyNode(tslNewShape[i]), groupLevels=True, pruneDagObjects=True, il=2, type='skinCluster')
            GoodFindJntList = [x.name() for x in GoodSkin[0].getInfluence()]
            GoodBindJntlist = []
            
            if ':' in GoodFindJntList[0]:
                GoodBindJntlist = [x.split(':')[1] for x in GoodFindJntList]
            else:
                GoodBindJntlist = GoodFindJntList
                
            BadSkin = pm.listHistory(pm.PyNode(tslOldShape[i]), groupLevels=True, pruneDagObjects=True, il=2, type='skinCluster')
            if BadSkin:
                BadFindJntList = [x.name() for x in BadSkin[0].getInfluence()]

                if not set(GoodBindJntlist) == set(BadFindJntList):
                    for Gjnt in GoodBindJntlist:
                        if Gjnt in BadFindJntList:
                            continue
                        else:
                            try:
                                pm.skinCluster(tslOldShape[i], edit=1, ai=Gjnt, lw=1, dr=4, tsb=1)
                            except:
                                pass
                    pm.copySkinWeights(ss=GoodSkin[0], ds=BadSkin[0], nm=1, sa='closestPoint', ia='closestJoint')
                    pm.displayInfo('AddJnt & Copy Skin: ' + tslNewShape[i] + ' >> ' + tslOldShape[i])
                    
                else:
                    pm.copySkinWeights(ss=GoodSkin[0], ds=BadSkin[0], nm=1, sa='closestPoint', ia='closestJoint')
                    pm.displayInfo('Copy Skin: ' + tslNewShape[i] + ' >> ' + tslOldShape[i])
                    
            else:
                newJntList = [x for x in GoodBindJntlist if pm.objExists(x)]
                pm.skinCluster(newJntList, tslOldShape[i], tsb=1)
                BadSkin = pm.listHistory(pm.PyNode(tslOldShape[i]), groupLevels=True, pruneDagObjects=True, il=2, type='skinCluster')
                pm.copySkinWeights(ss=GoodSkin[0], ds=BadSkin[0], nm=1, sa='closestPoint', ia='closestJoint')
                pm.displayInfo('Bind & Copy Skin: ' + tslNewShape[i] + ' >> ' + tslOldShape[i])
                
    else:
        pm.warning('Driver Index and Driven Index is Different')

    
def CopySkinOneToAll(driver, driven):
    
    tslNewShape = [driver.item(x).text() for x in range(driver.count())]
    tslOldShape = [driven.item(x).text() for x in range(driven.count())]

    GoodSkin = pm.listHistory(pm.PyNode(tslNewShape[0]), groupLevels=True, pruneDagObjects=True, il=2, type='skinCluster')
    GoodFindJntList = [x.name() for x in GoodSkin[0].getInfluence()]
    GoodBindJntlist = []

    if ':' in GoodFindJntList[0]:
        GoodBindJntlist = [x.split(':')[1] for x in GoodFindJntList]
    else:
        GoodBindJntlist = GoodFindJntList

    for changeObjs in tslOldShape:
        BadSkin = pm.listHistory(pm.PyNode(changeObjs), groupLevels=True, pruneDagObjects=True, il=2, type='skinCluster')

        if BadSkin:
            BadFindJntList = [x.name() for x in BadSkin[0].getInfluence()]
            addJntList = [x for x in GoodBindJntlist if not (x in BadFindJntList) * (pm.objExists(x))]
            if addJntList:
                pm.skinCluster(changeObjs, edit=1, ai=addJntList, lw=1, dr=4, tsb=1)
            pm.copySkinWeights(ss=GoodSkin[0], ds=BadSkin[0], nm=1, sa='closestPoint', ia='closestJoint')
            pm.displayInfo('Bind & Copy Skin: ' + tslNewShape[0] + ' >> ' + changeObjs)

        else:
            newJntList = [x for x in GoodBindJntlist if pm.objExists(x)]
            pm.skinCluster(GoodBindJntlist, changeObjs, tsb=1)
            BadSkin = pm.listHistory(pm.PyNode(changeObjs), groupLevels=True, pruneDagObjects=True, il=2, type='skinCluster')
            pm.copySkinWeights(ss=GoodSkin[0], ds=BadSkin[0], nm=1, sa='closestPoint', ia='closestJoint')
            pm.displayInfo('Bind & Copy Skin: ' + tslNewShape[0] + ' >> ' + changeObjs)
            

def artToInteractive():
    
    selL = pm.ls(sl=1)
    for sel in selL:
        if 'vtx' in str(sel):
            obj = sel.split('.')[0]
            pm.select(obj)
    
    # Normalize
    mel.eval('''
            doNormalizeWeightsArgList 1 {"2"};
            ''')

    # Interactive
    mel.eval('''
            doNormalizeWeightsArgList 1 {"4"};
            ''')

    pm.select(selL)


def artToPost():

    selL = pm.ls(sl=1)
    for sel in selL:
        if 'vtx' in str(sel):
            obj = sel.split('.')[0]
            pm.select(obj)
    
    # Post
            # EnableWeightPostNrm;
    mel.eval('''
            doNormalizeWeightsArgList 1 {"3"};
            ''')

    pm.select(selL)


def artFlood(*arg):
    mel.eval('artAttrSkinPaintCtx -e -clear `currentCtx`;')
    
    
def Re(*arg):
    mel.eval('ArtPaintSkinWeightsTool')
    mel.eval('artAttrPaintOperation artAttrSkinPaintCtx Replace;')


def Sm(*arg):
    mel.eval('ArtPaintSkinWeightsTool')
    mel.eval('artAttrPaintOperation artAttrSkinPaintCtx Smooth;')
    
    
def P0(*arg):
    mel.eval('artAttrSkinPaintCtx -e -opacity 1.0 `currentCtx`;')
    mel.eval('artSkinSetSelectionValue 0 false artAttrSkinPaintCtx artAttrSkin;')

def P1(*arg):
    mel.eval('artAttrSkinPaintCtx -e -opacity 0.05 `currentCtx`;')
    mel.eval('artSkinSetSelectionValue 1 false artAttrSkinPaintCtx artAttrSkin;')

def P2(*arg):
    mel.eval('artAttrSkinPaintCtx -e -opacity 0.1 `currentCtx`;')
    mel.eval('artSkinSetSelectionValue 1 false artAttrSkinPaintCtx artAttrSkin;')
    
def P3(*arg):
    mel.eval('artAttrSkinPaintCtx -e -opacity 0.3 `currentCtx`;')
    mel.eval('artSkinSetSelectionValue 1 false artAttrSkinPaintCtx artAttrSkin;')
    
def P4(*arg):
    mel.eval('artAttrSkinPaintCtx -e -opacity 0.5 `currentCtx`;')
    mel.eval('artSkinSetSelectionValue 1 false artAttrSkinPaintCtx artAttrSkin;')

def P5(*arg):
    mel.eval('artAttrSkinPaintCtx -e -opacity 1 `currentCtx`;')
    mel.eval('artSkinSetSelectionValue 1 false artAttrSkinPaintCtx artAttrSkin;')
    
    
def AvP0(*arg):
    mel.eval('artSkinSetSelectionValue 0 false artAttrSkinPaintCtx artAttrSkin;')
    # mel.eval('artAttrSkinPaintCtx -e -opacity 0.1 `currentCtx`;')
    
def AvP1(*arg):
    mel.eval('artSkinSetSelectionValue 0.1 false artAttrSkinPaintCtx artAttrSkin;')
    # mel.eval('artAttrSkinPaintCtx -e -opacity 0.1 `currentCtx`;')
    

def AvP2(*arg):
    mel.eval('artSkinSetSelectionValue 0.25 false artAttrSkinPaintCtx artAttrSkin;')
    # mel.eval('artAttrSkinPaintCtx -e -opacity 0.1 `currentCtx`;')

def AvP3(*arg):
    mel.eval('artSkinSetSelectionValue 0.5 false artAttrSkinPaintCtx artAttrSkin;')
    # mel.eval('artAttrSkinPaintCtx -e -opacity 0.1 `currentCtx`;')

def AvP4(*arg):
    mel.eval('artSkinSetSelectionValue 0.75 false artAttrSkinPaintCtx artAttrSkin;')
    # mel.eval('artAttrSkinPaintCtx -e -opacity 0.1 `currentCtx`;')

def AvP5(*arg):
    mel.eval('artSkinSetSelectionValue 1 false artAttrSkinPaintCtx artAttrSkin;')
    # mel.eval('artAttrSkinPaintCtx -e -opacity 0.1 `currentCtx`;')

    
def AL(*arg):
    
    mel.eval('artSkinLockInf artAttrSkinPaintCtx 1;')
    mel.eval('artSkinInvLockInf artAttrSkinPaintCtx 1;')

    
def AUL(*arg):

    mel.eval('artSkinLockInf artAttrSkinPaintCtx 0;')
    mel.eval('artSkinInvLockInf artAttrSkinPaintCtx 0;')
