"""SQLAlchemy persistence models registered in shared metadata."""

from organizeg3_api.infrastructure.persistence.models.audit_event import (
    AuditEventModel,
)
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
from organizeg3_api.infrastructure.persistence.models.finance import (
    FinancialAccountModel,
    FinancialAllocationModel,
    FinancialEntryModel,
    FinancialTransactionModel,
)
from organizeg3_api.infrastructure.persistence.models.inventory import (
    InventoryBalanceModel,
    InventoryLocationModel,
    InventoryMovementModel,
    InventoryReservationModel,
)
from organizeg3_api.infrastructure.persistence.models.machine import (
    MachineModel,
)
from organizeg3_api.infrastructure.persistence.models.material import (
    MaterialModel,
)
from organizeg3_api.infrastructure.persistence.models.production import (
    ProductionEventModel,
    ProductionExecutionModel,
    ProductionOperationModel,
    ProductionOrderModel,
    ProductionPauseModel,
)
from organizeg3_api.infrastructure.persistence.models.production_controls import (
    ProductionAssignmentModel,
    ProductionChecklistItemModel,
)
from organizeg3_api.infrastructure.persistence.models.purchasing import (
    PurchaseOrderItemModel,
    PurchaseOrderModel,
    PurchaseReceiptItemModel,
    PurchaseReceiptModel,
)
from organizeg3_api.infrastructure.persistence.models.sales import (
    SalesOrderItemModel,
    SalesOrderModel,
    SalesQuoteItemModel,
    SalesQuoteModel,
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
    "AuditEventModel",
    "BranchModel",
    "BrandModel",
    "CompanyModel",
    "CustomerModel",
    "EmployeeModel",
    "FinancialAccountModel",
    "FinancialAllocationModel",
    "FinancialEntryModel",
    "FinancialTransactionModel",
    "InventoryBalanceModel",
    "InventoryLocationModel",
    "InventoryMovementModel",
    "InventoryReservationModel",
    "MachineModel",
    "MaterialModel",
    "PermissionModel",
    "ProductionAssignmentModel",
    "ProductionChecklistItemModel",
    "ProductionEventModel",
    "ProductionExecutionModel",
    "ProductionOperationModel",
    "ProductionOrderModel",
    "ProductionPauseModel",
    "PurchaseOrderItemModel",
    "PurchaseOrderModel",
    "PurchaseReceiptItemModel",
    "PurchaseReceiptModel",
    "SalesOrderItemModel",
    "SalesOrderModel",
    "SalesQuoteItemModel",
    "SalesQuoteModel",
    "ServiceModel",
    "SupplierModel",
    "TenantMembershipModel",
    "TenantMembershipPermissionOverrideModel",
    "TenantMembershipProfileModel",
    "TenantModel",
    "TenantRecordModel",
    "UserModel",
]
