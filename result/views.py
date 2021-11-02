from django.shortcuts import redirect, render
from upload.models import Results
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
import os

def show_result(request, result_pk):
    print("넘어온 pk : ", result_pk)
    data = Results.objects.get(pk=result_pk)
    if request.method == "GET":
        return render(request, 'result/show_result.html', {'result' : data})
    else:
        if True:
            return redirect('/')

def revision(request, result_pk):
    if request.method == "GET":
        data = Results.objects.get(pk=result_pk)
        return render(request, 'result/revision.html', {'result' : data})
    else:
        choice_grade = request.POST.get('grade')
        result_id = request.POST.get('result_id')
        
        if True:
            update = Results.objects.get(pk = result_pk)
            update.modified_grade=choice_grade
            update.save()

            DATASET_SAVE_PATH = 'dataset'
            text_name = str(result_pk) + ".txt"
            TEXT_SAVE_PATH = os.path.join(DATASET_SAVE_PATH, text_name)
            print(TEXT_SAVE_PATH)

            with open(TEXT_SAVE_PATH,"rt") as f:
                lines = f.readlines()
                print(type(lines))
                print(lines[0])
                origin_split_lines = lines[0].split(" ")
                split_lines = lines[0].split(" ")
                print(split_lines)
                if choice_grade == "1++":
                    new_label = 0
                elif choice_grade == "1+":
                    new_label = 1
                elif choice_grade == "1":
                    new_label = 2
                elif choice_grade == "2":
                    new_label = 3
                elif choice_grade == "3":
                    new_label = 4

                split_lines[0] = str(new_label)
                print(split_lines)
                
                new_lines = ' '.join(split_lines)
                print(new_lines)
                with open(TEXT_SAVE_PATH,"wt") as wf:
                    wf.writelines(new_lines)

            return redirect('/')
            