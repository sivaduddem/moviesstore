#views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Petition
from .forms import PetitionForm


def index(request):
    """Render a list of petitions ordered newest first.

    The template expects `template_data` with `title` and `petitions`.
    """
    petitions = Petition.objects.all().order_by('-created_at') 
    template_data = {'title': 'Petitions', 'petitions': petitions}
    return render(request, 'petitions/index.html', {'template_data': template_data})


def show(request, petition_id):
    """Render a single petition's detail view by id."""
    petition = get_object_or_404(Petition, id=petition_id)
    template_data = {'title': petition.title, 'petition': petition}
    return render(request, 'petitions/show.html', {'template_data': template_data})


@login_required
def create(request):
    """Allow logged-in users to create a petition via GET/POST.

    GET: show empty form. POST: validate and save with the current user as creator.
    """
    if request.method == 'GET':
        return render(request, 'petitions/create.html', {'template_data': {'title': 'Create Petition', 'form': PetitionForm()}})

    form = PetitionForm(request.POST)
    if form.is_valid():
        petition = form.save(commit=False)
        petition.creator = request.user
        petition.save()
        return redirect('petitions.show', petition_id=petition.id)

    return render(request, 'petitions/create.html', {'template_data': {'title': 'Create Petition', 'form': form}})


@login_required
def vote(request, petition_id):
    """Handle yes/no voting for a petition.

    POST body must include `vote` with 'yes' or 'no'.
    Casting a vote will add the user to the respective M2M and remove them
    from the opposite vote so a user has at most one active vote.
    """
    petition = get_object_or_404(Petition, id=petition_id)

    if request.method != 'POST':
        return redirect('petitions.show', petition_id=petition_id)

    vote_value = request.POST.get('vote')
    user = request.user

    if vote_value == 'yes':
        petition.yes_votes.add(user)
        petition.no_votes.remove(user)
    elif vote_value == 'no':
        petition.no_votes.add(user)
        petition.yes_votes.remove(user)

    return redirect('petitions.show', petition_id=petition_id)
