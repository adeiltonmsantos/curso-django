import math


def make_pagination_range(
    page_range=list(range(1, 21)),
    qty_pages=4,
    current_page=1
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

    if final_range >= len(page_range):  # Defining static pagination range at the end # noqa: E501
        start_range = len(page_range) - qty_pages + 1
        final_range = len(page_range) + 1

    pagination_range = list(range(start_range, final_range))
    return {
        'pagination_range': pagination_range,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'final_range': final_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': final_range < total_pages,
    }

# def make_pagination_range(
#     page_range,
#     qty_pages,
#     current_page,
# ):
#     middle_range = math.ceil(qty_pages / 2)
#     start_range = current_page - middle_range
#     stop_range = current_page + middle_range
#     total_pages = len(page_range)

#     start_range_offset = abs(start_range) if start_range < 0 else 0

#     if start_range < 0:
#         start_range = 0
#         stop_range += start_range_offset

#     if stop_range >= total_pages:
#         start_range = start_range - abs(total_pages - stop_range)

#     pagination = page_range[start_range:stop_range]
#     return {
#         'pagination': pagination,
#         'page_range': page_range,
#         'qty_pages': qty_pages,
#         'current_page': current_page,
#         'total_pages': total_pages,
#         'start_range': start_range,
#         'stop_range': stop_range,
#         'first_page_out_of_range': current_page > middle_range,
#         'last_page_out_of_range': stop_range < total_pages,
#     }
