# # This is an auto-generated Django model module.
# # You'll have to do the following manually to clean this up:
# #   * Rearrange models' order
# #   * Make sure each model has one field with primary_key=True
# #   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
# #   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# # Feel free to rename the models, but don't rename db_table values or field names.

# import logging
# from django.db import models


# log = logging.getLogger(__name__)


# class ExtEnslavementTypes(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '1_enslavement_types'


# class ExtLocationTypes(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '1_location_types'


# class ExtLocations(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '1_locations'


# class ExtNameTypes(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '1_name_types'


# class ExtNationalContext(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '1_national_context'


# class ExtPeople(models.Model):
#     first_name = models.CharField(max_length=255, blank=True, null=True)
#     last_name = models.CharField(max_length=255, blank=True, null=True)
#     comments = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '1_people'


# class ExtRaces(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '1_races'


# class ExtReferenceTypes(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '1_reference_types'


# class ExtRoleRelationshipTypes(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '1_role_relationship_types'


# class ExtRoles(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)
#     name_as_relationship = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '1_roles'


# class ExtTitles(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '1_titles'


# class ExtTribes(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '1_tribes'


# class ExtUsers(models.Model):
#     role = models.CharField(max_length=64, blank=True, null=True)
#     name = models.CharField(max_length=64, blank=True, null=True)
#     email = models.CharField(max_length=120, blank=True, null=True)
#     created = models.DateTimeField(blank=True, null=True)
#     last_login = models.DateTimeField(blank=True, null=True)
#     password_hash = models.CharField(max_length=128, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '1_users'


# class ExtVocations(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '1_vocations'


# class ExtZoteroFields(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)
#     display_name = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '1_zotero_fields'


# class ExtZoteroTypes(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)
#     creator_name = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '1_zotero_types'


# class ExtCitationTypes(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)
#     zotero_type = models.ForeignKey(ExtZoteroTypes, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = '2_citation_types'


# class ExtReferencetypeRoles(models.Model):
#     reference_type = models.ForeignKey(ExtReferenceTypes, models.DO_NOTHING, db_column='reference_type', blank=True, null=True)
#     role = models.ForeignKey(ExtRoles, models.DO_NOTHING, db_column='role', blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '2_referencetype_roles'


# class ExtRoleRelationships(models.Model):
#     role1 = models.ForeignKey(ExtRoles, models.DO_NOTHING, db_column='role1', blank=True, null=True, related_name='role1_relationships')
#     role2 = models.ForeignKey(ExtRoles, models.DO_NOTHING, db_column='role2', blank=True, null=True, related_name='role2_relationships')
#     relationship_type = models.ForeignKey(ExtRoleRelationshipTypes, models.DO_NOTHING, db_column='relationship_type', blank=True, null=True)
#     alternate_text = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '2_role_relationships'


# class ExtZoterotypeFields(models.Model):
#     zotero_type = models.ForeignKey(ExtZoteroTypes, models.DO_NOTHING, blank=True, null=True)
#     zotero_field = models.ForeignKey(ExtZoteroFields, models.DO_NOTHING, blank=True, null=True)
#     rank = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '2_zoterotype_fields'


# class ExtCitations(models.Model):
#     citation_type = models.ForeignKey(ExtCitationTypes, models.DO_NOTHING)
#     display = models.CharField(max_length=500, blank=True, null=True)
#     zotero_id = models.CharField(max_length=255, blank=True, null=True)
#     comments = models.TextField(blank=True, null=True)
#     acknowledgements = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '3_citations'


# class ExtCitationtypeReferencetypes(models.Model):
#     citation_type = models.ForeignKey(ExtCitationTypes, models.DO_NOTHING, db_column='citation_type', blank=True, null=True)
#     reference_type = models.ForeignKey(ExtReferenceTypes, models.DO_NOTHING, db_column='reference_type', blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '3_citationtype_referencetypes'


# class ExtCitationFields(models.Model):
#     citation = models.ForeignKey(ExtCitations, models.DO_NOTHING, blank=True, null=True)
#     field = models.ForeignKey(ExtZoteroFields, models.DO_NOTHING, blank=True, null=True)
#     field_data = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '4_citation_fields'


