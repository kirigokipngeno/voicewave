from django.contrib.auth.views import LogoutView, LoginView
from django.contrib import messages
from datetime import timedelta

from django.utils import timezone
from django.core.paginator import Paginator
from django.template import loader

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy

from users.models import ContactInfo
from .models import Question, Choice,Vote
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required, user_passes_test


# Get questions and display them
# @login_required
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {'latest_question_list': latest_question_list, 'page':'polls'}
    return render(request, 'polls/index.html', context)

# Show specific question and choices
@login_required
def detail(request, question_id):
  try:
    question = Question.objects.get(pk=question_id)
  except Question.DoesNotExist:
    raise Http404("Question does not exist")
  return render(request, 'polls/detail.html', { 'question': question })

# Get question and display results
# @login_required
def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/results.html', { 'question': question })

# Vote for a question choice
@login_required

def vote(request, question_id):
    """
    Handle voting for a specific question.
    """
    question = get_object_or_404(Question, pk=question_id)

    # Check if the question is open for voting
    if not question.is_open:
        messages.error(request, "Voting is closed for this question.")
        return redirect('polls:detail', question_id=question.id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form with an error message
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a valid choice.",
        })
    else:
        # Check if the user has already voted on this question
        user_vote = Vote.objects.filter(user=request.user, choice__question=question).first()

        if user_vote:
            # If the user has voted before, update the vote
            user_vote.choice.votes -= 1  # Decrement the vote count of the previously selected choice
            user_vote.choice.save()
            user_vote.choice = selected_choice
        else:
            # Record a new vote
            user_vote = Vote(user=request.user, choice=selected_choice)

        # Update the vote count for the newly selected choice
        selected_choice.votes += 1
        selected_choice.save()
        user_vote.save()
        messages.success(request, "Your vote has been successfully submitted!")

        # Redirect to the results page
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


@login_required
def resultsData(request, obj):
    votedata = []

    question = Question.objects.get(id=obj)
    votes = question.choice_set.all()

    for i in votes:
        votedata.append({i.choice_text:i.votes})

    return JsonResponse(votedata, safe=False)
@user_passes_test(lambda u: u.is_staff) 
def close_election(request, question_id):
    question: object = get_object_or_404(Question, pk=question_id)
    question.is_open = False
    question.save() # Ensure this is on a new line
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
@user_passes_test(lambda u: u.is_staff)
@login_required
def admin_dashboard(request):
    """
    Display the admin dashboard with a paginated list of questions
    and optional search functionality.
    """
    search_query = request.GET.get('search', '')
    questions = Question.objects.filter(question_text__icontains=search_query)

    # Set up pagination for questions
    paginator = Paginator(questions, 5)  # Show 5 questions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    one_week_ago = timezone.now() - timedelta(days=7)

    new_contacts_count = ContactInfo.objects.filter(date__gte=one_week_ago).count()



    context = {
        'questions': page_obj,
        'search_query': search_query,
    }

    return render(request, 'polls/admin_dashboard.html', context)

def close_voting(request, question_id):
    """
    Close voting for a specific question by setting its `is_open` field to False.
    """
    question = get_object_or_404(Question, id=question_id)
    question.is_open = False
    question.save()
    return redirect('polls:admin_dashboard')

def continue_voting(request, question_id):
    """
    Reopen voting for a specific question by setting its `is_open` field to True.
    """
    question = get_object_or_404(Question, id=question_id)
    question.is_open = True
    question.save()
    return redirect('polls:admin_dashboard')
class AdminLoginView(LoginView):
    template_name = 'polls/admin_login.html'

    def get_success_url(self):
        return reverse_lazy('polls:admin_dashboard')  # Redirect to admin dashboard after login

class AdminLogoutView(LogoutView):
    template_name = 'polls/admin_logout.html'
@user_passes_test(lambda u: u.is_staff)
def admin_results(request):
    """
    Display all questions and their results to admin users.
    """
    questions = Question.objects.all()
    context = {
        'questions': questions,
    }
    return render(request, 'polls/admin_results.html', context)