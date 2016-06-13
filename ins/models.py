from __future__ import unicode_literals

from django.db import models

class Inspection(models.Model):
    class Meta:
        verbose_name = 'Top Level Inspection'
        verbose_name_plural = 'Top Level Inspections'


class Step(models.Model):
    class Meta:
        verbose_name = 'Inspection Step'
        verbose_name_plural = 'Inspections Step'


class PropNumericLimit(models.Model):
    class Meta:
        verbose_name = 'Inspection Property Numeric Limit'
        verbose_name_plural = 'Inspections Property Numeric Limit'


class PropFloat(models.Model):
    class Meta:
        verbose_name = 'Inspection Property Float'
        verbose_name_plural = 'Inspections Property Float'


class PropInt(models.Model):
    class Meta:
        verbose_name = 'Inspection Property Int'
        verbose_name_plural = 'Inspections Property Int'


class PropBool(models.Model):
    class Meta:
        verbose_name = 'Inspection Property Boolean'
        verbose_name_plural = 'Inspections Property Boolean'


class PropText(models.Model):
    class Meta:
        verbose_name = 'Inspection Property Text'
        verbose_name_plural = 'Inspections Property Text'


class StaticTag(models.Model):
    class Meta:
        verbose_name = 'Static Tag (Inspection) Names'
        verbose_name_plural = 'Static Tag (Inspections) Part'
        # tag name, type


class StaticTagPart(models.Model):
    class Meta:
        verbose_name = 'Static Tag (Inspections) Part'
        verbose_name_plural = 'Static Tag (Inspections) Part'


class StaticTagLimit(models.Model):
    class Meta:
        verbose_name = 'Static Tag (Inspections) Limit'
        verbose_name_plural = 'Static Tag (Inspections) Limits'
        # pn, tag, low, high


class StaticTagLimit(models.Model):
    class Meta:
        verbose_name = 'Static Tag (Inspections) Limit'
        verbose_name_plural = 'Static Tag (Inspections) Limits'
        # pn, tag