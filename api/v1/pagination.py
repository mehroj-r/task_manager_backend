from rest_framework import pagination


class CustomCursorPagination(pagination.CursorPagination):
    page_size = 5
    max_page_size = 5
    ordering = ('-created_at',)
