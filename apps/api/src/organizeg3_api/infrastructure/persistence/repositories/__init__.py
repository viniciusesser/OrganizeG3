"""SQLAlchemy repository implementations."""

from organizeg3_api.infrastructure.persistence.repositories.branch_repository import (
    SQLAlchemyBranchRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.brand_repository import (
    SQLAlchemyBrandRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.company_repository import (
    SQLAlchemyCompanyRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.customer_audit_repository import (
    SQLAlchemyCustomerAuditRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.customer_repository import (
    SQLAlchemyCustomerRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.employee_repository import (
    SQLAlchemyEmployeeRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.finance_repository import (
    SQLAlchemyFinancialAccountRepository,
    SQLAlchemyFinancialAllocationRepository,
    SQLAlchemyFinancialEntryRepository,
    SQLAlchemyFinancialTransactionRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.inventory_repository import (
    SQLAlchemyInventoryBalanceRepository,
    SQLAlchemyInventoryLocationRepository,
    SQLAlchemyInventoryMovementRepository,
    SQLAlchemyInventoryReservationRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.machine_repository import (
    SQLAlchemyMachineRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.material_repository import (
    SQLAlchemyMaterialRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.production_controls_repository import (
    SQLAlchemyProductionAssignmentRepository,
    SQLAlchemyProductionChecklistItemRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.production_repository import (
    SQLAlchemyProductionEventRepository,
    SQLAlchemyProductionExecutionRepository,
    SQLAlchemyProductionOperationRepository,
    SQLAlchemyProductionOrderRepository,
    SQLAlchemyProductionPauseRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.purchasing_repository import (
    SQLAlchemyPurchaseOrderItemRepository,
    SQLAlchemyPurchaseOrderRepository,
    SQLAlchemyPurchaseReceiptItemRepository,
    SQLAlchemyPurchaseReceiptRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.service_repository import (
    SQLAlchemyServiceRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.supplier_repository import (
    SQLAlchemySupplierRepository,
)
from organizeg3_api.infrastructure.persistence.repositories.tenant_repository import (
    SQLAlchemyTenantRepository,
)

__all__ = [
    "SQLAlchemyBranchRepository",
    "SQLAlchemyBrandRepository",
    "SQLAlchemyCompanyRepository",
    "SQLAlchemyCustomerAuditRepository",
    "SQLAlchemyCustomerRepository",
    "SQLAlchemyEmployeeRepository",
    "SQLAlchemyFinancialAccountRepository",
    "SQLAlchemyFinancialAllocationRepository",
    "SQLAlchemyFinancialEntryRepository",
    "SQLAlchemyFinancialTransactionRepository",
    "SQLAlchemyInventoryBalanceRepository",
    "SQLAlchemyInventoryLocationRepository",
    "SQLAlchemyInventoryMovementRepository",
    "SQLAlchemyInventoryReservationRepository",
    "SQLAlchemyMachineRepository",
    "SQLAlchemyMaterialRepository",
    "SQLAlchemyProductionAssignmentRepository",
    "SQLAlchemyProductionChecklistItemRepository",
    "SQLAlchemyProductionEventRepository",
    "SQLAlchemyProductionExecutionRepository",
    "SQLAlchemyProductionOperationRepository",
    "SQLAlchemyProductionOrderRepository",
    "SQLAlchemyProductionPauseRepository",
    "SQLAlchemyPurchaseOrderItemRepository",
    "SQLAlchemyPurchaseOrderRepository",
    "SQLAlchemyPurchaseReceiptItemRepository",
    "SQLAlchemyPurchaseReceiptRepository",
    "SQLAlchemyServiceRepository",
    "SQLAlchemySupplierRepository",
    "SQLAlchemyTenantRepository",
]
