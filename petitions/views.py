from django.shortcuts import render, redirect, get_object_or_404  # Django shortcuts for common patterns
from django.contrib.auth.decorators import login_required  # Decorator to require authentication
from .models import Petition  # Petition model defined in this app
from .forms import PetitionForm  # Form used to create petitions


def index(request):
    """Render a list of petitions ordered newest first.

    The template expects `template_data` with `title` and `petitions`.
    """
    petitions = Petition.objects.all().order_by('-created_at')  # Query for all petitions
    template_data = {'title': 'Petitions', 'petitions': petitions}  # Context for template
    return render(request, 'petitions/index.html', {'template_data': template_data})  # Render list template


def show(request, petition_id):
    """Render a single petition's detail view by id."""
    petition = get_object_or_404(Petition, id=petition_id)  # 404 if not found
    template_data = {'title': petition.title, 'petition': petition}  # Context for template
    return render(request, 'petitions/show.html', {'template_data': template_data})  # Render detail template


@login_required
def create(request):
    """Allow logged-in users to create a petition via GET/POST.

    GET: show empty form. POST: validate and save with the current user as creator.
    """
    if request.method == 'GET':
        return render(request, 'petitions/create.html', {'template_data': {'title': 'Create Petition', 'form': PetitionForm()}})

    form = PetitionForm(request.POST)  # Bind form for POST
    if form.is_valid():
        petition = form.save(commit=False)  # Create model instance but don't save yet
        petition.creator = request.user  # Set creator to current user
        petition.save()  # Persist to DB
        return redirect('petitions.show', petition_id=petition.id)  # Redirect to the new petition

    # If form invalid, re-render with errors
    return render(request, 'petitions/create.html', {'template_data': {'title': 'Create Petition', 'form': form}})


@login_required
def vote(request, petition_id):
    """Handle yes/no voting for a petition.

    POST body must include `vote` with 'yes' or 'no'.
    Casting a vote will add the user to the respective M2M and remove them
    from the opposite vote so a user has at most one active vote.
    """
    petition = get_object_or_404(Petition, id=petition_id)  # Fetch petition or 404

    if request.method != 'POST':
        return redirect('petitions.show', petition_id=petition_id)  # Only POST allowed for voting

    vote_value = request.POST.get('vote')  # Read vote value from form
    user = request.user  # Current user

    if vote_value == 'yes':
        petition.yes_votes.add(user)  # Record yes
        petition.no_votes.remove(user)  # Remove any previous no
    elif vote_value == 'no':
        petition.no_votes.add(user)  # Record no
        petition.yes_votes.remove(user)  # Remove any previous yes

    return redirect('petitions.show', petition_id=petition_id)  # Redirect back to detail view
