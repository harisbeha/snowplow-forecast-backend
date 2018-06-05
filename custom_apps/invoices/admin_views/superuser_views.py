from django.contrib.admin import register, ModelAdmin
from import_export.admin import ImportExportActionModelAdmin

from ..models import *
from ..resources import *
from django.forms.models import BaseModelFormSet

from django.forms.models import BaseInlineFormSet, BaseFormSet
from import_export.admin import ExportMixin
import nested_admin


# all the views in this file should be visible only to the superuser
class SuperuserModelAdmin(ImportExportActionModelAdmin):
    exclude = ['address_info_storage']
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

def invoice(self, obj=None):
    return self.invoice

def vendor(self, obj=None):
    return self.service_provider

def service_provider(self, obj=None):
    return self.service_provider

def location(self, obj=None):
    return self.building

def deicing_rate(self, obj=None):
    return self.building.deice_rate

def deicing_tax(self, obj=None):
    return self.building.deice_tax

def plow_rate(self, obj=None):
    return self.building.plow_rate

def plow_tax(self, obj=None):
    return self.building.plow_tax

def work_order(self, obj=None):
    return self.work_order_code

def deicing_fee(self, obj=None):
    try:
        cost = self.building.deice_rate * self.num_salts
        return str(cost)
    except:
        return ''

def plow_fee(self, obj=None):
    try:
        cost = self.building.plow_rate * self.num_plows
        return str(cost)
    except:
        return ''

def storm_total(self, obj=None):
    total = str((self.building.plow_rate * self.num_plows) + (self.building.deice_rate * self.num_salts))
    return total

def snowfall(self, obj=None):
    import random
    snowfall = random.choice([1.2,1.4,1.5,2,2.1,3,3.4,1.8])
    return snowfall

def storm_days(self, obj=None):
    return 2

def refreeze(self, obj=None):
    return '0'


def get_locations_by_system_user(user=None):
    # vendor = Vendor.objects.filter(system_user__email='VENDOR@VENDOR.com')[0]
    vend = Vendor.objects.get(system_user__username='vendor-user@bank.com')
    locations = Building.objects.filter(service_provider=vend)
    return locations


class SRFormSet(BaseInlineFormSet):
    model = SafetyReport

    def __init__(self, *args, **kwargs):
        super(SRFormSet, self).__init__(*args, **kwargs)
        self.locations = get_locations_by_system_user(self.request.user)


from django.forms import ModelForm
# class WOrderForm(ModelForm):
#     fields = ['vendor', 'building', 'number_plows', 'number_salts']


class WOFormSet(BaseInlineFormSet):
    model = WorkOrder

    def __init__(self, *args, **kwargs):
        super(WOFormSet, self).__init__(*args, **kwargs)
        self.locations = get_locations_by_system_user(self.request.user)


from django.utils.functional import curry


class WorkOrderInline(admin.TabularInline):
    model = WorkOrder
    formset = WOFormSet

    def get_formset(self, *args, **kwargs):
        formset = super(WorkOrderInline, self).get_formset(*args, **kwargs)
        return formset

    def get_formset(self, request, obj=None, **kwargs):
        """
        Pre-populating formset using GET params
        """
        initial = []
        if request.method == "GET":
            #
            # Populate initial based on request
            #
            locations = get_locations_by_system_user(request.user).values('id')
            s_name = None if not obj else obj.storm_name
            s_date = '2017-12-10' if not obj else obj.storm_date
            s_provider = None if not obj else obj.service_provider

            for l in locations:
                # print({'building': str(l['id']), 'service_provider': s_provider,
                #                 'storm_name': s_name,'storm_date': s_date,
                #                 'last_service_date': '2017-12-09',
                #                 'failed_service':False, 'work_order_code':'Td1290'})
                initial.append({})
        formset = super(WorkOrderInline, self).get_formset(request, obj, **kwargs)
        formset.__init__ = curry(formset.__init__, initial=initial)
        formset.request = request
        return formset

    def get_extra(self, request, obj=None, **kwargs):
        """Dynamically sets the number of extra forms. 0 if the related object
        already exists or the extra configuration otherwise."""
        if obj:
            return 0
        return get_locations_by_system_user(request.user).count()


