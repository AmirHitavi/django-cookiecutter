class ActionContextSerializerMixin:
    """
    Injects the current view action into the serializer context.
    This mixin is intended for use with Django REST Framework ViewSets,
    where the `action` attribute is defined.
    """
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["action"] = getattr(self, "action", None)
        return context
