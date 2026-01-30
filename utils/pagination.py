import math

from django.core.paginator import Paginator


def make_pagination_range(
    page_range,
    qty_pages,
    current_page
):
    total_pages = len(page_range)
    middle_range = math.ceil(qty_pages / 2)
    start_range = current_page - middle_range
    if start_range <= 0:  # Defining static pagination range at the beginning
        start_range = 1
        final_range = qty_pages + 1
    else:  # Defining dynamic pagination range
        start_range = current_page - middle_range
        final_range = current_page + middle_range

    if final_range >= total_pages:  # Defining static pagination range at the end # noqa: E501
        start_range = total_pages - qty_pages + 1
        final_range = total_pages + 1

    pagination_range = list(range(start_range, final_range))
    return {
        'pagination_range': pagination_range,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'final_range': final_range,
        'first_page_out_of_range': current_page > middle_range+1,
        'last_page_out_of_range': final_range < total_pages,
    }


def make_pagination(request, queryset, per_page, aditional_url_query=''):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(current_page)

    pagination_obj = make_pagination_range(
        paginator.object_list,
        4,
        current_page
    )

    return page_obj, pagination_obj
