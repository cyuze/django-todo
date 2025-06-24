
from django.shortcuts import render, get_object_or_404
from django.views import View # クラスベースビューを継承するのに必要
from .models import Task
from .forms import TaskForm
from django.shortcuts import redirect

# Create your views here.
class IndexView(View):
    def get(self, request):
        completed_tasks = Task.objects.filter(complete=True).order_by('-end_date')
        incomplete_tasks = Task.objects.filter(complete=False).order_by('end_date')
        return render(request, "mytodo/index.html", {
            "completed_tasks": completed_tasks,
            "incomplete_tasks": incomplete_tasks,
        })

# ビュークラスをインスタンス化
index = IndexView.as_view()

class AddView(View):
    def get(self, request):
        form = TaskForm()
        # テンプレートのレンダリング処理
        return render(request, "mytodo/add.html", {'form': form, 'flag': True})
    
    def post(self, request, *args, **kwargs):
        # 登録処理
        # 入力データをフォームに渡す
        form = TaskForm(request.POST)
        # 入力データに誤りがないかチェック
        is_valid = form.is_valid()

        # データが正常であれば
        if is_valid:
            # モデルに登録
            form.save()
            return redirect('/')

        # データが正常じゃない
        return render(request, 'mytodo/add.html', {'form': form})
    
add = AddView.as_view()

class Update_task_complete(View):
    def post(self, request, *args, **kwargs):
        task_id = request.POST.get('task_id')

        task = Task.objects.get(id=task_id)
        task.complete = not task.complete
        task.save()

        return redirect('/')
        
 
update_task_complete = Update_task_complete.as_view()
            
class UpdateView(View):
    def get(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(instance=task)
        return render(request, "mytodo/add.html", {"form": form})

    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("/")
        return render(request, "mytodo/add.html", {"form": form})

update = UpdateView.as_view()

class DeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(instance=task)
        return render(request, "mytodo/delete.html", {"form": form})

    def post(self, request, pk, *args, **kwargs):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect("/")

delete = DeleteView.as_view()
    