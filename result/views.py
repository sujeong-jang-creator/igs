from django.shortcuts import redirect, render
from upload.models import Results
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder

def show_result(request, pk):
    data = Results.objects.get(result_id=pk)
    if request.method == "GET":
        return render(request, 'result/show_result.html', {'result' : data})
    else:
        if True:
            return redirect('/')

def revision(request, pk):
    if request.method == "GET":
        data = Results.objects.get(result_id=pk)
        return render(request, 'result/revision.html', {'result' : data})
    else:
        choice_grade = request.POST.get('grade')
        result_id = request.POST.get('result_id')
        
        if True:
            update = Results.objects.get(result_id=pk)
            update.modified_grade=choice_grade
            update.save()
            return redirect('/')
            