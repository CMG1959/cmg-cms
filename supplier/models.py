from django.db import models

# Create your models here.

class supplier(models.Model):
    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'

    supplier_name = models.CharField(verbose_name='Supplier Name', max_length=25)

    def __unicode__(self):
        return self.supplier_name
