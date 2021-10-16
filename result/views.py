from django.shortcuts import redirect, render
from grading.models import Results
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder

def result(request, pk):
    data = Results.objects.get(result_id=pk)
    if True:
        return render(request, 'result.html', {'result' : data})

def revision(request, pk):
    if request.method == "GET":
        data = Results.objects.get(result_id=pk)
        return render(request, 'revision.html', {'result' : data})
    else:
        choice_grade = request.POST.get('grade')
        result_id = request.POST.get('result_id')
        
        if True:
            update = Results.objects.get(result_id=pk)
            update.modified_grade=choice_grade
            update.save()
            return redirect('/')