class SafetyReportInline(admin.TabularInline):
    model = SafetyReport
    # form = SafetyReportForm
    formset = SRFormSet

    def get_formset(self, *args, **kwargs):
        formset = super(SafetyReportInline, self).get_formset(*args, **kwargs)
        return formset

    def get_formset(self, request, obj=None, **kwargs):
        """
        Pre-populating formset using GET params
        """
        initial = []
        if request.method == "GET":
            #
            # Populate initial based on request
            #
            locations = get_locations_by_system_user(request.user).values('id')
            # print(locations.count())
            for l in locations:
                initial.append({'building': str(l['id']), 'site_serviced': True, 'safe_to_open': True, 'service_time': '2017-12-09'})
            # initial.append({
            #     'building': locations,
            # })
        formset = super(SafetyReportInline, self).get_formset(request, obj, **kwargs)
        formset.__init__ = curry(formset.__init__, initial=initial)
        formset.request = request
        return formset

    def get_extra(self, request, obj=None, **kwargs):
        """Dynamically sets the number of extra forms. 0 if the related object
        already exists or the extra configuration otherwise."""
        if obj:
            # Don't add any extra forms if the related object already exists.
            return 0
        return get_locations_by_system_user(request.user).count()


class InvoiceAdmin(admin.ModelAdmin):
    exclude=['remission_address', 'address_info_storage']
    inlines = [SafetyReportInline]
    limited_manytomany_fields = {}

    def get_changeform_initial_data(self, request):
        """
        Get the initial form data from the request's GET params.
        """
        from django.db import models
        initial_o = Invoice().__dict__
        initial = initial_o
        for k in initial:
            try:
                f = self.model._meta.get_field(k)
            except Exception as e:
                continue
            # We have to special-case M2Ms as a list of comma-separated PKs.
            if isinstance(f, models.ManyToManyField):
                initial[k] = initial[k].split(",")
        else:
            from django.db import models
            initial_o = Invoice().__dict__
            initial = initial_o
            for k in initial:
                try:
                    f = self.model._meta.get_field(k)
                except Exception as e:
                    continue
                # We have to special-case M2Ms as a list of comma-separated PKs.
                if isinstance(f, models.ManyToManyField):
                    initial[k] = initial[k].split(",")


class PrelimInvoiceAdmin(admin.ModelAdmin, ExportMixin):
    exclude=['remission_address', 'address_info_storage']
    resource_class = InvoiceResource
    inlines = [WorkOrderInline]
    limited_manytomany_fields = {}

    def get_changeform_initial_data(self, request):
        """
        Get the initial form data from the request's GET params.
        """
        from django.db import models
        initial_o = Invoice().__dict__
        initial = initial_o
        for k in initial:
            try:
                f = self.model._meta.get_field(k)
            except Exception as e:
                continue
            # We have to special-case M2Ms as a list of comma-separated PKs.
            if isinstance(f, models.ManyToManyField):
                initial[k] = initial[k].split(",")
        else:
            from django.db import models
            initial_o = Invoice().__dict__
            initial = initial_o
            for k in initial:
                try:
                    f = self.model._meta.get_field(k)
                except Exception as e:
                    continue
                # We have to special-case M2Ms as a list of comma-separated PKs.
                if isinstance(f, models.ManyToManyField):
                    initial[k] = initial[k].split(",")


# @register(Invoice)
# class InvoiceAdmin(admin.ModelAdmin):
#     model = Invoice
#     list_display = ['storm_name','storm_date']
#     exclude = ['remission_address', 'address_info_storage']
#     inlines = [SafetyReportInline]


