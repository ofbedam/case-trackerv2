# #yerler/models.py
# from django.db import models
#
# class Country(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100, unique=True)
#
#     def __str__(self):
#         return self.name
#     class Meta:
#         # managed = False
#         db_table = 'countries'
#
# class State(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255 )
#     country = models.ForeignKey(Country, models.DO_NOTHING)
#
#     class Meta:
#         # managed = False
#         db_table = 'states'
#
#     def __str__(self):
#         return self.name
#         # return f"{self.name} {self.country}"
#     class Meta:
#         # managed = False
#         db_table = 'states'
#
# class City(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     state = models.ForeignKey('State', models.DO_NOTHING)
#     country = models.ForeignKey('Country', models.DO_NOTHING)
#
#     def __str__(self):
#         # return f"{self.name}  / {self.state}/ {self.country}"
#
#         return self.name
#     class Meta:
#         # managed = False
#         db_table = 'cities'
#
#
#
# yerler/models.py
from django.db import models
from smart_selects.db_fields import ChainedForeignKey

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    name_eng = models.CharField(max_length=100, unique=True)
    iso3 = models.CharField(max_length=3, blank=True, null=True)
    numeric_code = models.CharField(max_length=3, blank=True, null=True)
    iso2 = models.CharField(max_length=2, blank=True, null=True)
    phonecode = models.CharField(max_length=255, blank=True, null=True)
    capital = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=255, blank=True, null=True)
    currency_name = models.CharField(max_length=255, blank=True, null=True)
    currency_symbol = models.CharField(max_length=255, blank=True, null=True)
    tld = models.CharField(max_length=255, blank=True, null=True)
    native = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    subregion = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    timezones = models.TextField(blank=True, null=True)
    translations = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    emoji = models.CharField(max_length=191, blank=True, null=True)
    emojiu = models.CharField(db_column='emojiU', max_length=191, blank=True, null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()
    flag = models.IntegerField()
    wikidataid = models.CharField(db_column='wikiDataId', max_length=255, blank=True, null=True,
                                  db_comment='Rapid API GeoDB Cities')  # Field name made lowercase.

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'countries'

class State(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=2)
    fips_code = models.CharField(max_length=255, blank=True, null=True)
    iso2 = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=191, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField()
    flag = models.IntegerField()
    wikidataid = models.CharField(db_column='wikiDataId', max_length=255, blank=True, null=True,
                                  db_comment='Rapid API GeoDB Cities')  # Field name made lowercase.

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'states'

class City(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    state = ChainedForeignKey(
        State,
        chained_field="country",
        chained_model_field="country",
        show_all=False,
        auto_choose=True,
        sort=True
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'cities'
