from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from deep_translator import GoogleTranslator
from django.contrib.auth.decorators import login_required
from .forms import TranslationForm
from .models import Translation

@login_required
def home(request):

    translated_text = None

    if request.method == "POST":

        form = TranslationForm(request.POST)

        if form.is_valid():

            text = form.cleaned_data["text"]
            source = form.cleaned_data["source_language"]
            target = form.cleaned_data["target_language"]

            translated_text = GoogleTranslator(
                source=source,
                target=target
            ).translate(text)

            Translation.objects.create(
                user=request.user,
                original_text=text,
                translated_text=translated_text,
                source_language=source,
                target_language=target,
            )

    else:
        form = TranslationForm()

    context = {
        "form": form,
        "translated_text": translated_text,
    }

    return render(
        request,
        "translator/home.html",
        context,
    )


@login_required
def history(request):

    query = request.GET.get("q", "")

    translations = Translation.objects.filter(
        user=request.user
    )
    if query:
        translations = translations.filter(
            Q(original_text__icontains=query) |
            Q(translated_text__icontains=query)
        )

    translations = translations.order_by("-created_at")

    context = {
        "translations": translations,
        "query": query,
    }

    return render(
        request,
        "translator/history.html",
        context,
    )


@login_required
def delete_translation(request, id):
    translation = get_object_or_404(
        Translation,
        id=id
    )

    if request.method == "POST":
        translation.delete()

    return redirect("history")