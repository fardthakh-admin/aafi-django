from django.contrib import admin
from .models import *


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "patients":
            kwargs["required"] = False
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "patients":
            kwargs["required"] = False
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "patients":
            kwargs["required"] = False
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Biomarkers)
class BiomarkersAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "patients":
            kwargs["required"] = False
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "patients":
            kwargs["required"] = False
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(CBT)
class CBTAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "patients":
            kwargs["required"] = False
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ["patient", "activity", "challenge", "checkIn", "goal", "badge", "game"]:
            kwargs["required"] = False
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(HistoricalDiagnosis)
class HistoricalDiagnosisAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "patients":
            kwargs["required"] = False
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "patients":
            kwargs["required"] = False
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "my_doctor":
            kwargs["required"] = False
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'email', 'is_active')
    # list_display_links=['name', 'price', 'active', 'category']
    list_editable = ['first_name', 'last_name',  'is_active'] #edit list
    search_fields = ['first_name', 'last_name', 'username', 'email', 'is_active']
    list_filter = ['first_name', 'last_name', 'is_active', 'username', 'email']
    # fields=['first_name', 'last_name']
admin.site.register(User, UserAdmin)
admin.site.register(Doctor)
admin.site.register(Challenge)
admin.site.register(Message)
admin.site.register(Badge)
admin.site.register(Game)
admin.site.register(Question)




