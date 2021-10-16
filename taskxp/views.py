from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .forms import TarefaForm
from django.contrib import messages
import datetime
from .models import Tarefaxp


@login_required
def taskList(request):
    search = request.GET.get('search')
    filter = request.GET.get('filter')
    tasksDoneRecently = Tarefaxp.objects.filter(done='done', update_at__gt=datetime.datetime.now()-datetime.timedelta(days=30)).count()
    tasksDone = Tarefaxp.objects.filter(done='done', user=request.user).count()
    tasksDoing = Tarefaxp.objects.filter(done='doing', user=request.user).count()

    if search:

        taskxp = Tarefaxp.objects.filter(done=filter, user=request.user)
    
    elif filter:
        taskxp = Tarefaxp.objects.filter(done=filter, user=request.user)
    else:

        taskxp_list = Tarefaxp.objects.all().order_by('-created_at').filter(user=request.user) #organiza por ordem de criação
        paginator = Paginator(taskxp_list, 3)
        page = request.GET.get('page')
        taskxp = paginator.get_page(page)

    return render(request, 'taskxp/list.html', {'taskxp': taskxp,'tasksrecently': tasksDoneRecently, 'tasksdone': tasksDone, 'tasksdoing': tasksDoing })

@login_required
def taskView(request, id):
    task = get_object_or_404(Tarefaxp, pk=id)       #pk é primary key
    return render(request, 'taskxp/task.html',{'task':task})
@login_required
def newTask(request):
    if request.method =='POST':
        form = TarefaForm(request.POST)

        if form.is_valid():
            tarefa = form.save(commit = False)
            tarefa.done = 'doing'
            tarefa.user = request.user
            tarefa.save()
            return redirect('/')
    else:
        form = TarefaForm()
        return render(request, 'taskxp/addtask.html', {'form':form})
@login_required
def editTask(request, id):
    tarefaxp = get_object_or_404(Tarefaxp, pk=id)
    form = TarefaForm(instance=tarefaxp)

    if(request.method == 'POST'):
        form = TarefaForm(request.POST, instance=tarefaxp)

        if(form.is_valid()):
            tarefaxp.save()
            return redirect('/')
    else:
        return render(request, 'taskxp/edittask.html', {'form': form, 'tarefa': tarefaxp})
@login_required
def deleteTask(request, id):
     tarefaxp = get_object_or_404(Tarefaxp, pk=id)
     tarefaxp.delete()

     messages.info(request, 'Essa tarefa foi deletada com sucesso.')  #tem varios tipos de mensagem, nesse caso é a classe info

     return redirect('/')

@login_required
def changeStatus(request, id):
    task = get_object_or_404(Tarefaxp, pk=id)

    if(task.done == 'doing'):
        task.done = 'done'
    else:
        task.done = 'doing'
    
    task.save()

    return redirect('/')

def helloWorld(request):
    return HttpResponse('Hello World!')

    #view sempre retorna algo


def yourName(request, name):
    return render(request, 'taskxp/yourname.html', {'name':name})

    