# class ExtReferences(models.Model):
#     citation = models.ForeignKey(ExtCitations, models.DO_NOTHING)
#     reference_type = models.ForeignKey(ExtReferenceTypes, models.DO_NOTHING)
#     national_context = models.ForeignKey(ExtNationalContext, models.DO_NOTHING)
#     date = models.DateField(blank=True, null=True)
#     transcription = models.TextField(blank=True, null=True)
#     # date_detail = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '4_references'


# class ExtHasLocation(models.Model):
#     reference = models.ForeignKey(ExtReferences, models.DO_NOTHING, blank=True, null=True)
#     location = models.ForeignKey(ExtLocations, models.DO_NOTHING, blank=True, null=True)
#     location_type = models.ForeignKey(ExtLocationTypes, models.DO_NOTHING, blank=True, null=True)
#     location_rank = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '5_has_location'


# class ExtReferenceEdits(models.Model):
#     reference = models.ForeignKey(ExtReferences, models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(ExtUsers, models.DO_NOTHING, blank=True, null=True)
#     timestamp = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '5_reference_edits'


# class ExtReferents(models.Model):
#     age = models.CharField(max_length=255, blank=True, null=True)
#     sex = models.CharField(max_length=255, blank=True, null=True)
#     primary_name = models.ForeignKey('ExtReferentNames', models.DO_NOTHING, blank=True, null=True)
#     reference = models.ForeignKey(ExtReferences, models.DO_NOTHING)
#     person = models.ForeignKey(ExtPeople, models.DO_NOTHING, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '5_referents'


# class ExtEnslavedAs(models.Model):
#     referent = models.ForeignKey(ExtReferents, models.DO_NOTHING, db_column='referent', blank=True, null=True)
#     enslavement = models.ForeignKey(ExtEnslavementTypes, models.DO_NOTHING, db_column='enslavement', blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '6_enslaved_as'


# class ExtHasOrigin(models.Model):
#     referent = models.ForeignKey(ExtReferents, models.DO_NOTHING, db_column='referent', blank=True, null=True)
#     origin = models.ForeignKey(ExtLocations, models.DO_NOTHING, db_column='origin', blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '6_has_origin'


# class ExtHasRace(models.Model):
#     referent = models.ForeignKey(ExtReferents, models.DO_NOTHING, db_column='referent', blank=True, null=True)
#     race = models.ForeignKey(ExtRaces, models.DO_NOTHING, db_column='race', blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '6_has_race'


# class ExtHasRole(models.Model):
#     referent = models.ForeignKey(ExtReferents, models.DO_NOTHING, db_column='referent', blank=True, null=True)
#     role = models.ForeignKey(ExtRoles, models.DO_NOTHING, db_column='role', blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '6_has_role'


# class ExtHasTitle(models.Model):
#     referent = models.ForeignKey(ExtReferents, models.DO_NOTHING, db_column='referent', blank=True, null=True)
#     title = models.ForeignKey(ExtTitles, models.DO_NOTHING, db_column='title', blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '6_has_title'


# class ExtHasTribe(models.Model):
#     referent = models.ForeignKey(ExtReferents, models.DO_NOTHING, db_column='referent', blank=True, null=True)
#     tribe = models.ForeignKey(ExtTribes, models.DO_NOTHING, db_column='tribe', blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '6_has_tribe'


# class ExtHasVocation(models.Model):
#     referent = models.ForeignKey(ExtReferents, models.DO_NOTHING, db_column='referent', blank=True, null=True)
#     vocation = models.ForeignKey(ExtVocations, models.DO_NOTHING, db_column='vocation', blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '6_has_vocation'


# class ExtReferentNames(models.Model):
#     referent = models.ForeignKey(ExtReferents, models.DO_NOTHING, blank=True, null=True)
#     name_type = models.ForeignKey(ExtNameTypes, models.DO_NOTHING, blank=True, null=True)
#     first = models.CharField(max_length=255, blank=True, null=True)
#     last = models.CharField(max_length=255, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '6_referent_names'


# class ExtReferentRelationships(models.Model):
#     subject = models.ForeignKey(ExtReferents, models.DO_NOTHING, blank=True, null=True, related_name='referent_subjects')
#     object = models.ForeignKey(ExtReferents, models.DO_NOTHING, blank=True, null=True, related_name='referent_objects')
#     role = models.ForeignKey(ExtRoles, models.DO_NOTHING, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = '6_referent_relationships'


# class AlembicVersion(models.Model):
#     version_num = models.CharField(primary_key=True, max_length=32)

#     class Meta:
#         managed = False
#         db_table = 'alembic_version'
