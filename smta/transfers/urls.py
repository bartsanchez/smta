from transfers import views


def register(router):
    router.register('transfers', views.TransferViewSet)
