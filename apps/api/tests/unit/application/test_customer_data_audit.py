"""Unit tests for legacy customer data auditing."""

import pytest

from organizeg3_api.application.customer.data_audit import (
    AuditIssueCode,
    CustomerAuditRecord,
    CustomerDataAuditor,
)

pytestmark = pytest.mark.unit


def make_record(
    customer_id: int,
    *,
    tenant_id: str | None = (
        "11111111-1111-1111-1111-111111111111"
    ),
    code: str | None = "CUST-0001",
    name: str | None = "Cliente",
    customer_type: str | None = "INDIVIDUAL",
    document_number: str | None = None,
    email: str | None = None,
    phone: str | None = None,
    is_archived: bool = False,
) -> CustomerAuditRecord:
    return CustomerAuditRecord(
        customer_id=customer_id,
        tenant_id=tenant_id,
        code=code,
        name=name,
        customer_type=customer_type,
        document_number=document_number,
        email=email,
        phone=phone,
        is_archived=is_archived,
    )


def test_reports_missing_required_fields() -> None:
    report = CustomerDataAuditor().audit(
        [
            make_record(
                1,
                tenant_id=None,
                code="   ",
                name=None,
                customer_type="UNKNOWN",
            )
        ]
    )

    codes = {
        issue.code
        for issue in report.issues
    }

    assert (
        AuditIssueCode.MISSING_TENANT_ID
        in codes
    )
    assert AuditIssueCode.MISSING_CODE in codes
    assert AuditIssueCode.MISSING_NAME in codes
    assert (
        AuditIssueCode.INVALID_CUSTOMER_TYPE
        in codes
    )
    assert report.blocking_issue_count == 1


def test_reports_non_normalized_contacts() -> None:
    report = CustomerDataAuditor().audit(
        [
            make_record(
                1,
                document_number=(
                    "529.982.247-25"
                ),
                email=(
                    "  CLIENTE@EXAMPLE.COM  "
                ),
                phone=(
                    "+55 (18) 99999-0000"
                ),
            )
        ]
    )

    codes = {
        issue.code
        for issue in report.issues
    }

    assert (
        AuditIssueCode
        .NON_NORMALIZED_DOCUMENT
        in codes
    )
    assert (
        AuditIssueCode
        .NON_NORMALIZED_EMAIL
        in codes
    )
    assert (
        AuditIssueCode
        .NON_NORMALIZED_PHONE
        in codes
    )
    assert report.error_count == 0
    assert report.warning_count == 3


def test_reports_invalid_contacts_and_type_mismatch() -> None:
    report = CustomerDataAuditor().audit(
        [
            make_record(
                1,
                document_number="123",
                email="email inválido",
                phone="9999-0000",
            ),
            make_record(
                2,
                customer_type="CORPORATE",
                document_number=(
                    "529.982.247-25"
                ),
            ),
        ]
    )

    codes = {
        issue.code
        for issue in report.issues
    }

    assert (
        AuditIssueCode.INVALID_DOCUMENT
        in codes
    )
    assert AuditIssueCode.INVALID_EMAIL in codes
    assert AuditIssueCode.INVALID_PHONE in codes
    assert (
        AuditIssueCode
        .DOCUMENT_TYPE_MISMATCH
        in codes
    )


def test_reports_duplicates_inside_same_tenant() -> None:
    report = CustomerDataAuditor().audit(
        [
            make_record(
                1,
                document_number=(
                    "529.982.247-25"
                ),
                email="cliente@example.com",
            ),
            make_record(
                2,
                document_number="52998224725",
                email="CLIENTE@EXAMPLE.COM",
            ),
        ]
    )

    duplicate_issues = [
        issue
        for issue in report.issues
        if issue.code
        in {
            AuditIssueCode.DUPLICATE_DOCUMENT,
            AuditIssueCode.DUPLICATE_EMAIL,
        }
    ]

    assert len(duplicate_issues) == 2
    assert report.blocking_issue_count == 2
    assert (
        report.duplicate_document_groups
        == 1
    )
    assert report.duplicate_email_groups == 1


def test_same_identity_in_different_tenants_is_not_duplicate() -> None:
    report = CustomerDataAuditor().audit(
        [
            make_record(
                1,
                tenant_id=(
                    "11111111-1111-1111-1111-111111111111"
                ),
                document_number="52998224725",
                email="cliente@example.com",
            ),
            make_record(
                2,
                tenant_id=(
                    "22222222-2222-2222-2222-222222222222"
                ),
                document_number="52998224725",
                email="cliente@example.com",
            ),
        ]
    )

    codes = {
        issue.code
        for issue in report.issues
    }

    assert (
        AuditIssueCode.DUPLICATE_DOCUMENT
        not in codes
    )
    assert (
        AuditIssueCode.DUPLICATE_EMAIL
        not in codes
    )


def test_archived_customer_participates_in_duplicate_detection() -> None:
    report = CustomerDataAuditor().audit(
        [
            make_record(
                1,
                document_number="52998224725",
            ),
            make_record(
                2,
                document_number=(
                    "529.982.247-25"
                ),
                is_archived=True,
            ),
        ]
    )

    duplicate = next(
        issue
        for issue in report.issues
        if issue.code
        is AuditIssueCode.DUPLICATE_DOCUMENT
    )

    assert duplicate.customer_ids == (1, 2)
    assert report.active_records == 1
    assert report.archived_records == 1

def test_reports_null_uuid_tenant_as_blocker() -> None:
    report = CustomerDataAuditor().audit(
        [
            make_record(
                1,
                tenant_id=(
                    "00000000-0000-0000-0000-000000000000"
                ),
            )
        ]
    )

    missing_tenant_issue = next(
        issue
        for issue in report.issues
        if issue.code
        is AuditIssueCode.MISSING_TENANT_ID
    )

    assert missing_tenant_issue.customer_ids == (1,)
    assert (
        missing_tenant_issue.blocks_unique_index
        is True
    )
    assert report.blocking_issue_count == 1
