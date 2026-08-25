from modules.pipeline import process_requirement


def main():
    print("=== MindBridge ===")

    user_input = input("\nEnter your requirement:\n> ")

    try:
        result = process_requirement(user_input)

        print("\n--- Structured Requirement ---")
        print(f"Language: {result.language}")
        print(f"Intent: {result.intent}")
        print(f"Task: {result.task}")
        print(f"Context: {result.context}")

        print("\nRequirements:")
        for item in result.requirements:
            print(f"- {item}")

        print("\nConstraints:")
        for item in result.constraints:
            print(f"- {item}")

        print(f"\nExpected Output: {result.expected_output}")

        print("\nEntities:")
        for entity in result.entities:
            print(f"- {entity}")

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()