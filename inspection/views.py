# Create your views here.
import collections
import datetime
import json
import numpy as np
import re
from decimal import Decimal
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Avg, Max, Min, StdDev
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import RequestContext, loader
from django.utils import timezone

from dashboard.models import errorLog
from employee.models import Employees, EmployeeAtWorkstation
from equipment.models import EquipmentInfo
from forms import NumericInspectionFormVF
from forms import jobReportSearch, itemReportSearch, \
    build_inspection_fields, PassFailIns, NumericInspectionForm, TextIns,\
    RangeInspectionForm, RangeInspectionFormVF, PassFailInspectionForm, TextInspectionForm
from models import *
from molds.models import Mold, PartIdentifier
from part.models import Part
from production_and_mold_history.models import ProductionHistory
from reports import JobReport
from startupshot.models import startUpShot, MattecProd


######################################
#
#  Section for generating indexes, etc
#
######################################


@login_required
def view_index(request):
    activeInMattec = MattecProd.objects.order_by('machNo').all()

    template = loader.get_template('inspection/index.html')
    context = RequestContext(request, {
        'active_parts': activeInMattec,
    })
    return HttpResponse(template.render(context))


@login_required
def view_job_detail(request):
    job_number = str(request.GET.get('job_number', -1)).strip()
    machine_number = str(request.GET.get('machine_number',-1)).strip()

    machine = EquipmentInfo.objects.get(part_identifier=machine_number)


    part_in_mattec = MattecProd.objects.get(jobNumber=job_number,
                                    machNo=machine_number)

    active_job = startUpShot.objects.filter(jobNumber=job_number,
                                            machNo=machine).last()
#
    if not active_job:
        redirect_url = '{0}?job_number={1}&machine_number={2}'.format(
            reverse('start_up_shot_create_new'), job_number, machine_number)
        return HttpResponseRedirect(redirect_url)

    item_number_id = active_job.item_id


    if machine_number in ['FAS01', 'OFP01'] or active_job:
        if machine_number not in ['FAS01', 'OFP01']:
            checkPartInspection(active_job.item)
        if not active_job and machine_number in ['FAS01', 'OFP01']:

            active_job = startUpShot(item_id=item_number_id,
                                     jobNumber=job_number,
                                     moldNumber_id=Mold.objects.get(mold_number=part_in_mattec.moldNumber).id,
                                     activeCavities=part_in_mattec.activeCavities,
                                     machNo_id=machine.id,
                                     machineOperator_id=0,
                                     inspectorName_id=0,
                                     shotWeight=-1,
                                     cycleTime=-1).save()


        pass_fail_inspection = passFailByPart.objects.filter(item_Number_id=item_number_id,
                                                          testName__isSystemInspection=False)
        numeric_inspection = numericTestByPart.objects.filter(item_Number_id=item_number_id,
                                                                testName__isSystemInspection=False)
        text_inspection = textRecordByPart.objects.filter(item_Number_id=item_number_id,
                                                              testName__isSystemInspection=False)
        # int_inspectionType = IntegerRecordByPart.objects.filter(item_Number_id=item_number_id,
        #                                                         testName__isSystemInspection=False)
        range_inspection = RangeRecordByPart.objects.filter(item_Number_id=item_number_id,
                                                                testName__isSystemInspection=False)
        template = loader.get_template('inspection/detail_job.html')
        context = RequestContext(request, {
            'active_job': active_job,
            'pf_inspectionType': pass_fail_inspection,
            'numeric_inspectionType': numeric_inspection,
            'text_inspectionType': text_inspection,
            # 'int_inspectionType': int_inspectionType,
            'range_inspectionType': range_inspection
        })
        return HttpResponse(template.render(context))
    else:
        redirect_url = '{0}?job_number={1}&machine_number={2}'.format(
            reverse('start_up_shot_create_new'), job_number, machine_number)
        return HttpResponseRedirect(redirect_url)


######################################
#
#  Section for generating forms
#
######################################

