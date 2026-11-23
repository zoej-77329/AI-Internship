
import json
from collections import Counter

from src.config import FAQ_FILE


def load_faqs():
    """Load FAQ records from the JSON file."""

    with open(FAQ_FILE, "r", encoding="utf-8") as file:
        faqs = json.load(file)

    return faqs


def validate_faqs(faqs):
    """Validate FAQ records and check for duplicate entries."""

    required_fields = {
        "id",
        "category",
        "question",
        "answer"
    }

    errors = []
    seen_ids = set()
    seen_questions = set()

    for index, faq in enumerate(faqs):

        if not isinstance(faq, dict):
            errors.append(f"Record {index + 1} is not an object.")
            continue

        missing = required_fields - faq.keys()

        if missing:
            errors.append(
                f"Record {index + 1} is missing: {missing}"
            )
            continue

        if not isinstance(faq["id"], int) or isinstance(faq["id"], bool):
            errors.append(f"Invalid ID in record {index + 1}.")
        elif faq["id"] in seen_ids:
            errors.append(f"Duplicate ID: {faq['id']}")
        else:
            seen_ids.add(faq["id"])

        for field in ("category", "question", "answer"):
            if not isinstance(faq[field], str) or not faq[field].strip():
                errors.append(
                    f"Empty or invalid {field} in record {index + 1}."
                )

        question = faq["question"].strip().casefold()

        if question in seen_questions:
            errors.append(
                f"Duplicate question: {faq['question']}"
            )

        seen_questions.add(question)

    return errors


def show_summary(faqs):
    """Display dataset statistics."""

    categories = Counter(
        faq["category"] for faq in faqs
    )

    print("\nFAQ DATASET SUMMARY")
    print("-" * 35)

    print("Total FAQs:", len(faqs))

    print("\nCategory Distribution:")

    for category, count in sorted(categories.items()):
        print(f"{category}: {count}")


def main():
    faqs = load_faqs()

    errors = validate_faqs(faqs)

    if errors:
        print("Dataset validation failed:")

        for error in errors:
            print("-", error)

        return

    print("FAQ dataset loaded successfully!")
    print("All records passed validation.")

    show_summary(faqs)


if __name__ == "__main__":
    main()
