from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.shortcuts import render

from onsite.models import Checkin
from user.models import teamdata


def onsite_checkin_view(request):
    # Fetch all teams
    teams = teamdata.objects.all()
    for team in teams:
        try:
            checkin = Checkin.objects.get(team=team)
            team.checkin = checkin
        except Checkin.DoesNotExist:
            # If no check-in object is found, assign None to team.checkin
            team.checkin = None

    # Pass the teams to the template for rendering
    return render(request, 'checkin_list.html', {'teams': teams})


def submit_checkin(request):
    if request.method == 'POST':
        team_id = request.POST.get('team_id')
        annexure1 = request.POST.get('annexure1') == 'on'
        annexure2 = request.POST.get('annexure2') == 'on'
        annexure3 = request.POST.get('annexure3') == 'on'
        faculty_accompanied = request.POST.get('faculty_accompanied') == 'on'
        team_members_present = request.POST.get('team_members_present')

        try:
            team = get_object_or_404(teamdata, id=team_id)
        except ValueError:
            return JsonResponse({'success': False, 'error': ('Invalid team ID.')})




        try:
            checkin = Checkin.objects.filter(team=team).first()
            checkin.annexure1 = annexure1
            checkin.annexure2 = annexure2
            checkin.annexure3 = annexure3
            checkin.faculty_accompanied = faculty_accompanied
            checkin.team_members_present = team_members_present if isinstance(team_members_present,int) else 0

            checkin.save()
        except:
            checkin = Checkin.objects.create(team=team, annexure1=annexure1, annexure2=annexure2, annexure3=annexure3,
                                             faculty_accompanied=faculty_accompanied,
                                             team_members_present=team_members_present)

        return  redirect('/onsite/checkin')
    else:
        return JsonResponse({'success': False, 'error': _('Invalid request method.')})