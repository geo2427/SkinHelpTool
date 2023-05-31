Base on the original 'tf_smoothSkinWeight.py' by Tom Ferstl found on createivecrash.com
http://www.creativecrash.com/maya/script/tf_smoothskinweight

Modified by : nuternativ
              nuttynew@hotmail.com
              http://nuternativtd.blogspot.com

How to use  : 1.Put averageVertexSkinWeightCmd.py(or .mll) to your plugin path. 
                (default is: C:\Program Files\Autodesk\<Version>\bin\plug-ins)
              2.Put averageVertexSkinWeightBrush.py to your python path. 
                (default is: C:\Documents and Settings\<username>\My Documents\maya\<Version>\scripts)
              3.Execute the python code below(make sure there's no ' ' white space at the beginning of all 3 lines).
/home/jioh.kim/maya/modules/averageVertexSkinWeight/


import averageVertexSkinWeightBrush
reload(averageVertexSkinWeightBrush)
averageVertexSkinWeightBrush.paint()



