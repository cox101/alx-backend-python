
from rest_framework_nested.routers import NestedMixin
from rest_framework_nested import routers

class CustomNestedRouter(NestedMixin, routers.DefaultRouter):
    def get_parent_viewset(self, parent_viewset):
        return {
            'parent_pk': getattr(parent_viewset, 'parent_lookup_field', 'conversation_id'),
            'parent_queryset': parent_viewset.get_queryset
        }
