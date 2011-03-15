# -*- coding: utf-8 -*-

import csv

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from sarpaminfohub.infohub.models import Formulation, MSHPrice


class Command(BaseCommand):
    args = '<csv_file>'
    help = 'Enter the CVS file for the MSH prices'

    def handle(self, *args, **options):
        csvReader = csv.reader(open(args[0]), delimiter="\t")

        currency_line = next(csvReader)
        next(csvReader)

        period = currency_line[0].split(' ')[2]

        for row in csvReader:
            (formulation, msh_price, dummy) = row
            msh_price = msh_price.strip()

            if msh_price:
                try:
                    f = Formulation.objects.get(name=formulation)
                    MSHPrice.objects.create(formulation=f, period=period, price=msh_price)
                except IntegrityError:
                    msh = MSHPrice.objects.get(formulation=f, period=period)
                    msh.price = msh_price
                    msh.save()
                except Formulation.DoesNotExist:
                    print "Formulation %s doesn't exist" % (formulation,)
