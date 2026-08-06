"""Generate read-only customer data audit reports."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import UTC, datetime
import json
import os
from pathlib import Path
import sys
from typing import Literal, cast

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from organizeg3_api.application.customer.data_audit import (
    CustomerAuditReport,
    CustomerDataAuditor,
)
from organizeg3_api.infrastructure.persistence.repositories.customer_audit_repository import (
    SQLAlchemyCustomerAuditRepository,
)

OutputFormat = Literal[
    "json",
    "csv",
    "both",
]

_BLOCKING_ISSUES_EXIT_CODE = 2


@dataclass(
    frozen=True,
    slots=True,
)
class AuditCommandOptions:
    """Validated CLI options."""

    database_url: str
    output_directory: Path
    output_format: OutputFormat
    fail_on_blockers: bool


def write_console(
    message: str = "",
) -> None:
    """Write one line to the command-line output."""

    sys.stdout.write(
        f"{message}\n"
    )


def parse_options() -> AuditCommandOptions:
    """Parse and validate command-line arguments."""

    load_dotenv()

    parser = argparse.ArgumentParser(
        description=(
            "Audita os dados legados de clientes "
            "sem realizar alterações no banco."
        )
    )

    parser.add_argument(
        "--database-url",
        help=(
            "URL SQLAlchemy. Quando omitida, usa "
            "DATABASE_URL do ambiente ou .env."
        ),
    )

    parser.add_argument(
        "--output-dir",
        default="reports",
        help=(
            "Diretório de saída dos relatórios."
        ),
    )

    parser.add_argument(
        "--format",
        choices=(
            "json",
            "csv",
            "both",
        ),
        default="both",
        help="Formato do relatório.",
    )

    parser.add_argument(
        "--fail-on-blockers",
        action="store_true",
        help=(
            "Retorna código 2 quando houver "
            "problemas que bloqueiam índices únicos."
        ),
    )

    namespace = parser.parse_args()

    argument_database_url = cast(
        str | None,
        namespace.database_url,
    )

    database_url = (
        argument_database_url
        or os.getenv("DATABASE_URL")
    )

    if not database_url:
        parser.error(
            "Informe --database-url ou defina "
            "DATABASE_URL no ambiente/.env."
        )

    return AuditCommandOptions(
        database_url=database_url,
        output_directory=Path(
            cast(
                str,
                namespace.output_dir,
            )
        ),
        output_format=cast(
            OutputFormat,
            namespace.format,
        ),
        fail_on_blockers=cast(
            bool,
            namespace.fail_on_blockers,
        ),
    )


def write_json_report(
    report: CustomerAuditReport,
    destination: Path,
) -> None:
    """Write the complete JSON audit report."""

    destination.write_text(
        json.dumps(
            report.to_dict(),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def write_csv_report(
    report: CustomerAuditReport,
    destination: Path,
) -> None:
    """Write one CSV row for every audit issue."""

    fieldnames = [
        "code",
        "severity",
        "message",
        "tenant_id",
        "customer_ids",
        "field",
        "raw_value",
        "normalized_value",
        "blocks_unique_index",
    ]

    with destination.open(
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as output_file:
        writer = csv.DictWriter(
            output_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for issue in report.issues:
            writer.writerow(
                {
                    "code": issue.code.value,
                    "severity": (
                        issue.severity.value
                    ),
                    "message": issue.message,
                    "tenant_id": (
                        issue.tenant_id or ""
                    ),
                    "customer_ids": ";".join(
                        str(customer_id)
                        for customer_id
                        in issue.customer_ids
                    ),
                    "field": issue.field or "",
                    "raw_value": (
                        issue.raw_value or ""
                    ),
                    "normalized_value": (
                        issue.normalized_value
                        or ""
                    ),
                    "blocks_unique_index": (
                        issue.blocks_unique_index
                    ),
                }
            )


def print_summary(
    report: CustomerAuditReport,
) -> None:
    """Write a human-readable report summary."""

    summary = report.summary()

    summary_lines = [
        "",
        "Auditoria de clientes concluída",
        "=" * 40,
        (
            "Registros analisados: "
            f"{summary['records_scanned']}"
        ),
        (
            "Registros ativos: "
            f"{summary['active_records']}"
        ),
        (
            "Registros arquivados: "
            f"{summary['archived_records']}"
        ),
        (
            "Problemas encontrados: "
            f"{summary['issue_count']}"
        ),
        (
            "Erros: "
            f"{summary['error_count']}"
        ),
        (
            "Avisos: "
            f"{summary['warning_count']}"
        ),
        (
            "Bloqueios para índice único: "
            f"{summary['blocking_issue_count']}"
        ),
        (
            "Grupos de CPF/CNPJ duplicados: "
            f"{summary['duplicate_document_groups']}"
        ),
        (
            "Grupos de e-mails duplicados: "
            f"{summary['duplicate_email_groups']}"
        ),
    ]

    for line in summary_lines:
        write_console(line)


def run_audit(
    options: AuditCommandOptions,
) -> int:
    """Run the read-only audit and write reports."""

    engine = create_engine(
        options.database_url,
        pool_pre_ping=True,
    )

    try:
        with Session(
            engine,
            autoflush=False,
            expire_on_commit=False,
        ) as session:
            if (
                engine.dialect.name
                == "postgresql"
            ):
                session.execute(
                    text(
                        "SET TRANSACTION READ ONLY"
                    )
                )

            records = (
                SQLAlchemyCustomerAuditRepository(
                    session
                ).fetch_all()
            )

            report = CustomerDataAuditor().audit(
                records
            )

        options.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.now(
            UTC
        ).strftime(
            "%Y%m%d_%H%M%S"
        )

        base_name = (
            f"customer_data_audit_{timestamp}"
        )

        if options.output_format in {
            "json",
            "both",
        }:
            json_path = (
                options.output_directory
                / f"{base_name}.json"
            )

            write_json_report(
                report,
                json_path,
            )

            write_console(
                f"JSON: {json_path.resolve()}"
            )

        if options.output_format in {
            "csv",
            "both",
        }:
            csv_path = (
                options.output_directory
                / f"{base_name}.csv"
            )

            write_csv_report(
                report,
                csv_path,
            )

            write_console(
                f"CSV: {csv_path.resolve()}"
            )

        print_summary(report)

        if (
            options.fail_on_blockers
            and report.blocking_issue_count > 0
        ):
            return _BLOCKING_ISSUES_EXIT_CODE

        return 0

    finally:
        engine.dispose()


def main() -> int:
    """Run the command-line audit."""

    return run_audit(
        parse_options()
    )


if __name__ == "__main__":
    raise SystemExit(main())
