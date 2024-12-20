from django.contrib import admin

from .models import *

admin.site.register(Commune)


class SearchableFilter(admin.SimpleListFilter):
    """
    A base filter class for searchable dropdowns.
    """
    template = 'admin/filter_select.html'


class AggressionClassFilter(SearchableFilter):
    title = 'aggression class'
    parameter_name = 'agression_class'

    def lookups(self, request, model_admin):
        # Fetch distinct aggression classes
        classes = Securite.objects.values_list('agression_class', flat=True).distinct()
        return [(cls, cls) for cls in classes if cls]  # Exclude empty values

    def queryset(self, request, queryset):
        # Filter by selected aggression class
        if self.value():
            return queryset.filter(agression_class=self.value())
        return queryset


class DepartmentFilter(SearchableFilter):
    title = 'department'
    parameter_name = 'department'

    def lookups(self, request, model_admin):
        # Fetch distinct departments from related communes
        departments = (
            Securite.objects.filter(commune__isnull=False)
            .values_list('commune__department', flat=True)
            .distinct()
        )
        return [(dep, dep) for dep in departments if dep]  # Exclude empty values

    def queryset(self, request, queryset):
        # Filter by selected department
        if self.value():
            return queryset.filter(commune__department=self.value())
        return queryset


class CommuneFilter(SearchableFilter):
    title = 'commune'
    parameter_name = 'commune'

    def lookups(self, request, model_admin):
        # Fetch distinct communes by name_full and order them alphabetically
        communes = (
            Securite.objects.filter(commune__isnull=False)
            .order_by('commune__name_full')  # Ensure alphabetical ordering
            .values_list('commune__name_full', flat=True)
            .distinct()
        )
        return [(commune, commune) for commune in communes if commune]  # Exclude empty values

    def queryset(self, request, queryset):
        # Filter by selected commune
        if self.value():
            return queryset.filter(commune__name_full=self.value())
        return queryset


class YearFilter(SearchableFilter):
    title = 'year'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        # Fetch distinct years
        years = Securite.objects.values_list('year', flat=True).distinct()
        return [(year, year) for year in years if year]  # Exclude empty values

    def queryset(self, request, queryset):
        # Filter by selected year
        if self.value():
            return queryset.filter(year=self.value())
        return queryset


@admin.register(Securite)
class SecuriteAdmin(admin.ModelAdmin):
    list_display = ('commune', 'year', 'agression_class', 'facts_value', 'aggression_unity')
    list_filter = (DepartmentFilter, CommuneFilter, YearFilter, AggressionClassFilter)