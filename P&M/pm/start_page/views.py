from django.shortcuts import render, redirect
from .forms import Add_medcine, Add_synonyms, Add_literature
from .models import Medcine, Synonyms, General_sources
from django.utils import timezone
from django.db.models import Sum
from django.contrib import messages
from django.forms import inlineformset_factory
from django.views.generic import ListView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin


def index(request):
    recent_synonyms = Synonyms.objects.order_by("-pub_date")[:5]
    request_range = timezone.now() - timezone.timedelta(days=14)
    popular_medcines = Synonyms.objects.filter(request_counter__date__gt=request_range).annotate(
        sm=Sum("request_counter__count")).order_by("-sm")[:5]
    data = {"recent_synonyms": recent_synonyms, "popular_medcines": popular_medcines}
    return render(request, "start_page/start.html", context=data)


def search_medcine(request):
    medcine_name = request.GET.get("medcine_name")
    try:
        synonym = Synonyms.objects.get(comm_name=medcine_name.capitalize())
    except Synonyms.DoesNotExist:
        return render(request, "start_page/not_in_base.html",
                      context={'search_name': medcine_name})
    else:
        view, created = synonym.request_counter_set.get_or_create(synonym=synonym.id, date=timezone.now())
        view.count = view.count + 1
        view.save(update_fields=["count"])
        return redirect("start_page:search_param", synonym.url_name)


def search_param(request, url_name):
    try:
        synonym = Synonyms.objects.get(url_name=url_name)
    except Synonyms.DoesNotExist:
        return redirect("start_page:error")
    else:
        medcine = Medcine.objects.get(synonyms__url_name=url_name)
        all_synonyms = medcine.synonyms_set.all().exclude(url_name=url_name)
        general_sources = medcine.general_sources_set.all()
        data = {"medcine": medcine, "synonym": synonym, "all_synonyms": all_synonyms,
                "sources": general_sources}
        return render(request, "start_page/search.html", context=data)


@login_required
def create_medcine(request):
    # create synonym's form
    SynonymsFormSet = inlineformset_factory(Medcine, Synonyms, form=Add_synonyms, can_delete=False, extra=2)
    # create literatures form
    SourcesFormSet = inlineformset_factory(Medcine, General_sources, form=Add_literature, can_delete=False, extra=4)

    def add_forms(*args):
        add_synonyms = SynonymsFormSet(*args)
        add_medcine = Add_medcine(*args)
        add_sources = SourcesFormSet(*args)
        data = {'add_medcine': add_medcine, 'add_synonyms': add_synonyms, 'add_sources': add_sources}
        return render(request, "start_page/create_base.html", context=data)

    if request.method == 'POST':
        # new medcine add
        new_medcine = Add_medcine(request.POST, request.FILES)
        if new_medcine.is_valid():
            new_medcine.save()
            medcine_name = new_medcine.cleaned_data['international_name']
            medcine_object = Medcine.objects.get(international_name=medcine_name)
            medcine_object.general_url_name = medcine_name.lower().replace(" ", "").replace(",", "")[:10]
            medcine_object.save()
            synonyms_formset = SynonymsFormSet(request.POST, instance=medcine_object)
            sources_formset = SourcesFormSet(request.POST, instance=medcine_object)
            if sources_formset.is_valid() and synonyms_formset.is_valid():
                if sources_formset.cleaned_data:
                    sources_formset.save()
                if synonyms_formset.cleaned_data:
                    synonyms_formset.save()
                messages.add_message(request, messages.SUCCESS, "???????????? ??????????????????")
                return redirect('start_page:base')
            else:
                medcine_object.delete()
                return add_forms(request.POST, request.FILES)
        else:
            return add_forms(request.POST, request.FILES)
    else:
        return add_forms()


class UpdateBase(LoginRequiredMixin, ListView):
    model = Medcine
    template_name = "start_page/update_base.html"
    context_object_name = 'medcines'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "???????? ????????????"
        return context


@login_required
def update_medcine(request, general_url_name):
    SynonymsFormSet = inlineformset_factory(Medcine, Synonyms, form=Add_synonyms, can_delete=True, extra=3)
    SourcesFormSet = inlineformset_factory(Medcine, General_sources, form=Add_literature, can_delete=True, extra=3)
    medcine_object = Medcine.objects.get(general_url_name=general_url_name)

    def add_forms(*args):
        add_synonyms = SynonymsFormSet(*args, instance=medcine_object)
        add_medcine = Add_medcine(*args, instance=medcine_object)
        add_sources = SourcesFormSet(*args, instance=medcine_object)
        data = {'add_medcine': add_medcine, 'add_synonyms': add_synonyms, 'add_sources': add_sources}
        return render(request, "start_page/create_base.html", context=data)

    if request.method == 'POST':
        new_medcine = Add_medcine(request.POST, request.FILES, instance=medcine_object)
        if new_medcine.is_valid():
            new_medcine.save()
            medcine_name = new_medcine.cleaned_data['international_name']
            medcine_object.general_url_name = medcine_name.lower().replace(" ", "").replace(",", "")[:10]
            medcine_object.save()
            synonyms_formset = SynonymsFormSet(request.POST, instance=medcine_object)
            sources_formset = SourcesFormSet(request.POST, instance=medcine_object)
            if sources_formset.is_valid() and synonyms_formset.is_valid():
                if sources_formset.cleaned_data:
                    sources_formset.save()
                if synonyms_formset.cleaned_data:
                    synonyms_formset.save()
                messages.add_message(request, messages.SUCCESS, "???????????? ??????????????????")
                return redirect('start_page:update')
            else:
                return add_forms(request.POST, request.FILES)
        else:
            return add_forms(request.POST, request.FILES)
    else:
        return add_forms()


class DeleteMedcine(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Medcine
    success_url = reverse_lazy('start_page:update')
    success_message = "???????????? ??????????????"
    template_name = 'start_page/medicine_confirm_delete.html'
    context_object_name = 'medicine'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '???????????????? ????????????'
        return context


