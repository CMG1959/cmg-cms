from __future__ import unicode_literals

from django.db import models
import uuid

class Inspection(models.Model):
    product_choices = (('IMM', 'Injection Mold'),
               ('ISBM', 'Injection Stretch Blow Mold'),
               ('FAS', 'Assembly'),
               ('OFP', 'Print'))

    inspection_choices = (('Round Sheet', 'Round Sheet'),
                          ('Startup Shot', 'Startup Shot'),
                          ('System', 'System'),
                          ('Custom', 'Custom'))

    plant_locations = (('Somerville', 'Somerville'), ('Brantford', 'Brantford'))

    class Meta:
        verbose_name = 'Top Level Inspection'
        verbose_name_plural = 'Top Level Inspections'

    uut_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # 'uuid-field'
    inspection_type =  models.CharField(max_length=35, choices=inspection_choices) #  ['Round Sheet', 'Startup Shot']
    product_type = models.CharField(max_length=35, choices=product_choices) # ['Injection Mold', 'Injection Stretch Blow Mold', 'Assembly', 'Print']
    job_number = models.CharField(max_length=20, verbose_name='Job Number') # '19200.001'
    production_date = models.DateField(verbose_name='Production Date')
    start_date_time = models.DateTimeField(verbose_name='Inspection Start Date-Time') # '2016-01-02 10:00:00'
    part_number = models.CharField(max_length=20, verbose_name='Part Number') # '353-900001'
    mold_number = models.CharField(max_length=20, verbose_name='Mold Number') #'353-500001'
    sta_reported = models.CharField(max_length=5, verbose_name='STA Reported') # 'IMM 01'
    shift = models.CharField(max_length=5, verbose_name='Shift') #[1,2,3]
    inspection_result = models.IntegerField(verbose_name='Inspection Result') # [0,1]
    location =  models.CharField(max_length=20, choices=plant_locations)  #['Somerville', 'Brantford']

    def __unicode__(self):
        return '%s Shift %s: %s %s %s' % \
               (self.production_date, self.shift, self.job_number, self.part_number, self.start_date_time)

class Step(models.Model):
    class Meta:
        verbose_name = 'Inspection Step'
        verbose_name_plural = 'Inspections Step'

    step_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #'uuid-field'
    uut = models.ForeignKey(to='Inspection') # 'uuid-field foreign key'
    step_name = models.ForeignKey(to='StaticInspection', verbose_name='Step Name') # may need to work on this
    step_result = models.IntegerField(verbose_name='Step Result') # [0,1]
    start_date_time = models.DateTimeField(verbose_name='Inspection Step Start Date-Time') # '2016-01-02 10:00:00'

    def __unicode__(self):
        return '%s %s %s' % (self.start_date_time, self.step_name, self.step_result)

class PropNumericLimit(models.Model):
    class Meta:
        verbose_name = 'Inspection Property Numeric Limit'
        verbose_name_plural = 'Inspections Property Numeric Limit'

    prop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step = models.ForeignKey(to='Step')
    prop_tag = models.ForeignKey(to='StaticInspection')
    prop_value = models.DecimalField(verbose_name='Value')
    low_limit = models.DecimalField(verbose_name='Low Limit')
    high_limit = models.DecimalField(verbose_name='High Limit')
    prop_result = models.IntegerField(verbose_name='Prop Result') # [-1, 0, 1]
    date_time = models.DateTimeField(verbose_name='Prop Date-Time') # '2016-01-02 10:00:00'
    cav_id = models.CharField(max_length=5, verbose_name='Cavity ID')
    head_id = models.CharField(max_length=5, verbose_name='Head ID')

    def __unicode__(self):
        return '%s: %s[%s <= X <= %s] %s' %\
               (self.prop_tag, self.prop_value, self.low_limit, self.high_limit, self.cav_id)

class PropFloat(models.Model):
    class Meta:
        verbose_name = 'Inspection Property Float'
        verbose_name_plural = 'Inspections Property Float'

    prop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step = models.ForeignKey(to='Step')
    prop_tag = models.ForeignKey(to='StaticInspection')
    prop_value = models.FloatField(verbose_name='Value')
    prop_result = models.IntegerField(verbose_name='Prop Result') # [-1, 0, 1]
    date_time = models.DateTimeField(verbose_name='Prop Date-Time') # '2016-01-02 10:00:00'
    cav_id = models.CharField(max_length=5, verbose_name='Cavity ID')
    head_id = models.CharField(max_length=5, verbose_name='Head ID')

    def __unicode__(self):
        return '%s: %s' % (self.prop_tag, self.prop_value)

class PropInt(models.Model):
    class Meta:
        verbose_name = 'Inspection Property Int'
        verbose_name_plural = 'Inspections Property Int'

    prop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step = models.ForeignKey(to='Step')
    prop_tag = models.ForeignKey(to='StaticInspection')
    prop_value = models.IntegerField(verbose_name='Value')
    prop_result = models.IntegerField(verbose_name='Prop Result') # [-1, 0, 1]
    date_time = models.DateTimeField(verbose_name='Prop Date-Time') # '2016-01-02 10:00:00'
    cav_id = models.CharField(max_length=5, verbose_name='Cavity ID')
    head_id = models.CharField(max_length=5, verbose_name='Head ID')

    def __unicode__(self):
        return '%s: %s' % (self.prop_tag, self.prop_value)


