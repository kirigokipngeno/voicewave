from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

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
    question = get_object_or_404(Question, pk=question_id)

    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not authenticated

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form if the choice is invalid or not found
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # Check if the user has already voted in this question
        user_vote = Vote.objects.filter(user=request.user, choice__question=question).first()

        if user_vote:
            # If the user has voted before, update the vote
            user_vote.choice.votes -= 1  # Decrement the vote count of the previously selected choice
            user_vote.choice.save()
            user_vote.choice = selected_choice
        else:
            # Record the new vote
            user_vote = Vote(user=request.user, choice=selected_choice)

        # Update the vote count of the newly selected choice
        selected_choice.votes += 1
        selected_choice.save()
        user_vote.save()

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
def admin_dashboard(request): 
    questions = Question.objects.all() 
    return render(request, 'polls/admin_dashboard.html', {'questions':questions})
@user_passes_test(lambda u: u.is_staff)
def continue_election(request, question_id):
    """
    View to mark a question as open (continue the election).
    Only accessible by staff users.
    """
    question = get_object_or_404(Question, pk=question_id)
    question.is_open = True
    question.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """
    View to display the admin dashboard.
    Includes a list of all questions and contact information.
    Only accessible by staff users.
    """
    questions = Question.objects.all()
    contacts = ContactInfo.objects.all()
    return render(request, 'polls/admin_dashboard.html', {'questions': questions, 'contacts': contacts})