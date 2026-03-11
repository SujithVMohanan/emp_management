from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from .custom_response import ResponseInfo  # your common response format

class RestPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        # Build pagination links (strip domain if needed)
        next_link = self.get_next_link()
        previous_link = self.get_previous_link()
        links = {
            'next': next_link.replace(self.request.build_absolute_uri('/')[:-1], '') if next_link else "",
            'previous': previous_link.replace(self.request.build_absolute_uri('/')[:-1], '') if previous_link else ""
        }

        # Prepare main data
        paginated_data = {
            'links': links,
            'count': self.page.paginator.count,
            'results': data,
            'heading': {}
        }

        # Wrap in ResponseInfo
        response_format = ResponseInfo(
            data=paginated_data,
            status=True,
            status_code=status.HTTP_200_OK,
            message="Data retrieved successfully"
        ).response

        return Response(response_format, status=status.HTTP_200_OK)