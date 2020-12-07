from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class ModelLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10


class ModelPageNumberPagination(PageNumberPagination):
    page_size = 1