@login_required
def view_inspection(request):
    job_number_id = int(request.GET.get('job_number_id', -1))
    inspection_type = request.GET.get('inspection_type', 'N/A')
    inspection_name_id = int(request.GET.get('inspection_name_id', -1))

    head_cav_id_choices, defect_type_choices = build_inspection_fields(job_id=job_number_id,
                                                                       inspection_type=inspection_type,
                                                                       inspection_id=inspection_name_id,
                                                                       man_num=request.user.webappemployee.EmpNum)

    head_cav_ids = [id for id, label in head_cav_id_choices]

    if request.method == 'POST':

        # try:
        active_job = startUpShot.objects.filter(id=job_number_id).last()
        context_dict = {'active_job': active_job,
                        'head_cav_id': '#id_headCavID'}
        range_info = None

        if inspection_type == 'Pass-Fail':
            test_info = passFailTest.objects.get(id=inspection_name_id)
            form = PassFailInspectionForm(request.POST or None,
                                          extra=head_cav_ids,
                                          defect_type_choices=defect_type_choices)

        elif inspection_type == 'Numeric':
            test_info = numericTest.objects.get(id=inspection_name_id)
            range_info = numericTestByPart.objects.get(testName_id=inspection_name_id,
                                                       item_Number_id=active_job.item_id)

            form = NumericInspectionFormVF(request.POST or None, extra=head_cav_ids)

        elif inspection_type == 'Text':
            test_info = textRecord.objects.get(id=inspection_name_id)
            form = TextInspectionForm(request.POST or None, extra=head_cav_ids)


        elif inspection_type == 'Range':
            test_info = RangeRecord.objects.get(id=inspection_name_id)
            range_info = RangeRecordByPart.objects.get(testName_id=inspection_name_id,
                                                       item_Number_id=active_job.item_id)

            form = RangeInspectionFormVF(request.POST or None, extra=head_cav_ids)

        else:
            raise Http404("Inspection Type Does Not Exist")

        if form.is_valid():
            bulk_save_list = []

            is_user = get_user_info(request.user.webappemployee.EmpNum)
            active_machine_operator = None
            if is_user:
                    # my_form.Passed_Partial = False
                my_form = form


                if inspection_type == 'Pass-Fail':
                    timestamp_form_recieved = datetime.datetime.now()

                    bulk_save_list = []
                    for each_cav, measurement in my_form.extra_answers():

                        new_form = passFailInspection(
                            passFailTestName_id=test_info.id,
                            jobID_id=job_number_id,
                            machineOperator_id=my_form.cleaned_data[
                                'machine_operator'],
                            inspectorName_id=is_user.id,
                            dateCreated=timestamp_form_recieved,
                            headCavID=each_cav
                        )

                        if measurement:
                            if each_cav == 'Full Shot':
                                each_cav = '-'



                            new_form.inspectionResult = False
                            new_form.save()

                            pass_fail_test_critereon = passFailTestCriteria.objects.filter(
                                id__in = measurement
                            )

                            error_objects = []
                            for each_measurement in pass_fail_test_critereon:
                                new_form.defectType.add(each_measurement)

                        else:
                            new_form.inspectionResult = True
                            bulk_save_list.append(new_form)

                    if bulk_save_list:
                        passFailInspection.objects.bulk_create(bulk_save_list)
                    active_machine_operator = new_form.machineOperator

                elif inspection_type == 'Numeric':
                    #my_form.numericTestName_id = range_info.id
                    timestamp_form_recieved = datetime.datetime.now()
                    bulk_save_list = []

                    for each_cav, measurement in my_form.extra_answers():
                        if measurement:
                            if ((measurement >= range_info.rangeMin) and (measurement <= range_info.rangeMax)):
                                inspectionResult = True
                            else:
                                inspectionResult = False

                            if each_cav == 'Full Shot':
                                each_cav = '-'



                            bulk_save_list.append(numericInspection(
                                numericTestName_id = range_info.id,
                                jobID_id = job_number_id,
                                machineOperator_id = my_form.cleaned_data['machine_operator'],
                                inspectorName_id = is_user.id,
                                dateCreated = timestamp_form_recieved,
                                isFullShot = my_form.cleaned_data['is_full_shot'],
                                numVal_1 = measurement,
                                inspectionResult = inspectionResult,
                                headCavID = each_cav,
                            ))

                    if bulk_save_list:
                        numericInspection.objects.bulk_create(bulk_save_list)
                        active_machine_operator = bulk_save_list[-1].machineOperator

                elif inspection_type == 'Text':
                    timestamp_form_recieved = datetime.datetime.now()
                    bulk_save_list = []

                    for each_cav, measurement in my_form.extra_answers():
                        if measurement:
                            if not re.search('cav_', each_cav):
                                each_cav = '-'

                            bulk_save_list.append(textInspection(
                                textTestName_id=test_info.id,
                                jobID_id=job_number_id,
                                machineOperator_id=my_form.cleaned_data[
                                    'machine_operator'],
                                inspectorName_id=is_user.id,
                                dateCreated=timestamp_form_recieved,
                                isFullShot=my_form.cleaned_data['is_full_shot'],
                                inspectionResult=measurement,
                                headCavID=each_cav,
                            ))

                    if bulk_save_list:
                        textInspection.objects.bulk_create(bulk_save_list)
                        active_machine_operator = bulk_save_list[
                            -1].machineOperator


                elif inspection_type == 'Integer':
                    my_form.integerTestName_id = inspection_name_id

                elif inspection_type == 'Range':
                    '''
                    Need:
                        1. Range record id
                        2. job_id
                        3. Machine operator (from form)
                        4. Inspector name (from is_user.id)
                        5. dateCreated = timestamp_form_recieved
                        6. is_full_shot (from my_form.cleaned_data['is_full_shot']
                        7. numVal_1
                        8. numVal_2
                        9. headCavID (each_cav)
                    '''


                    timestamp_form_recieved = datetime.datetime.now()
                    bulk_save_list = []


                    entry_dict = {}
                    cav_ids = []
                    for each_cav, measurement in my_form.extra_answers():
                        '''
                        Need to sort form answer and retrieve pairs
                        Dictionary:
                            key: cav_id
                            value: dictionary
                                {
                                low_measurement: measurement
                                high_measurement: measurement
                                }
                        '''
                        cav_id = each_cav.rstrip(' Low').rstrip(' High')

                        if cav_id not in entry_dict:
                            entry_dict[cav_id] = {
                                'low_measurement': None,
                                'high_measurement': None
                            }

                        if ' Low' in each_cav:
                            key = 'low_measurement'
                        elif ' High' in each_cav:
                            key = 'high_measurement'
                        else:
                            continue

                        entry_dict[cav_id].update({
                            key: measurement
                        })

                        cav_ids.append(cav_id)

                    cav_ids.sort()
                    entry_dict_sort = collections.OrderedDict()

                    for each_cav_id in cav_ids:
                        entry_dict_sort.update({each_cav_id: entry_dict[each_cav_id]})

                    for each_cav, measurement_dict in entry_dict_sort.iteritems():

                        if ((measurement_dict['low_measurement'] >= range_info.rangeMin) and (
                                    measurement_dict['high_measurement'] <= range_info.rangeMax)):
                            inspectionResult = True
                        else:
                            inspectionResult = False

                        if each_cav == 'Full Shot':
                            each_cav = '-'

                        if measurement:
                            bulk_save_list.append(RangeInspection(
                                rangeTestName_id=range_info.testName_id,
                                jobID_id=job_number_id,
                                machineOperator_id=my_form.cleaned_data[
                                    'machine_operator'],
                                inspectorName_id=is_user.id,
                                dateCreated=timestamp_form_recieved,
                                isFullShot=my_form.cleaned_data['is_full_shot'],
                                numVal_1=measurement_dict['low_measurement'],
                                numVal_2=measurement_dict['high_measurement'],
                                inspectionResult=inspectionResult,
                                headCavID=each_cav,
                            ))

                    if bulk_save_list:
                        RangeInspection.objects.bulk_create(bulk_save_list)
                        active_machine_operator = bulk_save_list[
                            -1].machineOperator



                else:
                    pass

                set_new_mach_op(active_job.jobNumber, active_machine_operator)
                # checkFormForLog(my_form, inspectionType=inspection_type,
                #                 inspectionName=test_info.testName,
                #                 activeJob=active_job, rangeInfo=range_info)
                # "{% url 'inspection_view_job_machine' %}?job_number={{each_part.jobNumber.strip}}&machine_number={{each_part.machNo.strip}}"
                redirect_url = "{0}?job_number={1}&machine_number={2}".format(
                    reverse('inspection_view_job_machine'),
                    active_job.jobNumber,
                    active_job.machNo.part_identifier)
                return HttpResponseRedirect(redirect_url)
            else:
                template = loader.get_template('inspection/bad_user.html')
                context = RequestContext(request)
                return HttpResponse(template.render(context))
        else:

            return Http404()

                # except Exception as e:
                #     raise Http404(str(e))

    else:

        active_job = startUpShot.objects.filter(id=job_number_id).last()
        context_dict = {'active_job': active_job,
                        'head_cav_id': '#id_headCavID'}

        if inspection_type == 'Pass-Fail':
            test_info = passFailTest.objects.get(id=inspection_name_id)
            form = PassFailInspectionForm(extra=head_cav_ids,
                                          defect_type_choices=defect_type_choices)
            context_dict_add = {
                'use_checkbox2': True,
                'id_check': '#id_inspectionResult',
                'idSelect': '#id_defectType',
                'idSelect2': '#id_headCavID',
            }

        elif inspection_type == 'Numeric':
            test_info = numericTest.objects.get(id=inspection_name_id)
            range_info = numericTestByPart.objects.get(testName_id=inspection_name_id,
                                                       item_Number_id=active_job.item_id)

            form = NumericInspectionFormVF(extra=head_cav_ids)

            context_dict_add = {
                'use_checkbox': True,
                'id_check': '#id_isFullShot',
                'idSelect': '#id_headCavID',
                'use_minmax': True,
                'num_id': '#id_numVal_1',
                'min_val': range_info.rangeMin,
                'max_val': range_info.rangeMax,
                'id_result': '#id_inspectionResult',
                'use_calculator': True if len(head_cav_ids) == 1 else False,
                'id_numeric' : 'id_cav_0',
                'active_cavities': active_job.activeCavities
            }

        elif inspection_type == 'Text':
            test_info = textRecord.objects.get(id=inspection_name_id)
            form = TextInspectionForm(extra=head_cav_ids)
            context_dict_add = {
                'use_checkbox': True,
                'id_check': '#id_inspectionResult',
                'idSelect': '#id_headCavID',
            }

        elif inspection_type == 'Range':
            test_info = RangeRecord.objects.get(id=inspection_name_id)
            form = RangeInspectionFormVF(extra=head_cav_ids)

            context_dict_add = {
                'use_checkbox': True,
                'id_check': '#id_isFullShot',
                'idSelect': '#id_headCavID'
            }

        else:
            raise Http404("Inspection Type Does Not Exist")

        machine_operator = get_previous_mach_op(job_number=active_job.jobNumber)
        if machine_operator:
            context_dict.update({'machine_operator': machine_operator.id})

        machine_operator_choices = []
        for each_employee in Employees.objects.filter(StatusActive=True, IsOpStaff=True).order_by('EmpShift').order_by(
                'EmpLName'):
            machine_operator_choices.append((each_employee.id,
                                             each_employee.__unicode__()))
        if not machine_operator_choices:
            machine_operator_choices = [(-1,'Error')]

        choice_field_dict = {'widget': forms.Select(),
                             'choices': machine_operator_choices}

        if machine_operator:
            choice_field_dict.update({'initial': machine_operator.id})

        form.fields['machine_operator'] = forms.ChoiceField(**choice_field_dict)

        context_dict.update({'form_title': test_info.testName,
                             'form': form})
        context_dict.update(context_dict_add)

        template = loader.get_template('inspection/forms/genInspection.html')
        context = RequestContext(request, context_dict)
        return HttpResponse(template.render(context))



