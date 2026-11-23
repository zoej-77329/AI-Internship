
import pandas as pd

from src.config import TICKET_FILE


REQUIRED_COLUMNS = [
    "ticket_id",
    "category",
    "query",
    "resolution",
    "status"
]


def load_tickets():
    """Load support tickets from CSV."""

    return pd.read_csv(TICKET_FILE)


def validate_tickets(df):
    """Validate the support-ticket dataset."""

    errors = []

    # Check required columns
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        errors.append(
            f"Missing columns: {missing_columns}"
        )
        return errors

    # Check missing values
    if df[REQUIRED_COLUMNS].isnull().any().any():
        errors.append("Dataset contains missing values.")

    # Check empty text fields
    for col in REQUIRED_COLUMNS:
        if df[col].dtype == "object":
            empty = df[col].astype(str).str.strip().eq("")

            if empty.any():
                errors.append(
                    f"Empty values found in {col}."
                )

    # Check duplicate ticket IDs
    if df["ticket_id"].duplicated().any():
        errors.append("Duplicate ticket IDs found.")

    # Check duplicate queries
    if df["query"].str.strip().str.casefold().duplicated().any():
        errors.append("Duplicate queries found.")

    # Check valid ticket statuses
    valid_statuses = {"Resolved", "Open"}

    invalid_statuses = (
        set(df["status"].dropna().unique()) - valid_statuses
    )

    if invalid_statuses:
        errors.append(
            f"Invalid statuses: {invalid_statuses}"
        )

    return errors


def show_ticket_summary(df):
    """Display ticket dataset statistics."""

    print("\nSUPPORT TICKET SUMMARY")
    print("-" * 35)

    print("Total Tickets:", len(df))

    print("\nCategory Distribution:")
    print(df["category"].value_counts().sort_index())

    print("\nStatus Distribution:")
    print(df["status"].value_counts().sort_index())


def main():
    df = load_tickets()

    errors = validate_tickets(df)

    if errors:
        print("Dataset validation failed:")

        for error in errors:
            print("-", error)

        return

    print("Support tickets loaded successfully!")
    print("All records passed validation.")

    show_ticket_summary(df)


if __name__ == "__main__":
    main()
