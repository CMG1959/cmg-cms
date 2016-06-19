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
        verbose_name = 'Inspection: Top Level'
        verbose_name_plural = 'Inspections: Top Level'

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
        verbose_name = 'Inspection: Step'
        verbose_name_plural = 'Inspections: Step'

    step_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #'uuid-field'
    uut = models.ForeignKey(to='Inspection', related_name='step') # 'uuid-field foreign key'
    step_name = models.ForeignKey(to='StaticInspection', verbose_name='Step Name') # may need to work on this
    step_result = models.IntegerField(verbose_name='Step Result') # [0,1]
    start_date_time = models.DateTimeField(verbose_name='Inspection Step Start Date-Time') # '2016-01-02 10:00:00'

    def __unicode__(self):
        return '%s %s %s' % (self.start_date_time, self.step_name, self.step_result)

class PropNumericLimit(models.Model):
    class Meta:
        verbose_name = 'Inspection: Step Property Numeric Limit'
        verbose_name_plural = 'Inspections: Step Property Numeric Limit'

    prop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step = models.ForeignKey(to='Step', related_name='prop_numeric')
    prop_tag = models.ForeignKey(to='StaticInspection')
    prop_value = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Value')
    low_limit = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Low Limit')
    high_limit = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='High Limit')
    prop_result = models.IntegerField(verbose_name='Prop Result') # [-1, 0, 1]
    date_time = models.DateTimeField(verbose_name='Prop Date-Time') # '2016-01-02 10:00:00'
    cav_id = models.CharField(max_length=5, verbose_name='Cavity ID')
    head_id = models.CharField(max_length=5, verbose_name='Head ID')

    def __unicode__(self):
        return '%s: %s[%s <= X <= %s] %s' %\
               (self.prop_tag, self.prop_value, self.low_limit, self.high_limit, self.cav_id)

class PropFloat(models.Model):
    class Meta:
        verbose_name = 'Inspection: Step Property Float'
        verbose_name_plural = 'Inspections: Step Property Float'

    prop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step = models.ForeignKey(to='Step', related_name='prop_float')
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
        verbose_name = 'Inspection: Step Property Int'
        verbose_name_plural = 'Inspections: Step Property Int'

    prop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step = models.ForeignKey(to='Step', related_name='prop_int')
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
        verbose_name = 'Inspection: Step Property Boolean'
        verbose_name_plural = 'Inspections: Step Property Boolean'

    prop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step = models.ForeignKey(to='Step', related_name='prop_bool')
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
        verbose_name = 'Inspection: Step Property Text'
        verbose_name_plural = 'Inspections: Step Property Text'

    prop_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    step = models.ForeignKey(to='Step', related_name='prop_text')
    prop_tag = models.ForeignKey(to='StaticInspection')
    prop_value = models.CharField(max_length=75, verbose_name='Value')
    prop_result = models.IntegerField(verbose_name='Prop Result') # [-1, 0, 1]
    date_time = models.DateTimeField(verbose_name='Prop Date-Time') # '2016-01-02 10:00:00'
    cav_id = models.CharField(max_length=5, verbose_name='Cavity ID')
    head_id = models.CharField(max_length=5, verbose_name='Head ID')

    def __unicode__(self):
        return '%s: %s' % (self.prop_tag, self.prop_value)

class StaticInspectionGroup(models.Model):
    product_types = (
                ('A', 'All'),
                ('M', 'Mold'),
               ('IMM', 'Injection Mold'),
               ('ISBM', 'Injection Stretch Blow Mold'),
               ('FAS', 'Assembly'),
               ('OFP', 'Print'))

    plant_locations = (('Somerville', 'Somerville'), ('Brantford', 'Brantford'))

    apply_log = (('All','All'),
                 ('Type','Type Specific'),
                 ('Part','Part Specific'))

    class Meta:
        verbose_name = 'Static Inspection Regime'
        verbose_name_plural = 'Static Inspection Regimes'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # 'uuid-field'
    inspection_name_short = models.CharField(max_length=25, verbose_name='Inspection Group')
    inspection_name_desc = models.CharField(max_length=200, verbose_name='Inspection Group Description')
    product_type = models.CharField(max_length=25, choices=product_types, verbose_name='Product Type')
    apply_type = models.CharField(max_length=10, choices=apply_log, verbose_name='Apply to all parts in product type?')
    location =  models.CharField(max_length=20, choices=plant_locations)

    def __unicode__(self):
        return '%s: %s' % (self.product_type, self.inspection_name_short)

class StaticInspection(models.Model):

    inspection_types = (('Numeric Limit', 'Numeric Limit'),
                        ('Float', 'Float'),
                        ('Integer', 'Integer'),
                        ('Boolean', 'Boolean'),
                        ('Text', 'Text'))

    class Meta:
        verbose_name = 'Static Inspection Steps '
        verbose_name_plural = 'Static Inspection Regime Steps'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # 'uuid-field'
    static_inspection_group = models.ForeignKey(to='StaticInspectionGroup', related_name='inspection_step')
    tag_description_short = models.CharField(max_length=25, verbose_name='Short Description')
    tag_description_desc = models.CharField(max_length=200, verbose_name='Long Description')
    inspection_type = models.CharField(max_length=25, choices=inspection_types)

    def __unicode__(self):
        return '%s: %s' % (self.static_inspection_group, self.tag_description_short)

class StaticInspectionLimit(models.Model):
    class Meta:
        verbose_name = 'Static Inspections Step Limit'
        verbose_name_plural = 'Static Inspection Step Limits'

    id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # 'uuid-field'
    static_inspection = models.ForeignKey(to='StaticInspection', related_name='inspection_limit')
    part_number = models.ForeignKey(to='part.Part', to_field='item_Number')
    low_limit = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='Low Limit')
    high_limit = models.DecimalField(max_digits=12, decimal_places=4, verbose_name='High Limit')

    def __unicode__(self):
        return '%s: %s LOW=%s, High=%s' % (self.part_number, self.static_inspection, self.low_limit, self.high_limit)

class StaticInspectionBool(models.Model):
    class Meta:
        verbose_name = 'Static Inspection Step Boolean'
        verbose_name_plural = 'Static Inspections Boolean'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # 'uuid-field'
    static_inspection = models.ForeignKey(to='StaticInspection', related_name='inspection_bool')
    part_number = models.ForeignKey(to='part.Part', to_field='item_Number')
    reason_short = models.CharField(max_length=25)
    reason_long = models.CharField(max_length=200)

    def __unicode__(self):
        return '%s: %s' % (self.part_number, self.reason_long)


class StaticInspectionPart(models.Model):
    class Meta:
        verbose_name = 'Station Inspection Steps - Part Assignment'
        verbose_name_plural = 'Station Inspection Steps - Part Assignments'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    inspection_group = models.ForeignKey(to='StaticInspectionGroup', related_name='inspection_parts')
    part_number = models.ForeignKey(to='part.Part', to_field='item_Number')

    def __unicode__(self):
        return '%s: %s' % (self.inspection_group, self.part_number)