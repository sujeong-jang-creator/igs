from django.shortcuts import render
from .models import Results
from django.core.paginator import Paginator
from django.views.generic import ListView

class PostListView(ListView):
    template_name = "grading/total_distinguish.html"
    model = Results
    paginate_by = 7

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
    model = Results
    paginate_by = 7

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

# def detail_distinguish(request):
#     return render(request, 'grading/detail_distinguish.html')

'''
def grade_table(request):
    result = Results.objects.all()
    # 페이지 처리 시작
    paginator = Paginator(result, 5)
    page = int(request.Get.get('page', 1))
    page_obj = paginator.page(page)
    # 페이지 처리 끝
    print(result)

    # response = render(request, "iguessso_app/total_distinguish.html",{"result":result})
    response = render(request, "grading/total_distinguish.html",{"page_obj":page_obj})
    return response
'''