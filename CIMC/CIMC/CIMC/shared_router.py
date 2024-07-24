from rest_framework import routers


class SharedAPIRootRouter(routers.SimpleRouter):

    shared_router = routers.DefaultRouter()

    def register(self, *args, **kwargs):
        self.shared_router.register(*args, **kwargs)
        super(SharedAPIRootRouter, self).register(*args,**kwargs)