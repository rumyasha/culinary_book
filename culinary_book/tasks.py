from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Recipe
import requests


@shared_task
def send_daily_recommendations():
    meal_types = ['breakfast', 'lunch', 'dinner']
    recommendations = {}

    for meal_type in meal_types:
        top_recipes = Recipe.objects.filter(meal_type=meal_type).order_by('-average_rating')[:3]
        recommendations[meal_type] = top_recipes

    # Отправка email
    subject = 'Кулинарные рекомендации на сегодня'
    message = 'Лучшие рецепты:\n\n'

    for meal_type, recipes in recommendations.items():
        message += f"{meal_type}:\n"
        for recipe in recipes:
            message += f"- {recipe.title} (Рейтинг: {recipe.average_rating()})\n"
        message += "\n"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ['user@example.com'],  # Замените на реальные email
        fail_silently=False,
    )

    # Отправка в Telegram (пример)
    bot_token = 'YOUR_BOT_TOKEN'
    chat_id = 'USER_CHAT_ID'
    telegram_message = 'Ваши кулинарные рекомендации на сегодня:\n\n' + message
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={telegram_message}'
    requests.get(url)