__author__ = 'mike'

import datetime
from django.utils import timezone
from django.db.models import Avg, Max, Min, StdDev

from startupshot.models import *
from production_and_mold_history.models import *
from inspection.models import *
from part.models import *

class jobReport:
    def __init__(self,jobNumber,dateFrom=None,dateTo=None):
        self.jobNumber = jobNumber
        self.reportDict = {}
        self.dateFrom = self.myDateHelper(dateFrom)
        self.dateTo = self.myDateHelper(dateTo)
        self.active_job = startUpShot.objects.filter(jobNumber=self.jobNumber).select_related('item')
        self.inspectionTypes = PartInspection.objects.get(item_Number__item_Number=self.active_job[0].item)
        self.dateList = []
        self.createMyReport()
        self.getDateStats()



    def getPHL(self):
        # Production History Log
        self.reportDict['phl'] = ProductionHistory.objects.filter(jobNumber__jobNumber=self.jobNumber,
        dateCreated__range=(self.dateFrom, self.dateTo),inspectorName__EmpJob__JobNum=6).select_related('item')
        self.myDateFinder('phl')


    def getVI(self):
        #   visual inspection
        if self.inspectionTypes.visual_inspection:
            self.reportDict['visualInspection']=visualInspection.objects.filter(jobID__jobNumber=self.jobNumber,\
            dateCreated__range=(self.dateFrom, self.dateTo))
            self.myDateFinder('visualInspection')


    def getPWI(self):
        #   part weight inspection
        if self.inspectionTypes.part_weight_inspection:
            self.reportDict['partWeightInspection']=partWeightInspection.objects.filter(jobID__jobNumber=self.jobNumber,
            dateCreated__range=(self.dateFrom, self.dateTo))
            self.myDateFinder('partWeightInspection')
            self.myStatsHelper('partWeightInspection','partWeight')

    def getSWI(self):
        #   shot weight inspection
        if self.inspectionTypes.shot_weight_inspection:
            self.reportDict['shotWeightInspection']=shotWeightInspection.objects.filter(\
                jobID__jobNumber=self.jobNumber,dateCreated__range=(self.dateFrom, self.dateTo))
            self.myDateFinder('shotWeightInspection')
            self.myStatsHelper('shotWeightInspection','partWeight')

    def getODI(self):
        #   outside diameter inspection
        if self.inspectionTypes.od_inspection:
            self.reportDict['od_inspection']=outsideDiameterInspection.objects.filter(
                jobID__jobNumber=self.jobNumber,dateCreated__range=(self.dateFrom, self.dateTo))
            self.myDateFinder('od_inspection')
            self.myStatsHelper('od_inspection','outsideDiameter')

    def getVOI(self):
        #   volume inspection
        if self.inspectionTypes.vol_inspection:
            self.reportDict['vol_inspection']=volumeInspection.objects.filter(
                jobID__jobNumber=self.jobNumber,dateCreated__range=(self.dateFrom, self.dateTo))
            self.myDateFinder('vol_inspection')
            self.myStatsHelper('vol_inspection','liquidWeight')


    def getNDI(self):
        #   neck diameter inspection
        if self.inspectionTypes.neck_diameter_inspection:
            self.reportDict['neckDiam_inspection']=neckDiameterInspection.objects.filter(
                jobID__jobNumber=self.jobNumber,dateCreated__range=(self.dateFrom, self.dateTo))
            self.myDateFinder('neckDiam_inspection')
            self.myDescStatsHelper('neckDiam_inspection')

    def getASI(self):
        #   assembly test inspection
        if self.inspectionTypes.assembly_test_inspection:
            self.reportDict['assembly_inspection']=assemblyInspection.objects.filter(\
                jobID__jobNumber=self.jobNumber,dateCreated__range=(self.dateFrom, self.dateTo))
            self.myDateFinder('assembly_inspection')


    def getCTI(self):
        #   carton temp inspection
        if self.inspectionTypes.carton_temp_inspection:
            self.reportDict['cartonTemp_inspection']=cartonTemperature.objects.filter(\
                jobID__jobNumber=self.jobNumber,dateCreated__range=(self.dateFrom, self.dateTo))

            self.myDateFinder('cartonTemp_inspection')
            self.myStatsHelper('cartonTemp_inspection','cartonTemp')


    def getVSI(self):
        #   vision system inspection
        if self.inspectionTypes.vision_system_inspection:
            self.reportDict['visionSys_inspection']=visionInspection.objects.filter(\
                jobID__jobNumber=self.jobNumber,dateCreated__range=(self.dateFrom, self.dateTo))

            self.myDateFinder('visionSys_inspection')


    def myDateHelper(self,myDate):
        if myDate is None:
            myDate = datetime.datetime.strptime('1900-01-01', '%Y-%m-%d')
            myDate = timezone.make_aware(myDate, timezone.get_current_timezone())
        return myDate


    def myDateFinder(self,dictID):
          self.dateList.append(self.reportDict[dictID].aggregate(Min('dateCreated'),Max('dateCreated')))

    def myStatsHelper(self,dictID,param):
        self.reportDict[dictID + 'Dict'] = self.reportDict[dictID].aggregate(Avg(param),
                                                                                Max(param),
                                                                                Min(param),
                                                                                StdDev(param))

    def getDateStats(self):
        # This will return the minimum and maximum date for all inspections

        # first map everything to a single dictionary
        finalMap = {}
        for d in self.dateList:
            finalMap.update(d)

        # then put all the values into a list
        seq = []
        for key, value in finalMap.iteritems():
            seq.append(value)

        # store the minimum and maximum values in the report dictionary
        self.reportDict['InspectionDates'] = {'dateCreated__min':min(seq),'dateCreated__max':max(seq)}


    def myDescStatsHelper(self,dictID):
        self.reportDict[dictID + 'Dict'] = {}
        self.reportDict[dictID + 'Dict']['numPass'] = self.reportDict[dictID].filter(param=1).count()
        self.reportDict[dictID + 'Dict']['numFail'] = self.reportDict[dictID].filter(param=0).count()
        self.reportDict[dictID + 'Dict']['totalInspections'] = self.reportDict[dictID + 'Dict']['numPass'] + \
            self.reportDict[dictID + 'Dict']['numFail']

        if self.reportDict[dictID + 'Dict']['totalInspections'] > 0 :
            self.reportDict[dictID + 'Dict']['passPerc'] = 100 * self.reportDict[dictID + 'Dict']['numPass'] / \
                                                           self.reportDict[dictID + 'Dict']['totalInspections']
        else:
            self.reportDict[dictID + 'Dict']['passPerc'] = 0


    def createMyReport(self):
        self.getASI() # Get Assembly Test Inspection
        self.getCTI() # Get Carton Temp Inspection
        self.getODI() # Get Outside Diameter Inspection
        self.getPHL() # Get Production History Log
        self.getPWI() # Get Part Weight Inspection
        self.getSWI() # Get Shot Weight Inspection
        self.getVI()  # Get Visual Inspection
        self.getVOI() # Get Volume Inspection
        self.getVSI() # Get Vision System Inspection

