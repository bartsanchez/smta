from users import views


def register(router):
    router.register('users', views.UserViewSet)
