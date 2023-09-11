from django.http import JsonResponse
from django.forms.models import model_to_dict
from chatuser.models import ChatUser, UserInterest


## Temporary 
def api_home(request):
    users = ChatUser.objects.all()

    res = {}
    for user in users:
        user_interests = UserInterest.objects.filter(user=user)
        interests_data = [model_to_dict(interest, fields=['interest', 'preference_score']) for interest in user_interests]

        user_data = model_to_dict(user, fields=['id', 'name', 'age'])
        user_data['interests'] = interests_data

        res[user.name] = (user_data)
    # response = model_to_dict(user, fields=['id', 'name', 'age' ])
    # response += model_to_dict(user_interests)

    
    return JsonResponse(res, safe=False)
    # pass

    
