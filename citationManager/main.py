import re


def main():
    # Initialize any necessary variables or objects
    # Import and read the contents of a text file
    with open("input.txt", "r") as file:
        text_content = file.read()

    with open("citations.txt", "r") as file:
        citations = file.read()

    counter = 1

    def increment_counter(_):
        nonlocal counter
        result = f"[{counter}]"
        counter += 1
        return result

    text_content = re.sub(
        r"LINK",
        increment_counter,
        text_content,
    )
    # print(counter)

    counter = 1
    citations = re.sub(
        r"\[.*?\]",
        increment_counter,
        citations,
    )
    # print(counter)

    # print(text_content)
    # print(citations)

    # Append citations to text_content
    combined_content = text_content + "\n\nCitations:\n" + citations

    # Export to new txt file
    with open("output.txt", "w") as output_file:
        output_file.write(combined_content)

    # Main program logic
    pass


if __name__ == "__main__":
    main()
