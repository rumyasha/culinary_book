from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .models import Recipe, Rating, Comment, Favorite
from .forms import RecipeForm, RatingForm, CommentForm, UserRegistrationForm


def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-created_at')
    return render(request, 'culinary_book/recipe_list.html', {'recipes': recipes})


@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        if 'rating_submit' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                Rating.objects.update_or_create(
                    recipe=recipe,
                    user=request.user,
                    defaults={'value': rating_form.cleaned_data['value']}
                )
                messages.success(request, 'Ваша оценка сохранена!')
                return redirect('recipe_detail', pk=pk)

        elif 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.recipe = recipe
                comment.author = request.user
                comment.save()
                messages.success(request, 'Комментарий добавлен!')
                return redirect('recipe_detail', pk=pk)

        elif 'favorite_submit' in request.POST:
            Favorite.objects.get_or_create(user=request.user, recipe=recipe)
            messages.success(request, 'Рецепт добавлен в избранное!')
            return redirect('recipe_detail', pk=pk)

    rating_form = RatingForm()
    comment_form = CommentForm()
    is_favorite = Favorite.objects.filter(user=request.user,
                                          recipe=recipe).exists() if request.user.is_authenticated else False

    return render(request, 'culinary_book/recipe_detail.html', {
        'recipe': recipe,
        'rating_form': rating_form,
        'comment_form': comment_form,
        'is_favorite': is_favorite,
    })


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Рецепт успешно добавлен!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'culinary_book/recipe_form.html', {'form': form})


@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('recipe')
    return render(request, 'culinary_book/favorites.html', {'favorites': favorites})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('recipe_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'culinary_book/register.html', {'form': form})