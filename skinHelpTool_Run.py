#-*- coding: utf-8 -*-
import sys, imp


def skinHelpTool_Run():

    path = r'/home/jioh.kim/Desktop/pipe/skinHelpTool/'
    if path not in sys.path:
        sys.path.append(path)

    import skinHelpTool_UI as ui
    imp.reload(ui)

    global win
    try:
        win.close()
        win.deleteLater()
    except:
        pass
    
    win = ui.SkinWindow()
    win.show()


skinHelpTool_Run()
