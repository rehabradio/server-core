from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate_queryset(serializer, request, queryset, page, limit=20):
    """Build a paginated response for a given queryset."""
    paginator = Paginator(queryset, 20)
    try:
        tracks = paginator.page(page)
    except PageNotAnInteger:
        tracks = paginator.page(1)
    except EmptyPage:
        tracks = paginator.page(paginator.num_pages)

    serializer_context = {'request': request}
    serializer_obj = serializer(
        tracks, context=serializer_context
    )

    return serializer_obj.data
