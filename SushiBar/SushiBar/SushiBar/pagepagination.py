import math
from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, _positive_int
from rest_framework.utils.urls import remove_query_param, replace_query_param


class HeaderPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        print(self.page_size_query_param)
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()
        first_url = self.get_first_link()
        last_url = self.get_last_link()

        links = []
        for label, url in (
                ("first", first_url),
                ("next", next_url),
                ("previous", previous_url),
                ("last", last_url),
        ):
            if url is not None:
                links.append('<{}>; rel="{}"'.format(url, label))

        headers = {"x-total-count": self.page.paginator.count}
        headers["link"] = ", ".join(links) if links else {}

        return Response(data, headers=headers)

    def get_first_link(self):
        if self.page.number <= 0:
            return None
        url = self.request.build_absolute_uri()
        return remove_query_param(url, self.page_query_param)

    def get_last_link(self):
        _page_size = self.get_page_size(self.request)
        if self.page.number + _page_size >= self.page.paginator.count:
            return None
        url = self.request.build_absolute_uri()
        url = replace_query_param(url, self.page_size_query_param, _page_size)
        page = math.ceil(self.page.paginator.count/_page_size)
        return replace_query_param(url, self.page_query_param, page)