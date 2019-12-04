# -*- coding: utf-8 -*-

from django.contrib import admin
from disa_app.models import Document, DocumentColonyState, DocumentRecordType, DocumentSourceType, DocumentLocation


class DocumentColoniesInline( admin.TabularInline ):
    """ Allows the DocumentAdmin to view/add/edit DocumentColonyState entries,
        _and_ the DocumentColonyStateAdmin to view/add/edit Document entries.
        From <https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#working-with-many-to-many-models>:
        ...The through attribute is a reference to the model that manages the many-to-many relation...
        """
    model = DocumentColonyState.documents.through
    extra = 1


class DocumentRecordTypeInline( admin.TabularInline ):
    model = DocumentRecordType.documents.through
    extra = 1


class DocumentSourceTypeInline( admin.TabularInline ):
    model = DocumentSourceType.documents.through
    extra = 1


class DocumentLocationInline( admin.TabularInline ):
    model = DocumentLocation.documents.through
    extra = 1


class DocumentAdmin( admin.ModelAdmin ):
    list_display = [ 'default_date', 'display_text' ]
    list_filter = [ 'display_text' ]
    ordering = [ 'display_text' ]
    inlines = [ DocumentColoniesInline, DocumentRecordTypeInline, DocumentSourceTypeInline, DocumentLocationInline ]
    # save_on_top = True
admin.site.register( Document, DocumentAdmin )


class DocumentColonyStateAdmin( admin.ModelAdmin ):
    """ From <https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#working-with-many-to-many-models>...
        The `exclude` disables the default admin-widget that would normally offer the Document view/add/edit capabilities,
        because the inline feature will be used.
        """
    list_display = [
        'name' ]
    list_filter = [
        'name', 'documents' ]
    ordering = [ 'name' ]
    inlines = [ DocumentColoniesInline ]
    exclude = [ 'documents' ]  #
    # save_on_top = True
admin.site.register( DocumentColonyState, DocumentColonyStateAdmin )


class DocumentRecordTypeAdmin( admin.ModelAdmin ):
    list_display = [
        'name' ]
    list_filter = [
        'name', 'documents' ]
    ordering = [ 'name' ]
    inlines = [ DocumentRecordTypeInline ]
    exclude = [ 'documents' ]  #
    # save_on_top = True
admin.site.register( DocumentRecordType, DocumentRecordTypeAdmin )


class DocumentSourceTypeAdmin( admin.ModelAdmin ):
    list_display = [
        'name' ]
    list_filter = [
        'name', 'documents' ]
    ordering = [ 'name' ]
    inlines = [ DocumentSourceTypeInline ]
    exclude = [ 'documents' ]  #
    # save_on_top = True
admin.site.register( DocumentSourceType, DocumentSourceTypeAdmin )


class DocumentLocationAdmin( admin.ModelAdmin ):
    list_display = [
        'name' ]
    list_filter = [
        'name', 'documents' ]
    ordering = [ 'name' ]
    inlines = [ DocumentLocationInline ]
    exclude = [ 'documents' ]  #
    # save_on_top = True
admin.site.register( DocumentLocation, DocumentLocationAdmin )







# # ===========================
# # external DBs
# # ===========================


# class MultiDBModelAdmin(admin.ModelAdmin):
#     # <https://docs.djangoproject.com/en/1.11/topics/db/multi-db/>

#     # A handy constant for the name of the alternate database.
#     using = 'disa_non_managed'

#     def get_queryset(self, request):
#         # Tell Django to look for objects on the 'other' database.
#         return super(MultiDBModelAdmin, self).get_queryset(request).using(self.using)


# class ExtPeopleAdmin(MultiDBModelAdmin):
#     search_fields = ['id', 'first_name', 'last_name']
#     list_display = ['id', 'first_name', 'last_name', 'comments']
# admin.site.register(ExtPeople, ExtPeopleAdmin)


# class ExtReferentsAdmin(MultiDBModelAdmin):
#     search_fields = ['id', 'age', 'sex', 'primary_name']
#     list_display = ['id', 'age', 'sex', 'primary_name']
# admin.site.register(ExtReferents, ExtReferentsAdmin)
