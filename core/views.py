import json
from django.template.response import TemplateResponse
from django.http import JsonResponse

from core.models import Entry,Tag

from core.forms import (
    RegisterEntryAPIForm,
    create_error_dict_from_form_errors,
)


def index(request):
    return TemplateResponse(request, "index.html", {
        "entry_list": Entry.objects.all()[:5],
        "tags": Tag.objects.all(),
    })


def entry_list_per_tag(request, tag_name):
    tag = Tag.objects.get(name=tag_name)

    return TemplateResponse(request, "index.html", {
        "entry_list": Entry.objects.filter(tags=tag),
        "tags": Tag.objects.all(),
    })


def api_search_entry(request):
    """ 記事検索API """
    return JsonResponse([entry.to_dict() for entry in Entry.search(request.GET.get("keyword"))], safe=False)


def api_entry(request):
    """ 記事投稿API """
    params = json.loads(request.body)
    form = RegisterEntryAPIForm(params)
    if not form.is_valid():
        return JsonResponse(create_error_dict_from_form_errors(form.errors), status=400)

    entry = form.save()
    entry.tags.set(Tag.multi_get_or_create(params.get("tags")))

    return JsonResponse({})


def _valid_limit(limit, default_value=10):
    try:
        return int(limit)
    except ValueError:
        return default_value
    except TypeError:
        return default_value


def api_recent_entry_list(request):
    """ 最近の記事取得API """
    limit = _valid_limit(request.GET.get("limit"))
    return JsonResponse([
        entry.to_dict(include_fields=["id", "day", "title", "content", "tags"])
        for entry in Entry.objects.order_by("-created_at")[:limit]
    ], safe=False)