# @register(InvoiceProxyVendor)
# class InvoiceAdmin(admin.ModelAdmin):
#     model = InvoiceProxyVendor
#     list_display = ['storm_name','storm_date']
#     exclude = ['remission_address', 'address_info_storage']
#     inlines = [SafetyReportInline]
#     # change_form_template = 'admin/invoice_admin.html'


# @register(InvoiceProxyPrelim)
# class InvoiceAdmin(admin.ModelAdmin):
#     model = InvoiceProxyPrelim
#     list_display = ['storm_name','storm_date']
#     exclude = ['remission_address', 'address_info_storage']
#     inlines = [WorkOrderInline]
#     change_form_template = 'admin/invoice_admin.html'


# @register(InvoiceProxyForecast)
# class InvoiceForecastAdmin(admin.ModelAdmin):
#
#     pass

class ServiceForecast(admin.ModelAdmin):
    model = WorkProxyServiceForecast
    list_filter = ('invoice_id', 'invoice__storm_name', 'invoice__storm_date')
    list_display = [work_order, invoice, service_provider, location, deicing_rate, deicing_tax, plow_rate,
                    plow_tax, snowfall, storm_days, refreeze,
                    'number_salts', 'number_plows', deicing_fee, plow_fee, storm_total]

    def number_salts(self, obj):
        return obj.aggregate_invoiced_salts

    def number_plows(self, obj):
        return obj.aggregate_invoiced_plows


class DiscrepancyReview(admin.ModelAdmin, ExportMixin):
    model = WorkProxyServiceDiscrepancy
    resource_class=InvoiceResource
    list_filter = ('invoice__id',)
    list_display = [work_order, invoice, service_provider, location, deicing_rate, deicing_tax, plow_rate,
                    plow_tax, snowfall, storm_days, refreeze,
                    'number_salts', 'number_salts_predicted', 'salt_delta', 'number_plows', 'number_plows_predicted',
                    'push_delta', 'deice_cost_delta', 'plow_cost_delta']

    def number_salts(self, obj):
        return obj.aggregate_invoiced_salts

    def number_plows(self, obj):
        return obj.aggregate_invoiced_plows

    generated_discrept_dict = {}

    def number_salts_predicted(self, obj):
        import random
        random_salts = random.choice([0,1,1,3,2,1,2,1,2])
        random_plows = random.choice([0,2,1,1,2,1,2,1,2])
        self.generated_discrept_dict = {'num_salts_pred': random_salts, 'num_plows_pred': random_plows}
        return random_salts

    def number_plows_predicted(self, obj):
        import random
        return self.generated_discrept_dict['num_plows_pred']

    def snowfall(self, obj):
        import random
        snowfall = random.choice([0,1,1,3,2,1,2,1,2])
        return snowfall

    def salt_delta(self, obj):
        try:
            # pred = self.num_plows - 1
            delta = int(obj.number_salts) - int(self.generated_discrept_dict['num_salts_pred'])
            self.generated_discrept_dict['salt_delta'] = delta
            if delta > 0:
                return u'<div style = "background-color: red; color:white; font-weight:bold; text-align:center;" >{0}</div>'.format(delta)
            else:
                return 0
        except Exception as e:
            return ''

    salt_delta.allow_tags = True

    def push_delta(self, obj):
        try:
            # pred = self.num_plows - 1
            delta = int(obj.number_plows) - int(self.generated_discrept_dict['num_plows_pred'])
            self.generated_discrept_dict['push_delta'] = delta
            if delta > 0:
                return u'<div style = "background-color: red; color:white; font-weight:bold; text-align:center;" >{0}</div>'.format(delta)
            else:
                return 0
        except Exception as e:
            return ''

    push_delta.allow_tags = True

    def deice_cost_delta(self, obj):
        try:
            # pred = self.num_plows - 1
            deice_cost = float(self.generated_discrept_dict['salt_delta']) * (obj.building.deice_rate)
            deice_tax = obj.building.deice_tax
            delta = deice_cost + deice_tax
            self.generated_discrept_dict['deice_cost_delta'] = delta
            if delta > 0:
                return u'<div style = "background-color: red; color:white; font-weight:bold; text-align:center;" >{0}</div>'.format(delta)
            else:
                return 0
        except Exception as e:
            return ''

    deice_cost_delta.allow_tags = True

    def plow_cost_delta(self, obj):
        try:
            # pred = self.num_plows - 1
            plow_cost = float(self.generated_discrept_dict['plow_delta']) * float(obj.building.plow_rate)
            plow_tax = obj.building.plow_tax
            delta = plow_cost + plow_tax
            self.generated_discrept_dict['plow_cost_delta'] = delta
            if delta > 0:
                return u'<div style = "background-color: red; color:white; font-weight:bold; text-align:center;" >{0}</div>'.format(delta)
            else:
                return 0
        except Exception as e:
            return ''

    plow_cost_delta.allow_tags = True

