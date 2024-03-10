from .models import teamdata,member



check = member.objects.filter(teamid="jrm")

print(check)