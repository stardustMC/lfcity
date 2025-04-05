from rest_framework.pagination import PageNumberPagination


class CourseListPagination(PageNumberPagination):
    max_page_size = 10
    size = 5
    page_query_param = "page"
    page_size_query_param = 'size'