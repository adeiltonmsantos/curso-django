from unittest import TestCase

from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_if_returns_pagination_range_correctly(self):
        page_range = list(range(1, 21))
        qty_pages = 9

        # Pagination range must be static here
        # Page = 1 -> [1,2,3,4,5,6,7,8,9]
        current_page = 1
        pg_rg = make_pagination_range(
            page_range=page_range,
            qty_pages=qty_pages,
            current_page=current_page
        )['pagination_range']

        self.assertEqual(
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            pg_rg,
            msg=f'When current_page={current_page} pagination range must be [1,2,3,4,5,6,7,8,9]'  # noqa: E501
        )

        # Pagination range must be static here
        # Page = 4 -> [1,2,3,4,5,6,7,8,9]
        current_page = 4
        pg_rg = make_pagination_range(
            page_range=page_range,
            qty_pages=qty_pages,
            current_page=current_page
        )['pagination_range']

        self.assertEqual(
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            pg_rg,
            msg=f'When current_page={current_page} pagination range must be [1,2,3,4,5,6,7,8,9]'  # noqa: E501
        )

        # Here pagination range isn't static anymore
        # Page = 5 -> [1,2,3,4,5,6,7,8,9]
        current_page = 5
        pg_rg = make_pagination_range(
            page_range=page_range,
            qty_pages=qty_pages,
            current_page=current_page
        )['pagination_range']

        self.assertEqual(
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            pg_rg,
            msg=f'When current_page={current_page} pagination range must be [1,2,3,4,5,6,7,8,9]'  # noqa: E501
        )

        # Here pagination range is static again
        # Page = 15 -> [12,13,14,15,16,17,18,19,20]
        current_page = 15
        pg_rg = make_pagination_range(
            page_range=page_range,
            qty_pages=qty_pages,
            current_page=current_page
        )['pagination_range']

        self.assertEqual(
            [12, 13, 14, 15, 16, 17, 18, 19, 20],
            pg_rg,
            msg=f'When current_page={current_page} pagination range must be [12,13,14,15,16,17,18,19,20]'  # noqa: E501
        )

        # Here pagination range is static again
        # Page >= 20 -> [12,13,14,15,16,17,18,19,20]
        current_page = 50
        pg_rg = make_pagination_range(
            page_range=page_range,
            qty_pages=qty_pages,
            current_page=current_page
        )['pagination_range']

        self.assertEqual(
            [12, 13, 14, 15, 16, 17, 18, 19, 20],
            pg_rg,
            msg=f'When current_page={current_page} pagination range must be [12,13,14,15,16,17,18,19,20]'  # noqa: E501
        )

    # def test_make_pagination_range_returns_a_pagination_range(self):
    #     pagination = make_pagination_range(
    #         page_range=list(range(1, 21)),
    #         qty_pages=4,
    #         current_page=1,
    #     )['pagination']
    #     self.assertEqual([1, 2, 3, 4], pagination)

    # def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):  # noqa: E501
    #     # Current page = 1 - Qty Page = 2 - Middle Page = 2
    #     pagination = make_pagination_range(
    #         page_range=list(range(1, 21)),
    #         qty_pages=4,
    #         current_page=1,
    #     )['pagination']
    #     self.assertEqual([1, 2, 3, 4], pagination)

    #     # Current page = 2 - Qty Page = 2 - Middle Page = 2
    #     pagination = make_pagination_range(
    #         page_range=list(range(1, 21)),
    #         qty_pages=4,
    #         current_page=2,
    #     )['pagination']
    #     self.assertEqual([1, 2, 3, 4], pagination)

    #     # Current page = 3 - Qty Page = 2 - Middle Page = 2
    #     # HERE RANGE SHOULD CHANGE
    #     pagination = make_pagination_range(
    #         page_range=list(range(1, 21)),
    #         qty_pages=4,
    #         current_page=3,
    #     )['pagination']
    #     self.assertEqual([2, 3, 4, 5], pagination)

    #     # Current page = 4 - Qty Page = 2 - Middle Page = 2
    #     # HERE RANGE SHOULD CHANGE
    #     pagination = make_pagination_range(
    #         page_range=list(range(1, 21)),
    #         qty_pages=4,
    #         current_page=4,
    #     )['pagination']
    #     self.assertEqual([3, 4, 5, 6], pagination)

    # def test_make_sure_middle_ranges_are_correct(self):
    #     # Current page = 10 - Qty Page = 2 - Middle Page = 2
    #     # HERE RANGE SHOULD CHANGE
    #     pagination = make_pagination_range(
    #         page_range=list(range(1, 21)),
    #         qty_pages=4,
    #         current_page=10,
    #     )['pagination']
    #     self.assertEqual([9, 10, 11, 12], pagination)

    #     # Current page = 14 - Qty Page = 2 - Middle Page = 2
    #     # HERE RANGE SHOULD CHANGE
    #     pagination = make_pagination_range(
    #         page_range=list(range(1, 21)),
    #         qty_pages=4,
    #         current_page=12,
    #     )['pagination']
    #     self.assertEqual([11, 12, 13, 14], pagination)

    # def test_make_pagination_range_is_static_when_last_page_is_next(self):
    #     # Current page = 18 - Qty Page = 2 - Middle Page = 2
    #     # HERE RANGE SHOULD CHANGE
    #     pagination = make_pagination_range(
    #         page_range=list(range(1, 21)),
    #         qty_pages=4,
    #         current_page=18,
    #     )['pagination']
    #     self.assertEqual([17, 18, 19, 20], pagination)

    #     # Current page = 19 - Qty Page = 2 - Middle Page = 2
    #     # HERE RANGE SHOULD CHANGE
    #     pagination = make_pagination_range(
    #         page_range=list(range(1, 21)),
    #         qty_pages=4,
    #         current_page=19,
    #     )['pagination']
    #     self.assertEqual([17, 18, 19, 20], pagination)

    #     # Current page = 20 - Qty Page = 2 - Middle Page = 2
    #     # HERE RANGE SHOULD CHANGE
    #     pagination = make_pagination_range(
    #         page_range=list(range(1, 21)),
    #         qty_pages=4,
    #         current_page=20,
    #     )['pagination']
    #     self.assertEqual([17, 18, 19, 20], pagination)

    #     # Current page = 21 - Qty Page = 2 - Middle Page = 2
    #     # HERE RANGE SHOULD CHANGE
    #     pagination = make_pagination_range(
    #         page_range=list(range(1, 21)),
    #         qty_pages=4,
    #         current_page=21,
    #     )['pagination']
    #     self.assertEqual([17, 18, 19, 20], pagination)
