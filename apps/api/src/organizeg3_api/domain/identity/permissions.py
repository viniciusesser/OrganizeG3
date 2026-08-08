"""Canonical permission definitions used by OrganizeG3 authorization."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PermissionDefinition:
    """Describe one canonical application permission."""

    code: str
    name: str
    module: str
    resource: str
    action: str
    description: str | None = None


class CustomerPermissions:
    """Permission codes for customer operations."""

    READ = "customers.read"
    CREATE = "customers.create"
    UPDATE = "customers.update"
    ARCHIVE = "customers.archive"
    REACTIVATE = "customers.reactivate"


class CompanyPermissions:
    """Permission codes for company operations."""

    READ = "company.read"
    CREATE = "company.create"
    UPDATE = "company.update"


class BranchPermissions:
    """Permission codes for branch operations."""

    READ = "branches.read"
    CREATE = "branches.create"
    UPDATE = "branches.update"
    DEACTIVATE = "branches.deactivate"
    REACTIVATE = "branches.reactivate"


class EmployeePermissions:
    """Permission codes for employee operations."""

    READ = "employees.read"
    CREATE = "employees.create"
    UPDATE = "employees.update"
    DEACTIVATE = "employees.deactivate"
    REACTIVATE = "employees.reactivate"


class SupplierPermissions:
    """Permission codes for supplier operations."""

    READ = "suppliers.read"
    CREATE = "suppliers.create"
    UPDATE = "suppliers.update"
    DEACTIVATE = "suppliers.deactivate"
    REACTIVATE = "suppliers.reactivate"


class MaterialPermissions:
    """Permission codes for material operations."""

    READ = "materials.read"
    CREATE = "materials.create"
    UPDATE = "materials.update"
    DEACTIVATE = "materials.deactivate"
    REACTIVATE = "materials.reactivate"


class ServicePermissions:
    """Permission codes for service operations."""

    READ = "services.read"
    CREATE = "services.create"
    UPDATE = "services.update"
    DEACTIVATE = "services.deactivate"
    REACTIVATE = "services.reactivate"


class MachinePermissions:
    """Permission codes for machine operations."""

    READ = "machines.read"
    CREATE = "machines.create"
    UPDATE = "machines.update"
    CHANGE_STATUS = "machines.change_status"
    DEACTIVATE = "machines.deactivate"
    REACTIVATE = "machines.reactivate"


class BrandPermissions:
    """Permission codes for brand operations."""

    READ = "brands.read"
    CREATE = "brands.create"
    UPDATE = "brands.update"
    DEACTIVATE = "brands.deactivate"
    REACTIVATE = "brands.reactivate"


PERMISSION_CATALOG = (
    PermissionDefinition(
        code=CustomerPermissions.READ,
        name="Visualizar clientes",
        module="customers",
        resource="customers",
        action="read",
        description="Permite consultar clientes do tenant.",
    ),
    PermissionDefinition(
        code=CustomerPermissions.CREATE,
        name="Criar clientes",
        module="customers",
        resource="customers",
        action="create",
        description="Permite criar clientes no tenant.",
    ),
    PermissionDefinition(
        code=CustomerPermissions.UPDATE,
        name="Atualizar clientes",
        module="customers",
        resource="customers",
        action="update",
        description="Permite atualizar clientes do tenant.",
    ),
    PermissionDefinition(
        code=CustomerPermissions.ARCHIVE,
        name="Arquivar clientes",
        module="customers",
        resource="customers",
        action="archive",
        description="Permite arquivar clientes do tenant.",
    ),
    PermissionDefinition(
        code=CustomerPermissions.REACTIVATE,
        name="Reativar clientes",
        module="customers",
        resource="customers",
        action="reactivate",
        description="Permite reativar clientes do tenant.",
    ),
    PermissionDefinition(
        code=CompanyPermissions.READ,
        name="Visualizar empresa",
        module="company",
        resource="company",
        action="read",
        description="Permite consultar os dados da empresa do tenant.",
    ),
    PermissionDefinition(
        code=CompanyPermissions.CREATE,
        name="Criar empresa",
        module="company",
        resource="company",
        action="create",
        description="Permite criar os dados da empresa do tenant.",
    ),
    PermissionDefinition(
        code=CompanyPermissions.UPDATE,
        name="Atualizar empresa",
        module="company",
        resource="company",
        action="update",
        description="Permite atualizar os dados da empresa do tenant.",
    ),
    PermissionDefinition(
        code=BranchPermissions.READ,
        name="Visualizar filiais",
        module="branches",
        resource="branches",
        action="read",
        description="Permite consultar filiais do tenant.",
    ),
    PermissionDefinition(
        code=BranchPermissions.CREATE,
        name="Criar filiais",
        module="branches",
        resource="branches",
        action="create",
        description="Permite criar filiais do tenant.",
    ),
    PermissionDefinition(
        code=BranchPermissions.UPDATE,
        name="Atualizar filiais",
        module="branches",
        resource="branches",
        action="update",
        description="Permite atualizar filiais do tenant.",
    ),
    PermissionDefinition(
        code=BranchPermissions.DEACTIVATE,
        name="Desativar filiais",
        module="branches",
        resource="branches",
        action="deactivate",
        description="Permite desativar filiais do tenant.",
    ),
    PermissionDefinition(
        code=BranchPermissions.REACTIVATE,
        name="Reativar filiais",
        module="branches",
        resource="branches",
        action="reactivate",
        description="Permite reativar filiais do tenant.",
    ),
    PermissionDefinition(
        code=EmployeePermissions.READ,
        name="Visualizar funcionários",
        module="employees",
        resource="employees",
        action="read",
        description="Permite consultar funcionários do tenant.",
    ),
    PermissionDefinition(
        code=EmployeePermissions.CREATE,
        name="Criar funcionários",
        module="employees",
        resource="employees",
        action="create",
        description="Permite criar funcionários no tenant.",
    ),
    PermissionDefinition(
        code=EmployeePermissions.UPDATE,
        name="Atualizar funcionários",
        module="employees",
        resource="employees",
        action="update",
        description="Permite atualizar funcionários do tenant.",
    ),
    PermissionDefinition(
        code=EmployeePermissions.DEACTIVATE,
        name="Desativar funcionários",
        module="employees",
        resource="employees",
        action="deactivate",
        description="Permite desativar funcionários do tenant.",
    ),
    PermissionDefinition(
        code=EmployeePermissions.REACTIVATE,
        name="Reativar funcionários",
        module="employees",
        resource="employees",
        action="reactivate",
        description="Permite reativar funcionários do tenant.",
    ),
    PermissionDefinition(
        code=SupplierPermissions.READ,
        name="Visualizar fornecedores",
        module="suppliers",
        resource="suppliers",
        action="read",
        description="Permite consultar fornecedores do tenant.",
    ),
    PermissionDefinition(
        code=SupplierPermissions.CREATE,
        name="Criar fornecedores",
        module="suppliers",
        resource="suppliers",
        action="create",
        description="Permite criar fornecedores no tenant.",
    ),
    PermissionDefinition(
        code=SupplierPermissions.UPDATE,
        name="Atualizar fornecedores",
        module="suppliers",
        resource="suppliers",
        action="update",
        description="Permite atualizar fornecedores do tenant.",
    ),
    PermissionDefinition(
        code=SupplierPermissions.DEACTIVATE,
        name="Desativar fornecedores",
        module="suppliers",
        resource="suppliers",
        action="deactivate",
        description="Permite desativar fornecedores do tenant.",
    ),
    PermissionDefinition(
        code=SupplierPermissions.REACTIVATE,
        name="Reativar fornecedores",
        module="suppliers",
        resource="suppliers",
        action="reactivate",
        description="Permite reativar fornecedores do tenant.",
    ),
    PermissionDefinition(
        code=MaterialPermissions.READ,
        name="Visualizar materiais",
        module="materials",
        resource="materials",
        action="read",
        description="Permite consultar materiais do tenant.",
    ),
    PermissionDefinition(
        code=MaterialPermissions.CREATE,
        name="Criar materiais",
        module="materials",
        resource="materials",
        action="create",
        description="Permite criar materiais no tenant.",
    ),
    PermissionDefinition(
        code=MaterialPermissions.UPDATE,
        name="Atualizar materiais",
        module="materials",
        resource="materials",
        action="update",
        description="Permite atualizar materiais do tenant.",
    ),
    PermissionDefinition(
        code=MaterialPermissions.DEACTIVATE,
        name="Desativar materiais",
        module="materials",
        resource="materials",
        action="deactivate",
        description="Permite desativar materiais do tenant.",
    ),
    PermissionDefinition(
        code=MaterialPermissions.REACTIVATE,
        name="Reativar materiais",
        module="materials",
        resource="materials",
        action="reactivate",
        description="Permite reativar materiais do tenant.",
    ),
    PermissionDefinition(
        code=ServicePermissions.READ,
        name="Visualizar serviços",
        module="services",
        resource="services",
        action="read",
        description="Permite consultar serviços do tenant.",
    ),
    PermissionDefinition(
        code=ServicePermissions.CREATE,
        name="Criar serviços",
        module="services",
        resource="services",
        action="create",
        description="Permite criar serviços no tenant.",
    ),
    PermissionDefinition(
        code=ServicePermissions.UPDATE,
        name="Atualizar serviços",
        module="services",
        resource="services",
        action="update",
        description="Permite atualizar serviços do tenant.",
    ),
    PermissionDefinition(
        code=ServicePermissions.DEACTIVATE,
        name="Desativar serviços",
        module="services",
        resource="services",
        action="deactivate",
        description="Permite desativar serviços do tenant.",
    ),
    PermissionDefinition(
        code=ServicePermissions.REACTIVATE,
        name="Reativar serviços",
        module="services",
        resource="services",
        action="reactivate",
        description="Permite reativar serviços do tenant.",
    ),
    PermissionDefinition(
        code=MachinePermissions.READ,
        name="Visualizar máquinas",
        module="machines",
        resource="machines",
        action="read",
        description="Permite consultar máquinas do tenant.",
    ),
    PermissionDefinition(
        code=MachinePermissions.CREATE,
        name="Criar máquinas",
        module="machines",
        resource="machines",
        action="create",
        description="Permite criar máquinas no tenant.",
    ),
    PermissionDefinition(
        code=MachinePermissions.UPDATE,
        name="Atualizar máquinas",
        module="machines",
        resource="machines",
        action="update",
        description="Permite atualizar os dados cadastrais das máquinas do tenant.",
    ),
    PermissionDefinition(
        code=MachinePermissions.CHANGE_STATUS,
        name="Alterar status de máquinas",
        module="machines",
        resource="machines",
        action="change_status",
        description="Permite alterar o status operacional das máquinas do tenant.",
    ),
    PermissionDefinition(
        code=MachinePermissions.DEACTIVATE,
        name="Desativar máquinas",
        module="machines",
        resource="machines",
        action="deactivate",
        description="Permite desativar máquinas do tenant.",
    ),
    PermissionDefinition(
        code=MachinePermissions.REACTIVATE,
        name="Reativar máquinas",
        module="machines",
        resource="machines",
        action="reactivate",
        description="Permite reativar máquinas do tenant.",
    ),
    PermissionDefinition(
        code=BrandPermissions.READ,
        name="Visualizar marcas",
        module="brands",
        resource="brands",
        action="read",
        description="Permite consultar marcas do tenant.",
    ),
    PermissionDefinition(
        code=BrandPermissions.CREATE,
        name="Criar marcas",
        module="brands",
        resource="brands",
        action="create",
        description="Permite criar marcas no tenant.",
    ),
    PermissionDefinition(
        code=BrandPermissions.UPDATE,
        name="Atualizar marcas",
        module="brands",
        resource="brands",
        action="update",
        description="Permite atualizar marcas do tenant.",
    ),
    PermissionDefinition(
        code=BrandPermissions.DEACTIVATE,
        name="Desativar marcas",
        module="brands",
        resource="brands",
        action="deactivate",
        description="Permite desativar marcas do tenant.",
    ),
    PermissionDefinition(
        code=BrandPermissions.REACTIVATE,
        name="Reativar marcas",
        module="brands",
        resource="brands",
        action="reactivate",
        description="Permite reativar marcas do tenant.",
    ),
)


def permission_codes() -> frozenset[str]:
    """Return every canonical permission code."""

    return frozenset(
        permission.code
        for permission in PERMISSION_CATALOG
    )


__all__ = [
    "PERMISSION_CATALOG",
    "BranchPermissions",
    "BrandPermissions",
    "CompanyPermissions",
    "CustomerPermissions",
    "EmployeePermissions",
    "MachinePermissions",
    "MaterialPermissions",
    "PermissionDefinition",
    "ServicePermissions",
    "SupplierPermissions",
    "permission_codes",
]
