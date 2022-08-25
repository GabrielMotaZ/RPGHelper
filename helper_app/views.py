from unicodedata import name
from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect, reverse
from helper_app.models import Characters, Skills, Rooms
from helper_app.forms import UserForm, RegisterForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_auth
from django.contrib.auth import logout as logout_account
from django.contrib.auth.models import User
from django.utils import timezone

# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return render(request, 'charSelect.html', {'charList': Characters.objects.filter(owner=User.objects.all().get(username=request.user.username))})
    return render(request, 'login.html', {})

def validate(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login_auth(request, user)
            return render(request, 'charSelect.html', {'charList': Characters.objects.filter(owner=user)})
        else:
            return render(request, 'login.html', {'error': 'Senha ou login incorreto'})

def select(request):
    return render(request, 'charSelect.html', {'charList': Characters.objects.filter(owner=User.objects.all().get(username=request.user.username))})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
            user.save()
            return render(request, 'registerComplete.html', {})
        else:
            return HttpResponse('nome invalido')
    else:
        return render(request, 'register.html', {})

def logout(request):
    if request.user.is_authenticated:
        logout_account(request)
    return render(request, 'login.html', {})

def test(request):
    if request.method == 'POST':
        return HttpResponse("personagem={}, skill={}, novo resultado={}".format(request.POST['character'], request.POST['skill'], request.POST['new_result']))

def editSkill(request):
    if request.method == 'POST':
        characterName = request.POST['static_character_name']
        toEditSkill = request.POST['skill']
        newResult = request.POST['new_result']
        account = get_object_or_404(User, username=request.user.username)
        character = account.characters_set.get(character_name=characterName)
        skill = character.skills_set.get(skill_name=toEditSkill)
        skill.results = newResult
        skill.save()
        room_name = request.session['room_name']
        character = account.characters_set.get(character_name=request.session['choice'])
        return render(request, 'index.html', {'room_name': room_name, 'character': character, 'skills': character.skills_set.all()})

def createSkill(request):
    if request.method == 'POST':
        account = get_object_or_404(User, username=request.user.username)
        characterName = account.characters_set.get(character_name=request.POST['static_character_name'])
        newSkillName = request.POST['skill_name']
        newResult = request.POST['results']
        try:
            obj = characterName.skills_set.get(skill_name=newSkillName)
            return HttpResponse('nome invalido')
        except:
            newSkill = Skills.objects.create(character=characterName, skill_name=newSkillName, results=newResult)
            newSkill.save()
            room_name = request.session['room_name']
            character = account.characters_set.get(character_name=request.session['choice'])
            return render(request, 'index.html', {'room_name': room_name, 'character': character, 'skills': character.skills_set.all()})

def deleteSkill(request):
    if request.method == 'POST':
        characterName = request.POST['static_character_name']
        toEditSkill = request.POST['skill']
        account = get_object_or_404(User, username=request.user.username)
        character = account.characters_set.get(character_name=characterName)
        skill = character.skills_set.get(skill_name=toEditSkill)
        skill.delete()
        room_name = request.session['room_name']
        character = account.characters_set.get(character_name=request.session['choice'])
        return render(request, 'index.html', {'room_name': room_name, 'character': character, 'skills': character.skills_set.all()})

def createChar(request):
    if request.method == 'POST':
        account = get_object_or_404(User, username=request.user.username)
        characterName = request.POST['charName']
        char = Characters.objects.create(owner=account, character_name=characterName)
        char.save()
        return select(request)

def enterRoom(request):
    if request.method == 'POST':
        account = get_object_or_404(User, username=request.user.username)
        character = account.characters_set.get(character_name=request.POST['choice'])
        room_name = request.POST['room-name'].strip()
        room_password = request.POST['room-password']
        if Rooms.objects.filter(name=room_name, password=room_password).exists():
            request.session['room_name'] = room_name
            request.session['choice'] = request.POST['choice']
            return render(request, 'index.html', {'room_name': room_name, 'character': character, 'skills': character.skills_set.all()})
        else:
            return render(request, 'charSelect.html', {'charList': Characters.objects.filter(owner=User.objects.all().get(username=request.user.username)),'error':'Room was not found with this name and password'})

def createRoom(request):
    if request.method == 'POST':
        account = get_object_or_404(User, username=request.user.username)
        character = account.characters_set.get(character_name=request.POST['choice'])
        room_name = request.POST['room-name'].strip()
        try:
            room = Rooms.objects.get(name=room_name)
        except:
            pass
        if room == False or timezone.now() > room.expirationDate:
            Rooms.objects.update_or_create(
                name=room_name,
                defaults={'password':request.POST['room-password'],
                'expirationDate':timezone.now()})
            return render(request, 'index.html', {'room_name': room_name, 'character': character, 'skills': character.skills_set.all()})
        else:
            return render(request, 'charSelect.html', {'charList': Characters.objects.filter(owner=User.objects.all().get(username=request.user.username)),'error':'This room is already being used'})
