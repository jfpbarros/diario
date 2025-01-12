from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Pessoa, Diario, Tag
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import Count

def home(request):
    textos = Diario.objects.all().order_by('-create_at')[:3]

    pessoas = Pessoa.objects.all()
    nomes = [pessoa.nome for pessoa in pessoas]
    
    # pessoas_com_contagem = Pessoa.objects.annotate(qtd_diarios=Count('diario'))
    
    # qtds = [pessoa.qtd_diarios for pessoa in pessoas_com_contagem]
    
    qtds=[]
    for pessoa in pessoas:
        qtd=Diario.objects.filter(pessoas=pessoa).count()
        qtds.append(qtd)

    ntags=[]
    otags = Tag.objects.all()
    ntags = [tag.nome for tag in otags]
    
    for tag in otags:
        resultados = Diario.objects.values('tags').annotate(total=Count('tags'))
        
        ttags = [tag['total'] for tag in resultados]
            #print(f"Tag: {n['tags']}, Total: {n['total']}")
        #Criar uma unica chave chamada dadostag..
    dadostag = (ntags, ttags)

    import json

    return render(request, 'home.html', {
        'textos': textos,
        'nomes': nomes,
        'qtds': qtds,
        'dadostag': json.dumps({'tags': ntags, 'totals': ttags})
    })


    #return render(request, 'home.html', {'textos': textos, 'nomes':nomes, 'qtds':qtds, 'dadostag':dadostag}) #render rtransforma o html em um arquivo para o usuário acessar

def escrever(request):

    if request.method =="GET":
        objs = Pessoa.objects.all()    
        tags = Tag.objects.all()
        return render(request, 'escrever.html', {'pessoas': objs , 'tags': tags }) #o terceiro parametro é para eu chamar dentro do HTML, através da chave que eu defini entr chaves.
    elif request.method == "POST":
        titulo = request.POST.get('titulo')
        tags = request.POST.getlist('tags')
        pessoas = request.POST.getlist('pessoas')
        texto = request.POST.get('texto')

        if len(titulo.strip()) == 0 or len(texto.strip()) == 0: #strip remove caracteres em branco
            messages.error(request, 'Preencha todos os campos!')            
            # objs = Pessoa.objects.all()
            # return render(request, 'escrever.html', {'pessoas': objs, 'titulo': titulo, 'texto': texto})
        
        obj = Diario(
            titulo = titulo,
            texto = texto
        )

        obj.set_tags(tags)

        obj.save()

        # for i in pessoas:
        #     pessoa = Pessoa.objects.get(id=i)
        #     obj.pessoas.add(pessoa)

        pessoas_objs = Pessoa.objects.filter(id__in=pessoas)
        obj.pessoas.add(*pessoas_objs)

        messages.success(request, 'Registro no diário incluído com sucesso!')
        return redirect('escrever')
    
def cadastrar_pessoa(request):
    if request.method == "GET":
        return render(request, 'pessoa.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        foto = request.FILES.get('foto')

        obj = Pessoa(
            nome = nome, 
            foto = foto
        )

        obj.save()
        return redirect('escrever')

    
def dia(request):
    data = request.GET.get('data')

    if data is None:
        messages.error(request, 'Data vazia!')
        return redirect('escrever')

    data_f = datetime.strptime(data, '%Y-%m-%d')
    diarios = Diario.objects.filter(create_at__gte=data_f).filter(create_at__lte=data_f + timedelta(days=1))

    return render(request, 'dia.html', {'diarios': diarios, 'total': diarios.count(), 'data': data})

def excluir_dia(request):
    dia = datetime.strptime(request.GET.get('data'), '%Y-%m-%d')
    diarios = Diario.objects.filter(create_at__gte=dia).filter(create_at__lte=dia + timedelta(days=1))

    diarios.delete()

    messages.success(request, 'Diarios exluídos com sucesso!')
    return redirect('escrever')

def manter_tag(request):
    if request.method == "GET":
    
        objs = Tag.objects.all()
        return render(request, 'manter_tag.html', {'tags': objs})
    
    elif request.method == "POST": 

        codigo = request.POST.get('codigo')
        nome = request.POST.get('nome')

        if len(codigo.strip()) == 0 or len(nome.strip()) == 0: #strip remove caracteres em branco
            messages.error(request, 'Preencha todos os campos!') 

        obj = Tag(
            codigo = codigo,
            nome = nome 
        )

        obj.save()
        messages.success(request, 'Tag incluída com sucesso')
        return redirect('manter_tag')
    