######################################
#
#  Section for generating reports
#
######################################


@login_required
def job_report_search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = jobReportSearch(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            report_type = form.cleaned_data['report_type']
            job_number = form.cleaned_data['job_Number']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']

            this_start_up_shot = startUpShot.objects.filter(jobNumber=job_number)
            workstation = this_start_up_shot[0].machNo

            if report_type == 'htmlReport':
                context_dic = createJobReportDict(job_number, date_from=date_from, date_to=date_to)
                redirect_url = '{0}?job_number={1}&workstation={2}'.\
                                   format(reverse('job_report_base'), job_number, workstation)
                return HttpResponseRedirect(redirect_url)
            else:
                if startUpShot.objects.filter(jobNumber=job_number).exists():
                    my_report = JobReport(job_number=job_number, date_from=date_from, date_to=date_to)
                    return my_report.get_report()
                else:
                    return render(request, '404.html')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = jobReportSearch()

    return render(request, 'inspection/searchForms/jobReportSearch.html', {'form': form})


@login_required
def view_itemReportSearch(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = itemReportSearch(request.POST)
        # check whether it's valid:
        if form.is_valid():
            item_number = form.cleaned_data['item_Number']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            context_dic = {}
            context_dic['partDict'] = createItemReportDict(item_number, date_from=date_from, date_to=date_to)
            context_dic.update({'list_many': True})

            template = loader.get_template('inspection/reports/partReport.html')
            context = RequestContext(request, context_dic)
            return HttpResponse(template.render(context))


    # if a GET (or any other method) we'll create a blank form
    else:
        form = itemReportSearch()

    return render(request, 'inspection/searchForms/itemReportSearch.html', {'form': form})


@login_required
def view_itemReport(request, itemNumber):
    context_dict = {}
    context_dict = createItemReportDict(itemNumber)
    context_dict.update({'list_many': True})

    template = loader.get_template('inspection/reports/partReport.html')
    context = RequestContext(request, context_dict)
    return HttpResponse(template.render(context))


@login_required
def view_jobReport(request, jobNumber):
    context_dic = createJobReportDict(jobNumber)
    template = loader.get_template('inspection/reports/jobReport.html')
    context = RequestContext(request, context_dic)
    return HttpResponse(template.render(context))


@login_required
def view_jobReport_pdf(request, jobNumber):
    if startUpShot.objects.filter(jobNumber=jobNumber).exists():
        my_report = JobReport(job_number=jobNumber)
        return my_report.get_report()
    else:
        return render(request, '404.html')


####### Section for generating data for plots ###########
def view_jsonError(job_number, date_from, date_to):
    date_from, date_to = createDateRange(date_from, date_to)
    pf = passFailInspection.objects.filter(jobID__jobNumber=job_number,
                                           dateCreated__range=(date_from, date_to),
                                           inspectionResult=0)
    ni = numericInspection.objects.filter(jobID__jobNumber=job_number,
                                          dateCreated__range=(date_from, date_to),
                                          inspectionResult=0)
    ti = textInspection.objects.filter(jobID__jobNumber=job_number,
                                       dateCreated__range=(date_from, date_to),
                                       inspectionResult=0)

    if (not ni.exists()) and (not pf.exists()):
        no_errors = True
    else:
        no_errors = False

    production_errors = []
    for eachpf in pf:
        production_errors.append(eachpf.passFailTestName.testName)
    for eachni in ni:
        production_errors.append(eachni.numericTestName.testName.testName)
    for eachti in ti:
        production_errors.append(eachti.textTestName.testName)

    count_errors = collections.Counter(production_errors)
    sort_jawn = [(l, k) for k, l in sorted([(j, i) for i, j in count_errors.items()], reverse=True)]
    counted_errors = []
    for k, v in sort_jawn:
        counted_errors.append({'error_name': k, 'error_count': v})

    if no_errors:
        return None
    else:
        return json.dumps(counted_errors, ensure_ascii=False).encode('utf8')


####### Helper functions ###########

def createItemReportDict(itemNumber, date_from=None, date_to=None):
    collapse_list = []

    date_from1, date_to1 = createDateRange(date_from=date_from, date_to=date_to)

    jobList = startUpShot.objects.filter(item__item_Number=itemNumber, dateCreated__range=(date_from1, date_to1))
    job_id_keys = [each_job.id for each_job in jobList]
    item_number_id = jobList[0].item_id



    susList = jobList
    jobList = jobList.values_list('jobNumber', flat=True)

    job_id_num = zip(job_id_keys, jobList)

    pf_inspectionType = passFailByPart.objects.filter(item_Number_id=item_number_id)
    numericTests = numericTestByPart.objects.filter(item_Number_id=item_number_id)
    textTests = textRecordByPart.objects.filter(item_Number_id=item_number_id)

    partDict = {'pf': {}, 'numericTest': {}, 'activeJob': susList, 'range_test': collections.OrderedDict()}

    k = 0
    for eachInspection1 in pf_inspectionType:
        eachInspection = eachInspection1.testName
        partDict['pf'][eachInspection] = collections.OrderedDict()
        thisInspection = passFailInspection.objects.filter(passFailTestName_id=eachInspection1.testName_id,
                                                           dateCreated__range=(date_from1, date_to1))
        n = 0

        key = 'pf' + str(k)
        collapse_list.append('#' + key)
        partDict['pf'][eachInspection]['html_id'] = key
        k = k + 1

        for job_id, job_num in job_id_num:
            partDict['pf'][eachInspection]['inspectionName'] = eachInspection
            partDict['pf'][eachInspection][n] = {}
            thisInspectionbyJob = thisInspection.filter(jobID_id=job_id).order_by('-dateCreated','headCavID')
            partDict['pf'][eachInspection][n]['jobID'] = job_num
            partDict['pf'][eachInspection][n].update(createPFStats(thisInspectionbyJob))
            n += 1

        partDict['pf'][eachInspection][n] = {}
        partDict['pf'][eachInspection][n]['jobID'] = 'Total'
        partDict['pf'][eachInspection][n].update(
            createPFStats(thisInspection.filter(jobID__in=job_id_keys)))

    k = 0
    for eachInspection1 in numericTests:

        eachInspection = eachInspection1.testName.testName
        partDict['numericTest'][eachInspection] = collections.OrderedDict()
        partDict['numericTest'][eachInspection]['inspectionName'] = eachInspection

        thisInspection = numericInspection.objects.filter(numericTestName_id=eachInspection1.id,
                                                          dateCreated__range=(date_from1, date_to1)).order_by(
            '-dateCreated')
        n = 0

        key = 'nt' + str(k)
        collapse_list.append('#' + key)
        partDict['numericTest'][eachInspection]['html_id'] = key
        k = k + 1

        totalNumericList = []
        for job_id, job_num in job_id_num:
            partDict['numericTest'][eachInspection][n] = {}
            partDict['numericTest'][eachInspection][n]['jobID'] = job_num

            thisInspectionbyJob = thisInspection.filter(jobID_id=job_id).order_by('-dateCreated','headCavID')
            active_job = startUpShot.objects.filter(id=job_id).select_related('item')

            numericList = []
            for eachShot in thisInspectionbyJob:
                numericList.append(eachShot.numVal_1)
                totalNumericList.append(numericList[-1])

            partDict['numericTest'][eachInspection][n]['numericStats'] = calc_numeric_stats(numericList)
            n += 1

        partDict['numericTest'][eachInspection][n] = {'jobID': 'Total',
                                                    'numericStats': calc_numeric_stats(totalNumericList)}



    for k, each_range_test in enumerate(RangeRecordByPart.objects.filter(item_Number_id=item_number_id)):
        test_name = each_range_test.testName.testName
        partDict['range_test'][test_name] = collections.OrderedDict()
        partDict['range_test'][test_name]['inspectionName']=test_name

        this_inspection = RangeInspection.objects.filter(rangeTestName_id=each_range_test.id,
                                                         dateCreated__range=(date_from1, date_to1)).order_by('-dateCreated','headCavID')

        key = 'rt' + str(k)
        collapse_list.append('#' + key)
        partDict['range_test'][test_name]['html_id'] = key

        total_range_list = []
        for n, (job_id, job_num) in enumerate(job_id_num):
            partDict['range_test'][test_name][n] = {
                'jobID' : job_num
            }
            partDict['range_test'][test_name][n].update(createPFStats(this_inspection.filter(jobID_id=job_id).order_by('-dateCreated','headCavID')))

        partDict['range_test'][test_name][n] = {}
        partDict['range_test'][test_name][n]['jobID'] = 'Total'
        partDict['range_test'][test_name][n].update(
        createPFStats(this_inspection.filter(jobID__in=job_id_keys)))

    n = 0
    partDict['textTests'] = collections.OrderedDict()
    for eachTextTest in textTests:
        key = 'tt' + str(n)
        collapse_list.append('#' + key)
        partDict['textTests'][n] = {
            'html_id': key,
            'testName': eachTextTest.testName,
            'textDict': textInspection.objects.filter( \
                    textTestName_id=eachTextTest.testName_id,
                    jobID__in=job_id_keys)
        }

        n += 1

    partDict['phl'] = ProductionHistory.objects.filter(id__in=job_id_keys).values('dateCreated', 'jobNumber',
                                                                                        'inspectorName__EmpLMName',
                                                                                        'descEvent').order_by('-dateCreated')

    # partDict['phl'] = [item for sublist in partDict['phl'] for item in sublist]  # change?
    partDict['useJobNo'] = True

    collapse_list.append('#phl')

    partDict.update({'collapse_list': collapse_list})

    partDict.update({
        'headerDict': {
            'companyName': 'Custom Molders Group',
            'reportName': 'Part Report',
            'documentName': 'Part Number: %s' % itemNumber
        },
        'list_many': True
    })

    return partDict


def createJobReportDict(jobNumber, date_from=None, date_to=None):
    collapse_list = []
    context_dic = {}
    context_dic['plot_info'] = view_jsonError(job_number=jobNumber, date_from=date_from, date_to=date_to)

    date_from, date_to = createDateRange(date_from=date_from, date_to=date_to)

    active_job = startUpShot.objects.filter(jobNumber=jobNumber).select_related('item')

    job_id_keys = [each_job.id for each_job in active_job]

    context_dic['active_job'] = active_job

    # Job number 6 and 9 should be QA and
    context_dic['phl'] = ProductionHistory.objects.filter(jobNumber=jobNumber,
                                                          dateCreated__range=(date_from, date_to),
                                                          inspectorName__IsQCStaff=True).values('dateCreated',
                                                                                                'jobNumber',
                                                                                                'inspectorName__EmpLMName',
                                                                                                'descEvent').order_by(
        '-dateCreated')

    pf_inspectionType = passFailByPart.objects.filter(item_Number_id=active_job[0].item_id)
    numericTests = numericTestByPart.objects.filter(item_Number_id=active_job[0].item_id)
    textTests = textRecordByPart.objects.filter(item_Number_id=active_job[0].item_id)

    context_dic['pf'] = {}
    context_dic['pfSummary'] = {}
    n = 0
    for each_pf_inspection in pf_inspectionType:
        key = 'pf' + str(n)
        collapse_list.append('#' + key)
        context_dic['pf'][key] = passFailInspection.objects.filter(
            passFailTestName_id=each_pf_inspection.testName_id,
            jobID__in=job_id_keys,
            dateCreated__range=(date_from, date_to)).order_by('-dateCreated')
        context_dic['pfSummary'][key] = {}

        if each_pf_inspection.testName.report_name:
            r_name = each_pf_inspection.testName.report_name
        else:
            r_name = each_pf_inspection.testName.testName

        context_dic['pfSummary'][key]['pfName'] = r_name
        context_dic['pfSummary'][key].update(createPFStats(context_dic['pf'][key]))
        n += 1


    context_dic.update({'range_tests':{}, 'range_summary':{}})
    for n, each_range_test in enumerate(RangeRecordByPart.objects.filter(item_Number_id=active_job[0].item_id)):
        key = 'range' + str(n)
        collapse_list.append('#'+key)
        context_dic['range_tests'][key] = RangeInspection.objects.filter(
            rangeTestName_id= each_range_test.testName_id,
            jobID__in=job_id_keys,
            dateCreated__range=(date_from, date_to)).order_by('-dateCreated')

        if each_range_test.testName.report_name:
            r_name = each_range_test.testName.report_name
        else:
            r_name = each_range_test.testName.testName

        context_dic['range_summary'][key] = {
            'range_test_name': r_name
        }
        context_dic['range_summary'][key].update(createPFStats(context_dic['range_tests'][key]))

    n = 0
    context_dic['numericTests'] = {}
    context_dic['numericTestSummary'] = {}
    for each_numeric_inspection in numericTests:
        key = 'rt' + str(n)
        collapse_list.append('#' + key)
        context_dic['numericTests'][key] = numericInspection.objects.filter(
            numericTestName_id=each_numeric_inspection.id,
            jobID__in=job_id_keys,
            dateCreated__range=(date_from, date_to)).order_by('-dateCreated')
        context_dic['numericTestSummary'][key] = {}

        if each_numeric_inspection.testName.report_name:
            r_name = each_numeric_inspection.testName.report_name
        else:
            r_name = each_numeric_inspection.testName.testName

        context_dic['numericTestSummary'][key]['numericName'] = r_name

        numericList = []
        for eachShot in context_dic['numericTests'][key]:
            numericList.append(eachShot.numVal_1)

        context_dic['numericTestSummary'][key]['numericStats'] = calc_numeric_stats(numericList)

        n += 1

    n = 0
    context_dic['textTests'] = {}
    for eachTextTest in textTests:
        key = 'tt' + str(n)
        collapse_list.append('#' + key)

        if eachTextTest.testName.report_name:
            r_name = eachTextTest.testName.report_name
        else:
            r_name = eachTextTest.testName.testName

        context_dic['textTests'][key] = {
            'testName': r_name,
            'textDict': textInspection.objects.filter( \
                    textTestName_id=eachTextTest.testName_id, jobID__in=job_id_keys).order_by('-dateCreated')
        }

        n += 1

    context_dic['phl'] = ProductionHistory.objects.filter(jobNumber=jobNumber).values('dateCreated', 'jobNumber',
                                                                                      'inspectorName__EmpLMName',
                                                                                      'descEvent').order_by(
        '-dateCreated')
    collapse_list.append('#' + 'phl')

    context_dic.update({
        'headerDict': {
            'companyName': 'Custom Molders Group',
            'reportName': 'Job Report',
            'documentName': 'Job Number: %s' % (jobNumber)
        },
        'list_many': True
    })

    context_dic.update({'collapse_list': collapse_list})
    return context_dic


######################
#
# Helper functions
#
######################

def createDateRange(date_from=None, date_to=None):
    if date_from is None:
        date_from = datetime.datetime.strptime('1900-01-01', '%Y-%m-%d')
        date_from = timezone.make_aware(date_from, timezone.get_current_timezone())

    if date_to is None:
        date_to = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        date_to = timezone.make_aware(date_to, timezone.get_current_timezone())

    return (date_from, date_to)


def presetStandardFields(my_form, jobID, test_type, test_name):
    # this will preset machine and qa fields
    ### Filter the machine operators
    my_form.fields["machineOperator"].queryset = Employees.objects.filter(StatusActive=True,
                                                                          IsOpStaff=True).order_by('EmpShift').order_by(
        'EmpLName')

    my_form.fields["jobID"].queryset = startUpShot.objects.filter(jobNumber=jobID)

    #
    # if test_type == 'pf':
    #     my_form.fields["defectType"].queryset = passFailTestCriteria.objects.filter(testName__testName=test_name)

    return my_form


def getShift():
    currentHour = datetime.datetime.time(datetime.datetime.now()).hour

    if (currentHour >= 7) and (currentHour < 15):
        shift = 1
    elif (currentHour >= 15) and (currentHour < 23):
        shift = 2
    else:
        shift = 3

    return shift


def checkPartInspection(item_Number):
    for requiredTests in passFailTest.objects.filter(requireAll=True):
        if not passFailByPart.objects.filter(item_Number__item_Number=item_Number,
                                             testName__testName=requiredTests.testName).exists():
            newPartInspection = passFailByPart(item_Number=Part.objects.get(item_Number=item_Number),
                                               testName=requiredTests)
            newPartInspection.save()

    for requiredTests in numericTest.objects.filter(requireAll=True):
        if not numericTestByPart.objects.filter(item_Number__item_Number=item_Number,
                                                testName__testName=requiredTests.testName).exists():
            try:
                exp_part_weight = Part.objects.get(item_Number=item_Number).exp_part_weight
                low_exp = Decimal(exp_part_weight * 0.95)
                high_exp = Decimal(exp_part_weight * 1.05)
                newPartInspection = numericTestByPart(item_Number=Part.objects.get(item_Number=item_Number),
                                                      testName=requiredTests,
                                                      rangeMin=low_exp,
                                                      rangeMax=high_exp)
            except Exception as e:
                newPartInspection = numericTestByPart(item_Number=Part.objects.get(item_Number=item_Number),
                                                      testName=requiredTests,
                                                      rangeMin=0,
                                                      rangeMax=999999)
            newPartInspection.save()

    for requiredTests in textRecord.objects.filter(requireAll=True):
        if not textRecordByPart.objects.filter(item_Number__item_Number=item_Number,
                                               testName__testName=requiredTests.testName).exists():
            newPartInspection = textRecordByPart(testName=requiredTests,
                                                 item_Number=Part.objects.get(item_Number=item_Number))
            newPartInspection.save()

    # for requiredTests in IntegerRecord.objects.filter(requireAll=True):
    #     if not IntegerRecordByPart.objects.filter(item_Number__item_Number=item_Number,
    #                                               testName__testName=requiredTests.testName).exists():
    #         newPartInspection = IntegerRecordByPart(testName=requiredTests,
    #                                                 item_Number=Part.objects.get(item_Number=item_Number))
    #         newPartInspection.save()

    for requiredTests in RangeRecord.objects.filter(requireAll=True):
        if not RangeRecordByPart.objects.filter(item_Number__item_Number=item_Number,
                                                testName__testName=requiredTests.testName).exists():
            newPartInspection = RangeRecordByPart(testName=requiredTests,
                                                  item_Number=Part.objects.get(item_Number=item_Number))
            newPartInspection.save()

            # Will probably need to create something for shot weights...


def checkFormForLog(form, inspectionType, inspectionName, activeJob, rangeInfo=None):
    create_log = False
    errorDescription = 'None'

    shiftID = getShift()
    jobID = activeJob.jobNumber
    machNo = activeJob.machNo.part_identifier
    partDesc = activeJob.item.item_Description
    inspectionName = inspectionName

    if inspectionType == 'Pass-Fail':
        if not form.inspectionResult:
            errorDescription = form.defectType.all()
            error_list = []
            for each_error in errorDescription:
                newForm = errorLog(
                        shiftID=shiftID,
                        machNo=machNo,
                        partDesc=partDesc,
                        jobID=jobID,
                        inspectionName=inspectionName,
                        errorDescription=each_error.passFail,
                )
                newForm.save()

    if inspectionType == 'Numeric':
        measured_val = form.numVal_1

        if measured_val < rangeInfo.rangeMin:
            errorDescription = 'Measured value is %1.3f which is less than tolerance (%1.3f)' % (
            measured_val, rangeInfo.rangeMin)
            create_log = True
        if measured_val > rangeInfo.rangeMax:
            errorDescription = 'Measured value is %1.3f which is greater than tolerance (%1.3f)' % (
            measured_val, rangeInfo.rangeMax)
            create_log = True

    if inspectionType == 'Text':
        if not form.inspectionResult:
            errorDescription = '%s' % form.inspectionResult
            create_log = True

    if inspectionType == 'Integer':
        if not form.inspectionResult:
            errorDescription = '%s' % form.inspectionResult
            create_log = True

    if inspectionType == 'Float':
        if not form.inspectionResult:
            errorDescription = '%s' % form.inspectionResult
            create_log = True

    if create_log:
        newForm = errorLog(
                shiftID=shiftID,
                machNo=machNo,
                partDesc=partDesc,
                jobID=jobID,
                inspectionName=inspectionName,
                errorDescription=errorDescription,
        )
        newForm.save()


def createPFStats(qSet):
    resultDict = {
        'numPass': qSet.filter(inspectionResult=1).count(),
        'numFail': qSet.filter(inspectionResult=0).count()}
    resultDict['totalInspections'] = resultDict['numPass'] + resultDict['numFail']
    if resultDict['totalInspections'] > 0:
        resultDict['passPerc'] = 100 * resultDict['numPass'] / resultDict['totalInspections']
    else:
        resultDict['passPerc'] = 0

    return resultDict


def calc_numeric_stats(numericList):
    if numericList:
        resultDict = {
            'numericList__count': '%i' % (len(numericList)),
            'numericList__min': '%1.3f' % (np.amin(numericList)),
            'numericList__max': '%1.3f' % (np.amax(numericList)),
            'numericList__avg': '%1.3f' % (np.mean(numericList)),
            'numericList__stddev': '%1.3f' % (np.std(numericList))
        }
    else:
        resultDict = {
            'numericList__count': '%i' % (0),
            'numericList__min': '%1.3f' % (0),
            'numericList__max': '%1.3f' % (0),
            'numericList__avg': '%1.3f' % (0),
            'numericList__stddev': '%1.3f' % (0)
        }
    return resultDict


def check_HeadCavID(cav_str):
    cav_str.strip(' ')
    cav_str.lower()
    re_pattern = '[a-zA-Z]\s*-\s*\d{1,3}|[a-zA-Z]\s*-\s*all|\d{1,3}|all|none'
    possible_match = re.search(re_pattern, cav_str)
    if possible_match:
        return possible_match.group(0)
    else:
        return None


def get_user_info(man_num):
    try:
        this_user = Employees.objects.get(EmpNum=man_num)
    except Employees.DoesNotExist:
        this_user = None
    return this_user


def get_previous_mach_op(job_number):
    try:
        mattec_info = MattecProd.objects.get(jobNumber=job_number)
        this_machine_operator = EmployeeAtWorkstation.objects.get(workstation=mattec_info.machNo)
        employee_info = this_machine_operator.employee
    except Exception as e:
        employee_info = None
    return employee_info


def set_new_mach_op(job_number, employee_info):
    try:
        mattec_info = MattecProd.objects.get(jobNumber=job_number)
        current_station = EmployeeAtWorkstation.objects.get(workstation=mattec_info.machNo)
        current_station.employee = employee_info
        current_station.save()
    except EmployeeAtWorkstation.DoesNotExist:
        mattec_info = MattecProd.objects.get(jobNumber=job_number)
        EmployeeAtWorkstation(workstation=mattec_info.machNo, employee=employee_info).save()
    except Exception as e:
        pass