class PropBool(models.Model):
    class Meta:
        verbose_name = 'Inspection Property Boolean'
        verbose_name_plural = 'Inspections Property Boolean'

    prop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step = models.ForeignKey(to='Step')
    prop_tag = models.ForeignKey(to='StaticInspection')
    prop_value = models.ForeignKey(to='StaticInspectionBool')
    prop_result = models.IntegerField(verbose_name='Prop Result') # [-1, 0, 1]
    date_time = models.DateTimeField(verbose_name='Prop Date-Time') # '2016-01-02 10:00:00'
    cav_id = models.CharField(max_length=5, verbose_name='Cavity ID')
    head_id = models.CharField(max_length=5, verbose_name='Head ID')

    def __unicode__(self):
        return '%s: %s' % (self.prop_tag, self.prop_value)

class PropText(models.Model):
    class Meta:
        verbose_name = 'Inspection Property Text'
        verbose_name_plural = 'Inspections Property Text'

    prop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step = models.ForeignKey(to='Step')
    prop_tag = models.ForeignKey(to='StaticInspection')
    prop_value = models.CharField(max_length=75, verbose_name='Value')
    prop_result = models.IntegerField(verbose_name='Prop Result') # [-1, 0, 1]
    date_time = models.DateTimeField(verbose_name='Prop Date-Time') # '2016-01-02 10:00:00'
    cav_id = models.CharField(max_length=5, verbose_name='Cavity ID')
    head_id = models.CharField(max_length=5, verbose_name='Head ID')

    def __unicode__(self):
        return '%s: %s' % (self.prop_tag, self.prop_value)

class StaticInspectionGroup(models.Model):
    product_types = (('IMM', 'Injection Mold'),
               ('ISBM', 'Injection Stretch Blow Mold'),
               ('FAS', 'Assembly'),
               ('OFP', 'Print'))

    plant_locations = (('Somerville', 'Somerville'), ('Brantford', 'Brantford'))

    apply_log = (('All','All'),
                 ('Type','Type Specific'),
                 ('Part','Part Specific'))

    class Meta:
        verbose_name = 'Inspection Name'
        verbose_name_plural = 'Inspections Names'

    inspection_name_short = models.CharField(max_length=25, verbose_name='Inspection Group')
    inspection_name_desc = models.CharField(max_length=25, verbose_name='Inspection Group Description')
    product_type = models.CharField(max_length=25, choices=product_types, verbose_name='Product Type')
    apply_type = models.CharField(max_length=10, choices=apply_log, verbose_name='Apply to all parts in product type?')
    location =  models.CharField(max_length=20, choices=plant_locations)

    def __unicode__(self):
        return '%s: %s' % (self.product_type, self.inspection_name_short)

class StaticInspection(models.Model):

    inspection_types = ((4,'Numeric Limit'),
                        (2, 'Float'),
                        (3, 'Integer'),
                        (1, 'Boolean'),
                        (5, 'Text'))

    class Meta:
        verbose_name = 'Static Tag (Inspection) Names'
        verbose_name_plural = 'Static Tag (Inspections) Part'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # 'uuid-field'
    static_inspection_group = models.ForeignKey(to='StaticInspectionGroup')
    tag_description_short = models.CharField(max_length=25, verbose_name='Short Description')
    tag_description_desc = models.CharField(max_length=200, verbose_name='Long Description')
    inspection_type = models.CharField(max_length=25, choices=inspection_types)

    def __unicode__(self):
        return '%s: %s' % (self.static_inspection_group, self.tag_description_short)

class StaticInspectionLimit(models.Model):
    class Meta:
        verbose_name = 'Static Tag (Inspections) Limit'
        verbose_name_plural = 'Static Tag (Inspections) Limits'

    id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # 'uuid-field'
    static_inspection = models.ForeignKey(to='StaticInspection')
    part_number = models.ForeignKey(to='Part', to_field='item_Number')
    low_limit = models.DecimalField(verbose_name='Low Limit')
    high_limit = models.DecimalField(verbose_name='High Limit')

    def __unicode__(self):
        return '%s: %s LOW=%s, High=%s' % (self.part_number, self.static_inspection, self.low_limit, self.high_limit)

class StaticInspectionBool(models.Model):
    class Meta:
        verbose_name = 'Static Pass/Fail (Inspections) Limit'
        verbose_name_plural = 'Static Tag (Inspections) Limits'

    id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # 'uuid-field'
    part_number = models.ForeignKey(to='Part', to_field='item_Number')
    reason_short = models.CharField(max_length=25)
    reason_long = models.CharField(max_length=200)

    def __unicode__(self):
        return '%s: %s' % (self.part_number, self.reason_long)