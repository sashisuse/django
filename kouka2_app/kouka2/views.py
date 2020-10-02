from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Kouka2
from .forms import Kouka2Form
from .forms import FindForm
from django.db.models import Count,Sum,Avg,Min,Max
from django.core.paginator import Paginator


def index(request, num=1):
  data = Kouka2.objects.all()
  page = Paginator(data, 3)
  re1 = Kouka2.objects.aggregate(Count('price'))
  re2 = Kouka2.objects.aggregate(Sum('price'))
  re3 = Kouka2.objects.aggregate(Avg('price'))
  re4 = Kouka2.objects.aggregate(Min('price'))
  re5 = Kouka2.objects.aggregate(Max('price'))
  msg = '項目数：' + str(re1['price__count']) \
      + '<br>価格合計：' + str(re2['price__sum']) \
      + '<br>価格平均：' + str(re3['price__avg']) \
      + '<br>価格最小値：' + str(re4['price__min']) \
      + '<br>価格最大値：' + str(re5['price__max'])

  params = {
    'title': '農産物商品検索',
    'message': msg,
    'data': page.get_page(num),
  }
  return render(request, 'kouka2/index.html', params)

def create(request):
  if (request.method == 'POST'):
    obj = Kouka2()
    kouka2 = Kouka2Form(request.POST, instance=obj)
    kouka2.save()
    return redirect(to='/kouka2')
  params = {
    'title': '農産物商品検索',
    'form': Kouka2Form(),
  }
  return render(request, 'kouka2/create.html', params)

def edit(request, num):
  obj = Kouka2.objects.get(id=num)
  if (request.method == 'POST'):
    kouka2 = Kouka2Form(request.POST, instance=obj)
    kouka2.save()
    return redirect(to='/kouka2')
  params = {
    'title': '農産物商品検索',
    'id':num,
    'form': Kouka2Form(instance=obj),
  }
  return render(request, 'kouka2/edit.html', params)

def delete(request, num):
    kouka2 = Kouka2.objects.get(id=num)
    if (request.method == 'POST'):
        kouka2.delete()
        return redirect(to='/kouka2')
    params = {
        'title': '農産物商品検索',
        'id':num,
        'obj': kouka2,
    }
    return render(request, 'kouka2/delete.html', params)

def find(request):
    if (request.method == 'POST'):
        form = FindForm(request.POST)
        # find = request.POST['find']
        # val = find.split()
        # data = Kouka2.objects.filter(price__gte=val[0], price__lte=val[1])  #☆
        # msg = '検索語: ' + str(data.count())
        msg = request.POST['find']
        sql = 'select * from kouka2_kouka2'
        if (msg != ' '):
            sql += ' where ' + msg
        data = Kouka2.objects.raw(sql)
        msg = sql
    else:
        msg = '検索...'
        form = FindForm()
        data =Kouka2.objects.all()
    params = {
        'title': '農産物商品検索',
        'message': msg,
        'form':form,
        'data':data,
    }
    return render(request, 'kouka2/find.html', params)


def check(request):
    params = {
        'title': '農産物商品検索',
        'message':'バリデーションチェック',
        'form': Kouka2Form(),
    }
    if (request.method == 'POST'):
        form = Kouka2Form(request.POST)
        params['form'] = form
        if (form.is_valid()):
            params['message'] = '問題ありません'
        else:
            params['message'] = '入力データに問題があります'
    return render(request, 'kouka2/check.html', params)



