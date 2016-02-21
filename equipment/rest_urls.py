from CIMC.shared_router import SharedAPIRootRouter

from rest_views import EquipmentTypeViewSet

router = SharedAPIRootRouter()
router.register(r'EquipmentType', EquipmentTypeViewSet)
router.regiser()