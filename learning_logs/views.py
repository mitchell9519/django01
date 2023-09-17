from django.shortcuts import render,redirect
from .models import Topic,Entry
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
# Create your views here.

def index(request):
    '''Homepage for learning logs'''
    return render(request, 'learning_logs/index.html')
    
@login_required    
def topics(request):
    #show all topics
    
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html',context)

@login_required    
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required    
def new_topic(request):
    '''Creates a new topoic from users side'''
    if request.method != 'POST':
        #no data submitted;create blank form
        form = TopicForm()
    else:
        #POST submitted ; process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    #display blank invalid form   

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required    
def new_entry(request, topic_id):
    '''Add new entry for a topic'''
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        #no data submitted;create blank form
        form = EntryForm()
        
    else:
        #POST submitted ; process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic',topic_id =topic_id)
    context = {'topic': topic, 'form' : form}
    return render(request, 'learning_logs/new_entry.html', context)




@login_required    
def edit_entry(request, entry_id):
    '''Edit an entry for a topic'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #pre-fill form with current entry
        form = EntryForm(instance=entry)
        
    else:
        #initial request,pre-fill with current entry
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
        
    context = {'entry': entry,'topic': topic, 'form' : form}
    return render(request, 'learning_logs/edit_entry.html', context)