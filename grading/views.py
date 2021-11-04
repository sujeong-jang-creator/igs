from typing import Counter
from django.shortcuts import render

from account.models import User
from upload.models import Results
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.contrib.auth import get_user


class PostListView(ListView):
    template_name = "grading/total_distinguish.html"
    model = Results
    paginate_by = 7

    def get_queryset(self):
        return Results.objects.filter(user_id=get_user(self.request).pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_group_count = 5
        current_page =  int(self.request.GET.get('page', 1))

        start_idx = int((current_page-1)/page_group_count)*page_group_count
        end_idx = start_idx + page_group_count
        page_range = paginator.page_range[start_idx:end_idx]

        start_page = paginator.page(page_range[0])
        end_page = paginator.page(page_range[-1])

        has_previous = start_page.has_previous()
        has_next = end_page.has_next()

        context['page_range'] = page_range
        if has_previous:
            context['has_previous'] = has_previous
            context['previous_page_no'] = start_page.previous_page_number()
        
        if has_next:
            context['has_next'] = has_next
            context['next_page_no'] = end_page.next_page_number()

        return context


class PostListView2(ListView):
    template_name = "grading/detail_distinguish.html"
    paginate_by = 7

    def get_queryset(self):
        return Results.objects.filter(user_id=get_user(self.request).pk).order_by('-register_date')

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)

        paginator = context['paginator']
        page_group_count = 5
        current_page =  int(self.request.GET.get('page', 1))

        start_idx = int((current_page-1)/page_group_count)*page_group_count
        end_idx = start_idx + page_group_count
        page_range = paginator.page_range[start_idx:end_idx]

        start_page = paginator.page(page_range[0])
        end_page = paginator.page(page_range[-1])

        has_previous = start_page.has_previous()
        has_next = end_page.has_next()

        context['page_range'] = page_range
        if has_previous:
            context['has_previous'] = has_previous
            context['previous_page_no'] = start_page.previous_page_number()
        
        if has_next:
            context['has_next'] = has_next
            context['next_page_no'] = end_page.next_page_number()

        return context

def show_detail(request, result_pk):
    data = Results.objects.get(pk=result_pk)

    return render(request, 'grading/show_detail.html', {'result' : data})
