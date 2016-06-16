# from __future__ import unicode_literals
#
# from django.db import models
# import uuid
#
# class Inspection(models.Model):
#     product_choices = (('Injection Mold', 'Injection Mold'),
#                ('Injection Stretch Blow Mold', 'Injection Stretch Blow Mold'),
#                ('Assembly', 'Assembly'),
#                ('Print', 'Print'))
#
#     inspection_choices = (('Round Sheet', 'Round Sheet'),
#                           ('Startup Shot', 'Startup Shot'),
#                           ('System', 'System'),
#                           ('Custom', 'Custom'))
#
#     plant_locations = (('Somerville', 'Somerville'), ('Brantford', 'Brantford'))
#
#     class Meta:
#         verbose_name = 'Top Level Inspection'
#         verbose_name_plural = 'Top Level Inspections'
#
#     uut_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # 'uuid-field'
#     inspection_type =  models.CharField(max_length=35, choices=inspection_choices) #  ['Round Sheet', 'Startup Shot']
#     product_type = models.CharField(max_length=35, choices=product_choices) # ['Injection Mold', 'Injection Stretch Blow Mold', 'Assembly', 'Print']
#     job_number = models.CharField(max_length=20, verbose_name='Job Number') # '19200.001'
#     production_date = models.DateField(verbose_name='Production Date')
#     start_date_time = models.DateTimeField(verbose_name='Inspection Start Date-Time') # '2016-01-02 10:00:00'
#     part_number = models.CharField(max_length=20, verbose_name='Part Number') # '353-900001'
#     mold_number = models.CharField(max_length=20, verbose_name='Mold Number') #'353-500001'
#     sta_reported = models.CharField(max_length=5, verbose_name='STA Reported') # 'IMM 01'
#     shift = models.CharField(max_length=5, verbose_name='Shift') #[1,2,3]
#     inspection_result = models.IntegerField(verbose_name='Inspection Result') # [0,1]
#     location =  models.CharField(max_length=20, choices=plant_locations)  #['Somerville', 'Brantford']
#
#
# class Step(models.Model):
#     class Meta:
#         verbose_name = 'Inspection Step'
#         verbose_name_plural = 'Inspections Step'
#
#     step_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #'uuid-field'
#     uut_id = models.ForeignKey(to='Inspection') # 'uuid-field foreign key'
#     step_name = models.ForeignKey(to=StaticInspection, verbose_name='Step Name') # may need to work on this
#     step_result = models.IntegerField(verbose_name='Step Result') # [0,1]
#     start_date_time = models.DateTimeField(verbose_name='Inspection Step Start Date-Time') # '2016-01-02 10:00:00'
#
#
# class PropNumericLimit(models.Model):
#     class Meta:
#         verbose_name = 'Inspection Property Numeric Limit'
#         verbose_name_plural = 'Inspections Property Numeric Limit'
#
#     prop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     step_id = models.ForeignKey(to='Step')
#     prop_tag_id = models.ForeignKey(to='StaticInspection')
#     prop_value = models.DecimalField(verbose_name='Value')
#     low_limit = models.DecimalField(verbose_name='Low Limit')
#     high_limit = models.DecimalField(verbose_name='High Limit')
#     prop_result = models.IntegerField(verbose_name='Prop Result') # [-1, 0, 1]
#     date_time = models.DateTimeField(verbose_name='Prop Date-Time') # '2016-01-02 10:00:00'
#     cav_id = models.CharField(max_length=5, verbose_name='Cavity ID')
#     head_id = models.CharField(max_length=5, verbose_name='Head ID')
#
#
# class PropFloat(models.Model):
#     class Meta:
#         verbose_name = 'Inspection Property Float'
#         verbose_name_plural = 'Inspections Property Float'
#
#     prop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     step_id = models.ForeignKey(to='Step')
#     prop_tag_id = models.ForeignKey(to='StaticInspection')
#     prop_value = models.FloatField(verbose_name='Value')
#     prop_result = models.IntegerField(verbose_name='Prop Result') # [-1, 0, 1]
#     date_time = models.DateTimeField(verbose_name='Prop Date-Time') # '2016-01-02 10:00:00'
#     cav_id = models.CharField(max_length=5, verbose_name='Cavity ID')
#     head_id = models.CharField(max_length=5, verbose_name='Head ID')
#
#
# class PropInt(models.Model):
#     class Meta:
#         verbose_name = 'Inspection Property Int'
#         verbose_name_plural = 'Inspections Property Int'
#
#     prop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     step_id = models.ForeignKey(to='Step')
#     prop_tag_id = models.ForeignKey(to='StaticInspection')
#     prop_value = models.IntegerField(verbose_name='Value')
#     prop_result = models.IntegerField(verbose_name='Prop Result') # [-1, 0, 1]
#     date_time = models.DateTimeField(verbose_name='Prop Date-Time') # '2016-01-02 10:00:00'
#     cav_id = models.CharField(max_length=5, verbose_name='Cavity ID')
#     head_id = models.CharField(max_length=5, verbose_name='Head ID')
#
#
# class PropBool(models.Model):
#     class Meta:
#         verbose_name = 'Inspection Property Boolean'
#         verbose_name_plural = 'Inspections Property Boolean'
#
#     prop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     step_id = models.ForeignKey(to='Step')
#     prop_tag_id = models.ForeignKey(to='StaticInspection')
#     prop_value = models.BooleanField(verbose_name='Value')
#     prop_fail_reason = models.ForeignKey(to='StaticInspectionBool')
#     prop_result = models.IntegerField(verbose_name='Prop Result') # [-1, 0, 1]
#     date_time = models.DateTimeField(verbose_name='Prop Date-Time') # '2016-01-02 10:00:00'
#     cav_id = models.CharField(max_length=5, verbose_name='Cavity ID')
#     head_id = models.CharField(max_length=5, verbose_name='Head ID')
#
#
# class PropText(models.Model):
#     class Meta:
#         verbose_name = 'Inspection Property Text'
#         verbose_name_plural = 'Inspections Property Text'
#
#     prop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     step_id = models.ForeignKey(to='Step')
#     prop_tag_id = models.ForeignKey(to='StaticInspection')
#     prop_value = models.CharField(max_length=75, verbose_name='Value')
#     prop_result = models.IntegerField(verbose_name='Prop Result') # [-1, 0, 1]
#     date_time = models.DateTimeField(verbose_name='Prop Date-Time') # '2016-01-02 10:00:00'
#     cav_id = models.CharField(max_length=5, verbose_name='Cavity ID')
#     head_id = models.CharField(max_length=5, verbose_name='Head ID')
#
#
# class StaticInspectionGroup(models.Model):
#     product_types = (('Injection Mold', 'Injection Mold'),
#                ('Injection Stretch Blow Mold', 'Injection Stretch Blow Mold'),
#                ('Assembly', 'Assembly'),
#                ('Print', 'Print'))
#
#     plant_locations = (('Somerville', 'Somerville'), ('Brantford', 'Brantford'))
#
#     class Meta:
#         verbose_name = 'Inspection Name'
#         verbose_name_plural = 'Inspections Names'
#
#     inspection_name_short = models.CharField(max_length=25, verbose_name='Inspection Group')
#     inspection_name_desc = models.CharField(max_length=25, verbose_name='Inspection Group Description')
#     product_type = models.CharField(max_length=25, choices=product_types, verbose_name='Product Type')
#     apply_to_all = models.BooleanField(verbose_name='Apply to all parts in product type?')
#     location =  models.CharField(max_length=20, choices=plant_locations)
#
#
# class StaticInspection(models.Model):
#     class Meta:
#         verbose_name = 'Static Tag (Inspection) Names'
#         verbose_name_plural = 'Static Tag (Inspections) Part'
#
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # 'uuid-field'
#     static_inspection_group = models.ForeignKey(to=StaticInspectionGroup)
#     tag_description_short = 'Part Weight'
#     tag_description_desc = 'Part Weight bla bla bla'
#     inspection_type = ['Numeric Limit', 'Float', 'Int', 'Bool', 'Text']
#
#
# class StaticInspectionLimit(models.Model):
#     class Meta:
#         verbose_name = 'Static Tag (Inspections) Limit'
#         verbose_name_plural = 'Static Tag (Inspections) Limits'
#
#     id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # 'uuid-field'
#     static_inspection_id = models.ForeignKey(to=StaticInspection)
#     part_id = '353-900001'
#     low_limit = models.DecimalField(verbose_name='Low Limit')
#     high_limit = models.DecimalField(verbose_name='High Limit')
#
#
#
# class StaticInspectionBool(models.Model):
#     class Meta:
#         verbose_name = 'Static Pass/Fail (Inspections) Limit'
#         verbose_name_plural = 'Static Tag (Inspections) Limits'
#
#     id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # 'uuid-field'
#     part_id = '353-900001'
#     reason = ''
#
#
