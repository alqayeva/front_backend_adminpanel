from rest_framework.pagination import PageNumberPagination

from utils.response import paginated_success_response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        # DRF normalda pagination ucun birbasa count/next/previous/results qaytarir.
        # Task 9-da ise pagination da success/data/message formatina salinmalidir.
        return paginated_success_response(
            count=self.page.paginator.count,
            next_link=self.get_next_link(),
            previous_link=self.get_previous_link(),
            results=data,
        )
