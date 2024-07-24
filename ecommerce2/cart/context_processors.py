from .models import Cart


def total(request):
    user = request.user
    count = 0
    if request.user.is_authenticated:
        try:
            item = Cart.objects.filter(user=user)
            count = item.count()
        except:
            count = 0
    return {'count':count}