@register(Building)
class BuildingAdmin(SuperuserModelAdmin):
    list_display = ['building_code', 'address', 'service_provider', 'weather_station', 'deice_rate', 'deice_tax', 'plow_rate', 'plow_tax', 'type']
    list_filter = ['service_provider', 'weather_station']
    search_fields = ['service_provider__name']


@register(WorkOrderIDSuperProxy)
class WorkOrderIDAdmin(SuperuserModelAdmin):
    list_display = ['work_order_code','vendor', 'available']
#
#
class RegionalManagerAdmin(SuperuserModelAdmin):
    list_display = ['name', 'system_user']
#
#
# @register(VendorSettings)
# class VendorSettingsAdmin(SuperuserModelAdmin):
#     list_display = ['const_a', 'const_b', 'vendor']
#
#
class VendorAdmin(SuperuserModelAdmin):
    list_display = ['name', 'address', 'system_user']
#
#
# @register(WorkOrder)
# class WorkOrderAdmin(SuperuserModelAdmin):
#     list_display = ['vendor', 'invoice', 'building', 'storm_name']
#     raw_id_fields = ("building",)
#
#
# @register(WorkVisit)
# class WorkVisitAdmin(SuperuserModelAdmin):
#     list_display = ['work_order', 'response_time_start', 'response_time_end']
#
#


def storm_date(obj):
    return obj.invoice.storm_date


def storm_name(obj):
    return obj.invoice.storm_name

# @register(SafetyReport)
# class SafetyReportAdmin(admin.ModelAdmin):
#     # list_filter = (storm_date, storm_date)
#     list_display = ['building', storm_name, storm_date, 'existing_work_order', 'site_serviced', 'safe_to_open', 'service_time']
#
#     def existing_work_order(self, obj):
#         existing_work_order = WorkOrder.objects.filter(invoice=obj.invoice, building=obj.building).exists()
#         return existing_work_order
#     existing_work_order.boolean = True


# @register(ModifiablePrelimInvoice)
# class ModifyPrelimInvoiceAdmin(admin.ModelAdmin):
#     # list_filter = (storm_date, storm_date)
#     list_filter = ['invoice_id', 'invoice__storm_name', 'invoice__storm_date', 'failed_service']
#     list_editable = ['building', 'last_service_date', 'num_plows', 'num_salts', 'failed_service']
#     list_display = ['id', 'building', service_provider, storm_name, storm_date, 'last_service_date',
#                     'num_plows', 'num_salts', 'failed_service']


#
#
# @register(DiscrepancyReport)
# class DiscrepancyReportAdmin(SuperuserModelAdmin):
#     list_display = ['work_order', 'author', 'message']
#
#
# @register(Invoice)
# class InvoiceAdmin(SuperuserModelAdmin):
#     list_display = ['vendor', 'remission_address']

@register(WeatherStationSuperProxy)
class WeatherStationSuperProxyAdmin(SuperuserModelAdmin):
    list_display = ['station_name', 'short_name', 'zip_code_list', 'nws_code', 'cst_reference']

    def zip_code_list(self, obj):
        return str(obj.zip_codes)