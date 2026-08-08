"""SQLAlchemy persistence models registered in the shared metadata."""

from organizeg3_api.infrastructure.persistence.models.authorization import (
    AccessProfileModel,
    AccessProfilePermissionModel,
    PermissionModel,
    TenantMembershipPermissionOverrideModel,
    TenantMembershipProfileModel,
)
from organizeg3_api.infrastructure.persistence.models.branch import (
    BranchModel,
)
from organizeg3_api.infrastructure.persistence.models.brand import (
    BrandModel,
)
from organizeg3_api.infrastructure.persistence.models.company import (
    CompanyModel,
)
from organizeg3_api.infrastructure.persistence.models.customer import (
    CustomerModel,
)
from organizeg3_api.infrastructure.persistence.models.employee import (
    EmployeeModel,
)
from organizeg3_api.infrastructure.persistence.models.machine import (
    MachineModel,
)
from organizeg3_api.infrastructure.persistence.models.material import (
    MaterialModel,
)
from organizeg3_api.infrastructure.persistence.models.production import (
    ProductionExecutionModel,
    ProductionOperationModel,
    ProductionOrderModel,
)
from organizeg3_api.infrastructure.persistence.models.service import (
    ServiceModel,
)
from organizeg3_api.infrastructure.persistence.models.supplier import (
    SupplierModel,
)
from organizeg3_api.infrastructure.persistence.models.tenant import (
    TenantRecordModel,
)
from organizeg3_api.infrastructure.persistence.models.user import (
    TenantMembershipModel,
    UserModel,
)

TenantModel = TenantRecordModel


__all__ = [
    "AccessProfileModel",
    "AccessProfilePermissionModel",
    "BranchModel",
    "BrandModel",
    "CompanyModel",
    "CustomerModel",
    "EmployeeModel",
    "MachineModel",
    "MaterialModel",
    "PermissionModel",
    "ProductionExecutionModel",
    "ProductionOperationModel",
    "ProductionOrderModel",
    "ServiceModel",
    "SupplierModel",
    "TenantMembershipModel",
    "TenantMembershipPermissionOverrideModel",
    "TenantMembershipProfileModel",
    "TenantModel",
    "TenantRecordModel",
    "UserModel",
]
