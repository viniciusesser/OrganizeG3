"""Unit tests for branch application use cases."""

from __future__ import annotations

from collections.abc import Sequence
import uuid

import pytest

from organizeg3_api.application.branch.schemas import (
    BranchCreate,
    BranchUpdate,
)
from organizeg3_api.application.branch.use_cases import (
    CreateBranchUseCase,
    DeactivateBranchUseCase,
    GetBranchUseCase,
    ListBranchesUseCase,
    ReactivateBranchUseCase,
    UpdateBranchUseCase,
)
from organizeg3_api.core.exceptions import (
    ConflictError,
    NotFoundError,
    ValidationError,
)
from organizeg3_api.domain.branch.entity import (
    Branch,
)


class FakeBranchRepository:
    """In-memory repository used by branch application tests."""

    def __init__(self) -> None:
        self._branches: dict[
            tuple[uuid.UUID, uuid.UUID],
            Branch,
        ] = {}

    def exists_active_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID,
    ) -> bool:
        branch = self._branches.get(
            (
                tenant_id,
                branch_id,
            )
        )

        return (
            branch is not None
            and branch.is_active
        )

    def get_by_id_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        branch_id: uuid.UUID,
    ) -> Branch | None:
        return self._branches.get(
            (
                tenant_id,
                branch_id,
            )
        )

    def list_all(
        self,
        *,
        tenant_id: uuid.UUID,
        include_inactive: bool = False,
        search: str | None = None,
        is_headquarters: bool | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Sequence[Branch]:
        branches = [
            branch
            for (
                stored_tenant_id,
                _
            ),
            branch in self._branches.items()
            if stored_tenant_id
            == tenant_id
        ]

        if not include_inactive:
            branches = [
                branch
                for branch in branches
                if branch.is_active
            ]

        if is_headquarters is not None:
            branches = [
                branch
                for branch in branches
                if branch.is_headquarters
                is is_headquarters
            ]

        normalized_search = (
            search.strip().lower()
            if search is not None
            else ""
        )

        if normalized_search:
            branches = [
                branch
                for branch in branches
                if (
                    normalized_search
                    in branch.code.lower()
                    or normalized_search
                    in branch.name.lower()
                )
            ]

        branches.sort(
            key=lambda branch: (
                not branch.is_headquarters,
                branch.code,
            )
        )

        return branches[
            offset : offset + limit
        ]

    def exists_by_code(
        self,
        *,
        tenant_id: uuid.UUID,
        code: str,
        exclude_branch_id: uuid.UUID | None = None,
    ) -> bool:
        normalized_code = (
            code.strip().upper()
        )

        return any(
            branch.tenant_id
            == tenant_id
            and branch.code
            == normalized_code
            and branch.id
            != exclude_branch_id
            for branch in self._branches.values()
        )

    def exists_headquarters_for_tenant(
        self,
        *,
        tenant_id: uuid.UUID,
        exclude_branch_id: uuid.UUID | None = None,
    ) -> bool:
        return any(
            branch.tenant_id
            == tenant_id
            and branch.is_headquarters
            and branch.id
            != exclude_branch_id
            for branch in self._branches.values()
        )

    def add(
        self,
        branch: Branch,
    ) -> Branch:
        assert branch.id is not None

        self._branches[
            (
                branch.tenant_id,
                branch.id,
            )
        ] = branch

        return branch

    def save(
        self,
        branch: Branch,
    ) -> Branch:
        assert branch.id is not None

        self._branches[
            (
                branch.tenant_id,
                branch.id,
            )
        ] = branch

        return branch


def test_creates_branch() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeBranchRepository()

    branch = CreateBranchUseCase(
        repository
    ).execute(
        tenant_id,
        BranchCreate(
            code=" matriz ",
            name=" Matriz ",
            email=" MATRIZ@EXAMPLE.COM ",
            phone="(18) 3222-1234",
            state="sp",
            postal_code="19273-000",
            is_headquarters=True,
        ),
    )

    assert branch.id is not None
    assert branch.tenant_id == tenant_id
    assert branch.code == "MATRIZ"
    assert branch.name == "Matriz"
    assert branch.email == "matriz@example.com"
    assert branch.phone == "1832221234"
    assert branch.state == "SP"
    assert branch.postal_code == "19273000"
    assert branch.is_headquarters is True


def test_rejects_duplicate_branch_code() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeBranchRepository()

    repository.add(
        Branch.create(
            tenant_id=tenant_id,
            code="FILIAL-01",
            name="Filial 01",
        )
    )

    with pytest.raises(
        ConflictError,
        match="código",
    ):
        CreateBranchUseCase(
            repository
        ).execute(
            tenant_id,
            BranchCreate(
                code=" filial-01 ",
                name="Outra Filial",
            ),
        )


def test_rejects_second_headquarters() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeBranchRepository()

    repository.add(
        Branch.create(
            tenant_id=tenant_id,
            code="MATRIZ",
            name="Matriz",
            is_headquarters=True,
        )
    )

    with pytest.raises(
        ConflictError,
        match="matriz",
    ):
        CreateBranchUseCase(
            repository
        ).execute(
            tenant_id,
            BranchCreate(
                code="MATRIZ-02",
                name="Outra Matriz",
                is_headquarters=True,
            ),
        )


def test_gets_branch() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeBranchRepository()

    expected = repository.add(
        Branch.create(
            tenant_id=tenant_id,
            code="FILIAL",
            name="Filial",
        )
    )

    assert expected.id is not None

    branch = GetBranchUseCase(
        repository
    ).execute(
        tenant_id,
        expected.id,
    )

    assert branch is expected


def test_get_rejects_branch_from_other_tenant() -> None:
    tenant_a_id = uuid.uuid4()
    tenant_b_id = uuid.uuid4()

    repository = FakeBranchRepository()

    branch = repository.add(
        Branch.create(
            tenant_id=tenant_a_id,
            code="FILIAL",
            name="Filial",
        )
    )

    assert branch.id is not None

    with pytest.raises(
        NotFoundError,
        match="Filial não encontrada",
    ):
        GetBranchUseCase(
            repository
        ).execute(
            tenant_b_id,
            branch.id,
        )


def test_lists_active_branches_by_default() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeBranchRepository()

    repository.add(
        Branch.create(
            tenant_id=tenant_id,
            code="ATIVA",
            name="Filial Ativa",
        )
    )

    inactive = repository.add(
        Branch.create(
            tenant_id=tenant_id,
            code="INATIVA",
            name="Filial Inativa",
        )
    )

    inactive.deactivate()

    branches = ListBranchesUseCase(
        repository
    ).execute(
        tenant_id
    )

    assert [
        branch.code
        for branch in branches
    ] == [
        "ATIVA",
    ]


def test_lists_with_search_and_pagination() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeBranchRepository()

    for index in range(3):
        repository.add(
            Branch.create(
                tenant_id=tenant_id,
                code=f"FILIAL-{index}",
                name=f"Unidade {index}",
            )
        )

    branches = ListBranchesUseCase(
        repository
    ).execute(
        tenant_id,
        search="unidade",
        limit=1,
        offset=1,
    )

    assert len(branches) == 1
    assert branches[0].code == "FILIAL-1"


def test_updates_branch_profile() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeBranchRepository()

    branch = repository.add(
        Branch.create(
            tenant_id=tenant_id,
            code="FILIAL",
            name="Filial Antiga",
            email="antigo@example.com",
        )
    )

    assert branch.id is not None

    updated = UpdateBranchUseCase(
        repository
    ).execute(
        tenant_id,
        branch.id,
        BranchUpdate(
            code=" nova ",
            name=" Nova Filial ",
            email=" NOVO@EXAMPLE.COM ",
        ),
    )

    assert updated.code == "NOVA"
    assert updated.name == "Nova Filial"
    assert updated.email == "novo@example.com"


def test_update_can_clear_optional_field() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeBranchRepository()

    branch = repository.add(
        Branch.create(
            tenant_id=tenant_id,
            code="FILIAL",
            name="Filial",
            legal_name="Empresa Filial LTDA",
        )
    )

    assert branch.id is not None

    updated = UpdateBranchUseCase(
        repository
    ).execute(
        tenant_id,
        branch.id,
        BranchUpdate(
            legal_name=None,
        ),
    )

    assert updated.legal_name is None


def test_update_rejects_empty_payload() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeBranchRepository()

    branch = repository.add(
        Branch.create(
            tenant_id=tenant_id,
            code="FILIAL",
            name="Filial",
        )
    )

    assert branch.id is not None

    with pytest.raises(
        ValidationError,
        match="ao menos um campo",
    ):
        UpdateBranchUseCase(
            repository
        ).execute(
            tenant_id,
            branch.id,
            BranchUpdate(),
        )


def test_update_rejects_duplicate_code() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeBranchRepository()

    branch_a = repository.add(
        Branch.create(
            tenant_id=tenant_id,
            code="FILIAL-A",
            name="Filial A",
        )
    )

    repository.add(
        Branch.create(
            tenant_id=tenant_id,
            code="FILIAL-B",
            name="Filial B",
        )
    )

    assert branch_a.id is not None

    with pytest.raises(
        ConflictError,
        match="código",
    ):
        UpdateBranchUseCase(
            repository
        ).execute(
            tenant_id,
            branch_a.id,
            BranchUpdate(
                code="FILIAL-B",
            ),
        )


def test_update_rejects_second_headquarters() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeBranchRepository()

    repository.add(
        Branch.create(
            tenant_id=tenant_id,
            code="MATRIZ",
            name="Matriz",
            is_headquarters=True,
        )
    )

    branch = repository.add(
        Branch.create(
            tenant_id=tenant_id,
            code="FILIAL",
            name="Filial",
        )
    )

    assert branch.id is not None

    with pytest.raises(
        ConflictError,
        match="matriz",
    ):
        UpdateBranchUseCase(
            repository
        ).execute(
            tenant_id,
            branch.id,
            BranchUpdate(
                is_headquarters=True,
            ),
        )


def test_deactivates_and_reactivates_branch() -> None:
    tenant_id = uuid.uuid4()
    repository = FakeBranchRepository()

    branch = repository.add(
        Branch.create(
            tenant_id=tenant_id,
            code="FILIAL",
            name="Filial",
        )
    )

    assert branch.id is not None

    deactivated = DeactivateBranchUseCase(
        repository
    ).execute(
        tenant_id,
        branch.id,
    )

    assert deactivated.is_active is False

    reactivated = ReactivateBranchUseCase(
        repository
    ).execute(
        tenant_id,
        branch.id,
    )

    assert reactivated.is_active is True
