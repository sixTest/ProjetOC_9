from django import template

register = template.Library()


def rating_stars(rating):
    return rating*[True] + (5-rating)*[False]


def rating_champs(rating):
    return [i+1 for i in range(rating+1)]


register.filter('rating_stars', rating_stars)
register.filter('rating_champs', rating_champs)
