from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import InscriptionForm, ConnectionForm, CreationTicketForm, CreationReviewForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value
from itertools import chain
from .models import Ticket, Review, UserFollows


def login_view(request):
    form = ConnectionForm()
    context = {'form': form}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return flux(request)
        else:
            context['errors'] = 'Les informations sont incorrecte.'
    template = loader.get_template('LITReview/login/login.html')
    return HttpResponse(template.render(context, request=request))


def logout_view(request):
    logout(request)
    form = ConnectionForm()
    context = {'form': form}
    template = loader.get_template('LITReview/login/login.html')
    return HttpResponse(template.render(context, request=request))


def inscription(request):
    form = InscriptionForm()
    context = {'form': form}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user = User.objects.filter(username=username)
        if user.exists():
            context['errors'] = 'Il existe deja un nom comme celui-ci !'
        elif password != confirm_password:
            context['errors'] = 'La confirmation du mot de passe a échoué.'
        else:
            form = ConnectionForm()
            context = {'form': form}
            User.objects.create_user(username=username, password=password)
            template = loader.get_template('LITReview/login/login.html')
            return HttpResponse(template.render(context, request=request))

    template = loader.get_template('LITReview/inscription/inscription.html')
    return HttpResponse(template.render(context, request=request))


@login_required
def flux(request):
    user = User.objects.filter(username=request.user.username)
    users_followed = [user_followed.followed_user for user_followed in UserFollows.objects.filter(user=user[0])]
    user_tickets = Ticket.objects.filter(user=user[0]).annotate(content_type=Value('MY_TICKET', CharField()))
    user_reviews = Review.objects.filter(user=user[0]).annotate(content_type=Value('MY_REVIEW', CharField()))

    users_followed_tickets = []
    users_followed_reviews = []
    for user_followed in users_followed:
        users_followed_tickets.extend(Ticket.objects.filter(user=user_followed).annotate(
            content_type=Value('TICKET', CharField())))
        users_followed_reviews.extend(Review.objects.filter(user=user_followed).annotate(
            content_type=Value('REVIEW', CharField())))

    for ticket in chain(user_tickets, users_followed_tickets):
        if Review.objects.filter(ticket=ticket, user__in=chain(users_followed, user)):
            ticket.review_exists = True

    user_answered_tickets_reviews = Review.objects.filter(ticket__user=user[0]).annotate(
        content_type=Value('REVIEW', CharField()))
    reviews = set(chain(user_reviews, users_followed_reviews, user_answered_tickets_reviews))
    tickets = chain(user_tickets, users_followed_tickets)
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'LITReview/flux/flux.html', context={
        'header': render_to_string('LITReview/header/header.html'),
        'posts': posts})


@login_required
def creation_ticket(request):
    context = {'header': render_to_string('LITReview/header/header.html')}
    if request.method == 'POST':
        form = CreationTicketForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title_ticket']
            description = form.cleaned_data['description']
            user = User.objects.filter(username=request.user.username)
            image = form.cleaned_data['image']
            Ticket(title=title, description=description, user=user[0], image=image).save()
            return flux(request)
        else:
            context['errors'] = 'Certain champs sont invalides.'

    context['form'] = CreationTicketForm()
    template = loader.get_template('LITReview/ticket/creation_ticket.html')
    return HttpResponse(template.render(context, request=request))


@login_required
def creation_review_without_ticket(request):
    context = {'header': render_to_string('LITReview/header/header.html')}
    if request.method == 'POST':
        form_ticket = CreationTicketForm(request.POST, request.FILES)
        form_review = CreationReviewForm(request.POST, request.FILES)
        if form_ticket.is_valid() and form_review.is_valid():
            user = User.objects.filter(username=request.user.username)
            title_ticket = form_ticket.cleaned_data['title_ticket']
            description_ticket = form_ticket.cleaned_data['description']
            image = form_ticket.cleaned_data['image']
            title_review = form_review.cleaned_data['title_review']
            rating = int(request.POST.get('inlineRadioOptions'))
            comment_review = form_review.cleaned_data['comment']
            ticket = Ticket(title=title_ticket, description=description_ticket, user=user[0], image=image)
            ticket.save()
            Review(ticket=ticket, rating=rating, headline=title_review, body=comment_review, user=user[0]).save()
            return flux(request)
        else:
            context['errors'] = 'Certain champs sont invalides.'

    context['form_ticket'] = CreationTicketForm()
    context['form_review'] = CreationReviewForm()
    template = loader.get_template('LITReview/review/creation_review_without_ticket.html')
    return HttpResponse(template.render(context, request=request))


