from django import template

register = template.Library()


@register.filter()
def mymedia(val):
    if val:
        return f"/media/{val}"
    else:
        return f"/media/no-image.png"


@register.filter()
def get_avatar(val):
    if val:
        return f"/media/{val}"
    else:
        return f"/media/users/noname.jpg"
