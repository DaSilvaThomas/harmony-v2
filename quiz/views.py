from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from .models import QuizTheme, Question, Score
import random

@login_required
def quiz_home(request):
    """Page d'accueil du quiz avec les scores"""
    themes = QuizTheme.objects.all()
    
    # Scores globaux (top 10)
    top_scores = Score.objects.values('user__username').annotate(
        total=Sum('points_total')
    ).order_by('-total')[:10]
    
    # Scores par thème
    theme_scores = {}
    for theme in themes:
        theme_scores[theme] = Score.objects.filter(theme=theme).order_by('-points_total')[:5]
    
    context = {
        'themes': themes,
        'top_scores': top_scores,
        'theme_scores': theme_scores,
    }
    return render(request, 'quiz/quiz_home.html', context)

@login_required
def quiz_theme(request, theme_id):
    """Page détail d'un thème"""
    theme = get_object_or_404(QuizTheme, id=theme_id)
    scores = Score.objects.filter(theme=theme).order_by('-points_total')[:10]
    
    context = {
        'theme': theme,
        'scores': scores,
        'question_count': theme.questions.count(),
    }
    return render(request, 'quiz/quiz_theme.html', context)

@login_required
def quiz_play(request, theme_id=None):
    """Jouer au quiz"""
    if theme_id:
        theme = get_object_or_404(QuizTheme, id=theme_id)
        questions = list(theme.questions.all())
    else:
        # Quiz aléatoire
        questions = list(Question.objects.all())
        theme = None
    
    if not questions:
        messages.error(request, "Aucune question disponible pour ce thème.")
        return redirect('quiz_home')
    
    # Sélectionner 10 questions aléatoires (ou moins si pas assez)
    random.shuffle(questions)
    questions = questions[:10]
    
    # Initialiser la session de quiz
    if 'quiz_session' not in request.session or request.method == 'GET':
        request.session['quiz_session'] = {
            'theme_id': theme.id if theme else None,
            'questions': [q.id for q in questions],
            'current_index': 0,
            'score': 0,
            'answers': []
        }
    
    session = request.session['quiz_session']
    current_index = session['current_index']
    
    # Traitement de la réponse
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        user_answer = request.POST.get('answer')
        
        if question_id and user_answer:
            question = Question.objects.get(id=question_id)
            is_correct = user_answer == question.bonne_reponse
            
            if is_correct:
                session['score'] += 10
            
            session['answers'].append({
                'question_id': question_id,
                'user_answer': user_answer,
                'correct': is_correct
            })
            
            session['current_index'] += 1
            request.session.modified = True
            
            # Vérifier si c'est la fin du quiz
            if session['current_index'] >= len(session['questions']):
                return redirect('quiz_result')
    
    # Obtenir la question courante
    if current_index < len(session['questions']):
        current_question = Question.objects.get(id=session['questions'][current_index])
        shuffled_answers = current_question.get_all_reponses_shuffled()
    else:
        return redirect('quiz_result')
    
    context = {
        'theme': theme,
        'question': current_question,
        'answers': shuffled_answers,
        'current_index': current_index + 1,
        'total_questions': len(session['questions']),
        'score': session['score'],
    }
    return render(request, 'quiz/quiz_play.html', context)

@login_required
def quiz_result(request):
    """Afficher les résultats du quiz"""
    if 'quiz_session' not in request.session:
        return redirect('quiz_home')
    
    session = request.session['quiz_session']
    score = session['score']
    theme_id = session.get('theme_id')
    
    # Enregistrer le score
    if theme_id:
        theme = QuizTheme.objects.get(id=theme_id)
        Score.objects.create(
            user=request.user,
            theme=theme,
            points_total=score
        )
    
    # Récupérer les détails des réponses
    answers_details = []
    for answer in session['answers']:
        question = Question.objects.get(id=answer['question_id'])
        answers_details.append({
            'question': question,
            'user_answer': answer['user_answer'],
            'correct': answer['correct']
        })
    
    context = {
        'score': score,
        'total_questions': len(session['questions']),
        'answers': answers_details,
        'theme': QuizTheme.objects.get(id=theme_id) if theme_id else None,
    }
    
    # Nettoyer la session
    del request.session['quiz_session']
    request.session.modified = True
    
    return render(request, 'quiz/quiz_result.html', context)