"""Interactive CLI for Drug Interaction Knowledge Graph."""

from agent import answer_query, KNOWN_DRUGS


def main():
    print("=" * 55)
    print("  💊 Drug Interaction Knowledge Graph")
    print("=" * 55)
    print(f"  Known drugs: {', '.join(KNOWN_DRUGS)}")
    print("  Type 'quit' to exit.\n")

    while True:
        try:
            query = input("🔎 Query: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not query:
            continue
        if query.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        print()
        print(answer_query(query))
        print("-" * 55)


if __name__ == "__main__":
    main()
