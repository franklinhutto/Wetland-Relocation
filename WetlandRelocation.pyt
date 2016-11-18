#-------------------------------------------------------------------------------
# Name:        Wetland Relocation Toolbox / Poof
# Purpose:     Create a weighted sum overlay for best location to relocated wetland
# Author:      Franklin Hutto
# Created:     10/20  /2016
#-------------------------------------------------------------------------------
import arcpy
from arcpy.sa import*


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Poof]


class Poof(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Poof"
        self.description = "Weighted Sum"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0= arcpy.Parameter(
            displayName="Model Name",
            name="ModelName",
            datatype="String",
            parameterType="Required",
            direction="Input")
        params = [param0]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        #finds current mapdoucument and dataframe
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd,"Layers")[0]
        # need import table with layer Value
        #Raster imput
        inR1 = 'NWI'
        inR2 = 'STATELAND'

        # need to genrate this table
        #Weighted Sum Table
        WSTableObj = WSTable([
                    [inR1,"NWI_VALUES.VALUE", .5],
                    [inR2,"STATELAND_VALUES.VALUE",.5]
                    ])
        # load spatial extentsion
        arcpy.CheckOutExtension("Spatial")
        #Weighted Sum Overlay
        outWeightedSum = WeightedSum(WSTableObj)
        #outSetNull = setNull(InR*,..., "VALUE < 10)
        #Save the output
        ModelName = parameters[0].valueAsText
        savedPath ="Model.gdb/" + ModelName
        outWeightedSum.save(savedPath)
        arcpy.mapping.AddLayer(df, arcpy.mapping.Layer(savedPath),"TOP")
        arcpy.ApplySymbologyFromLayer_management (ModelName, 'Symbology')

        # need to delete stuff