@login_required
def creation_review(request):
    context = {'header': render_to_string('LITReview/header/header.html')}
    if request.method == 'GET':
        ticket = Ticket.objects.get(id=request.GET['id_ticket'])
        form_review = CreationReviewForm()
        context['form_review'] = form_review
        context['ticket'] = ticket
        context['id_ticket'] = request.GET['id_ticket']
        template = loader.get_template('LITReview/review/creation_review.html')
        return HttpResponse(template.render(context, request=request))
    else:
        ticket = Ticket.objects.get(id=request.GET['id_ticket'])
        user = User.objects.filter(username=request.user.username)
        title_review = request.POST.get('title_review')
        rating = int(request.POST.get('inlineRadioOptions'))
        comment_review = request.POST.get('comment')
        Review(ticket=ticket, rating=rating, headline=title_review, body=comment_review, user=user[0]).save()
        return flux(request)


@login_required
def posts(request):
    if 'delete_id_ticket' in request.GET:
        Ticket.objects.get(id=request.GET['delete_id_ticket']).delete()
    elif 'delete_id_review' in request.GET:
        review = Review.objects.get(id=request.GET['delete_id_review'])
        if review.user == review.ticket.user:
            review.ticket.delete()
        review.delete()

    user = User.objects.filter(username=request.user.username)
    reviews = Review.objects.all().filter(user=user[0])
    tickets = Ticket.objects.all().filter(user=user[0])
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'LITReview/posts/posts.html', context={
        'header': render_to_string('LITReview/header/header.html'),
        'posts': posts})


@login_required
def following(request):
    context = {'header': render_to_string('LITReview/header/header.html')}
    template = loader.get_template('LITReview/following/following.html')
    user = User.objects.filter(username=request.user.username)
    if request.method == 'POST':
        user_followed = User.objects.filter(username=request.POST.get('follow'))
        if user_followed.exists():
            if user_followed[0].username != user[0].username:
                if user_followed[0].username not in [u.followed_user.username for
                                                     u in UserFollows.objects.filter(user=user[0])]:
                    UserFollows(user=user[0], followed_user=user_followed[0]).save()
                else:
                    context['errors'] = 'Vous suivez déja cette utilisateur.'
            else:
                context['errors'] = 'Vous ne pouvez pas vous suivre.'
        else:
            context['errors'] = "L'utilisateur est inconnue."
    else:
        if 'unfollow' in request.GET:
            user_followed = User.objects.filter(username=request.GET['unfollow'])
            UserFollows.objects.all().filter(followed_user=user_followed[0]).delete()

    user_following = UserFollows.objects.all().filter(user=user[0])
    user_followed = UserFollows.objects.all().filter(followed_user=user[0])
    context['followed'] = user_following
    context['following'] = user_followed
    return HttpResponse(template.render(context, request=request))


@login_required
def modification_ticket(request):
    context = {'header': render_to_string('LITReview/header/header.html')}
    if request.method == 'POST':
        form = CreationTicketForm(request.POST, request.FILES)
        if form.is_valid():
            title_ticket = form.cleaned_data['title_ticket']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']
            ticket = Ticket.objects.get(pk=request.GET['id'])
            ticket.title = title_ticket
            ticket.description = description
            if image:
                ticket.image = image
            ticket.save()
            return posts(request)
        else:
            context['errors'] = 'Certain champs sont invalides.'
    id_ticket = request.GET['id']
    ticket = Ticket.objects.get(id=id_ticket)
    context['form'] = CreationTicketForm(initial={'title_ticket': ticket.title, 'description': ticket.description})
    context['ticket'] = ticket
    context['id_ticket'] = id_ticket
    template = loader.get_template('LITReview/ticket/modification_ticket.html')
    return HttpResponse(template.render(context, request=request))


@login_required
def modification_review(request):
    context = {'header': render_to_string('LITReview/header/header.html')}
    if request.method == 'POST':
        title_review = request.POST.get('title_review')
        rating = int(request.POST.get('inlineRadioOptions'))
        comment = request.POST.get('comment')
        Review.objects.all().filter(id=request.GET['id']).update(headline=title_review, rating=rating, body=comment)
        return posts(request)
    else:
        id_review = request.GET['id']
        review = Review.objects.get(id=id_review)
        context['form_review'] = CreationReviewForm(initial={'title_review': review.headline, 'comment': review.body})
        context['review'] = review
        context['id_review'] = id_review
        template = loader.get_template('LITReview/review/modification_review.html')
    return HttpResponse(template.render(context, request=request))
