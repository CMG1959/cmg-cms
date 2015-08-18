__author__ = 'mike'

import datetime
from django.utils import timezone

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


    #
    # if inspectionTypes.part_weight_inspection:
    #     context_dic['partWeightInspection'] = partWeightInspection.objects.filter(jobID__jobNumber=jobNumber,
    #                                                                               dateCreated__range=(date_from, date_to))
    #     context_dic['partWeightInspectionDict'] = {}
    #     context_dic['partWeightInspectionDict'] = context_dic['partWeightInspection'].aggregate(Avg('partWeight'),
    #                                                                                             Max('partWeight'),
    #                                                                                             Min('partWeight'),
    #                                                                                             StdDev('partWeight'))
    #
    # if inspectionTypes.shot_weight_inspection:
    #     context_dic['shotWeightInspection'] = shotWeightInspection.objects.filter(jobID__jobNumber=self.jobNumber,
    #                                                                               dateCreated__range=(self.dateFrom, self.dateTo))
    #     context_dic['shotWeightInspectionDict'] = {}
    #     context_dic['shotWeightInspectionDict'] = context_dic['shotWeightInspection'].aggregate(Avg('shotWeight'),
    #                                                                                             Max('shotWeight'),
    #                                                                                             Min('shotWeight'),
    #                                                                                             StdDev('shotWeight'))
    #
    # if inspectionTypes.od_inspection:
    #     context_dic['od_inspection'] = outsideDiameterInspection.objects.filter(jobID__jobNumber=self.jobNumber,
    #                                                                             dateCreated__range=(self.dateFrom, self.dateTo))
    #     context_dic['od_inspectionDict'] = {}
    #     context_dic['od_inspectionDict'] = context_dic['od_inspection'].aggregate(
    #         Avg('outsideDiameter'),
    #         Max('outsideDiameter'),
    #         Min('outsideDiameter'),
    #         StdDev('outsideDiameter'))
    #
    # if inspectionTypes.vol_inspection:
    #     context_dic['vol_inspection'] = volumeInspection.objects.filter(jobID__jobNumber=self.jobNumber,
    #                                                                     dateCreated__range=(self.dateFrom, self.dateTo))
    #     context_dic['vol_inspectionDict'] = {}
    #     context_dic['vol_inspectionDict'] = context_dic['od_inspection'].aggregate(
    #         Avg('liquidWeight'),
    #         Max('liquidWeight'),
    #         Min('liquidWeight'),
    #         StdDev('liquidWeight'))
    #
    # if inspectionTypes.neck_diameter_inspection:
    #     context_dic['neckDiam_inspection'] = neckDiameterInspection.objects.filter(jobID__jobNumber=self.jobNumber,
    #                                                                                dateCreated__range=(self.dateFrom, self.dateTo))
    #     context_dic['neckDiam_inspectionDict'] = {}
    #     context_dic['neckDiam_inspectionDict']['numPass'] = context_dic['neckDiam_inspection'].filter(
    #         testResult=1).count()
    #     context_dic['neckDiam_inspectionDict']['numFail'] = context_dic['neckDiam_inspection'].filter(
    #         testResult=0).count()
    #     context_dic['neckDiam_inspectionDict']['totalInspections'] = context_dic['neckDiam_inspectionDict']['numPass'] + \
    #                                                                  context_dic['neckDiam_inspectionDict']['numFail']
    #
    #     ### Calculate percentage passed
    #     if context_dic['neckDiam_inspectionDict']['totalInspections'] > 0:
    #         context_dic['neckDiam_inspectionDict']['passPerc'] = 100 * context_dic['neckDiam_inspectionDict'][
    #             'numPass'] / context_dic['neckDiam_inspectionDict']['totalInspections']
    #     else:
    #         context_dic['neckDiam_inspectionDict']['passPerc'] = 0

    # if inspectionTypes.assembly_test_inspection:
    #     context_dic['assembly_inspection'] = assemblyInspection.objects.filter(jobID__jobNumber=self.jobNumber,
    #                                                                            dateCreated__range=(self.dateFrom, self.dateTo))
    # if inspectionTypes.carton_temp_inspection:
    #     context_dic['cartonTemp_inspection'] = cartonTemperature.objects.filter(jobID__jobNumber=self.jobNumber,
    #                                                                             dateCreated__range=(self.dateFrom, self.dateTo))
    #     context_dic['cartonTemp_inspectionDict'] = {}
    #     context_dic['cartonTemp_inspectionDict'] = context_dic['cartonTemp_inspection'].aggregate(
    #         Avg('cartonTemp'),
    #         Max('cartonTemp'),
    #         Min('cartonTemp'),
    #         StdDev('cartonTemp'))

    # if inspectionTypes.vision_system_inspection:
    #     context_dic['visionSys_inspection'] = visionInspection.objects.filter(jobID__jobNumber=self.jobNumber,
    #                                                                           dateCreated__range=(self.dateFrom, self.dateTo))

    #
    # return context_dic
