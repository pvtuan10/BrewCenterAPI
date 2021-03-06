"""
Run this script in Django's Manage.py like so: `python manage.py shell < ../scripts/data_loader`
"""
import os
import sqlite3 as sql
from django.conf import settings
from django.core.management.base import BaseCommand

from brew_data.models import CountryCode, FermentableType, Fermentable, HopType, Hop, YeastType, Yeast, Style
import brew_data.data_miner.brew_target.miner as brew_target_miner

class Command(BaseCommand):
    def handle(self, **options):
        brew_target_miner.mine(self.stdout)
        source = sql.connect(os.path.join(settings.BASE_DIR, 'brew_data/data_miner/brew_target/brewtarget_processed.sqlite'))
        s = source.cursor()

        # save all country codes used
        s.execute("SELECT code from countrycode;")
        cur = s.fetchone()
        n = 0
        while cur:
            CountryCode.objects.get_or_create(code=cur[0])
            n += 1
            cur = s.fetchone()
        self.stdout.write("Updated db with {0} CountryCodes".format(n))

        # save all fermentable types used
        s.execute("SELECT name from fermentabletype;")
        cur = s.fetchone()
        n = 0
        while cur:
            FermentableType.objects.get_or_create(name=cur[0])
            n += 1
            cur = s.fetchone()
        self.stdout.write("Updated db with {0} FermentableTypes".format(n))

        # save all fermentables found
        s.execute("SELECT {0} from fermentable;".format(brew_target_miner.Fermentable.get_keys()))
        cur = s.fetchone()
        n = 0
        while cur:
            # check for collisions
            if Fermentable.objects.filter(name=cur[0]).count() == 0:
                Fermentable.objects.create(
                    name=cur[0],
                    type_id=cur[1],
                    country_id=cur[2],
                    ppg=cur[3],
                    lovibond=cur[4],
                    moisture=cur[5],
                    diastatic_power=cur[6],
                    protein=cur[7],
                    max_in_batch=cur[8],
                    is_mashed=cur[9],
                    notes=cur[10]
                )

            n += 1
            cur = s.fetchone()
        self.stdout.write("Updated db with {0} Fermentables".format(n))

        # save all hop types used
        s.execute("SELECT name from hoptype;")
        cur = s.fetchone()
        n = 0
        while cur:
            HopType.objects.get_or_create(name=cur[0])
            n += 1
            cur = s.fetchone()
        self.stdout.write("Updated db with {0} HopTypes".format(n))

        # save all hops found
        s.execute("SELECT {0} from hop;".format(brew_target_miner.Hop.get_keys()))
        cur = s.fetchone()
        n = 0
        while cur:
            # check for collisions
            if Hop.objects.filter(name=cur[0]).count() == 0:
                Hop.objects.create(
                    name=cur[0],
                    type_id=cur[1],
                    country_id=cur[2],
                    alpha_acids=cur[3],
                    beta_acids=cur[4],
                    notes=cur[5]
                )

            n += 1
            cur = s.fetchone()
        self.stdout.write("Updated db with {0} Hops".format(n))

        # save all yeast types used
        s.execute("SELECT name from yeasttype;")
        cur = s.fetchone()
        n = 0
        while cur:
            YeastType.objects.get_or_create(name=cur[0])
            n += 1
            cur = s.fetchone()
        self.stdout.write("Updated db with {0} YeastTypes".format(n))

        # save all yeast found
        s.execute("SELECT {0} from yeast;".format(brew_target_miner.Yeast.get_keys()))
        cur = s.fetchone()
        n = 0
        while cur:
            # check for collisions
            if Yeast.objects.filter(name=cur[0]).count() == 0:
                Yeast.objects.create(
                    name=cur[0],
                    type_id=cur[1],
                    is_liquid=cur[2],
                    lab=cur[3],
                    min_temp=cur[4],
                    max_temp=cur[5],
                    flocculation=cur[6],
                    attenuation=cur[7],
                    notes=cur[8]
                )

            n += 1
            cur = s.fetchone()
        self.stdout.write("Updated db with {0} Yeast".format(n))

        # save all styles found
        s.execute("SELECT {0} from styles;".format(brew_target_miner.Style.get_keys()))
        cur = s.fetchone()
        n = 0
        while cur:
            # check for collisions
            if Style.objects.filter(name=cur[0]).count() == 0:
                Style.objects.create(
                    name=cur[0],
                    type=cur[1],
                    category=cur[2],
                    og_min=cur[3],
                    og_max=cur[4],
                    fg_min=cur[5],
                    fg_max=cur[6],
                    ibu_min=cur[7],
                    ibu_max=cur[8],
                    srm_min=cur[9],
                    srm_max=cur[10],
                    abv_min=cur[11],
                    abv_max=cur[12]
                )

            n += 1
            cur = s.fetchone()
        self.stdout.write("Updated db with {0} Styles".format(n))


        source.close()
