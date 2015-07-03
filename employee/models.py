from django.db import models

# Create your models here.

class organizations(models.Model):
    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

    org_name = models.CharField(verbose_name="Organization Name", max_length=25)

    def __unicode__(self):
        return self.org_name


class employee(models.Model):
    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    last_name = models.CharField(verbose_name="Last Name", max_length=25)
    first_name = models.CharField(verbose_name="First Name", max_length=25)
    employee_id = models.CharField(verbose_name="Employee ID", max_length=25)
    organization_name = models.ForeignKey(organizations, verbose_name="Organization Name")
    shift_id = models.IntegerField(default=1,verbose_name="Shift")

    def __unicode__(self):
        return '%s - %s' % (self.last_name, self.first_name)
