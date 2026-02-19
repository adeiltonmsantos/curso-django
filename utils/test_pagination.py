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
