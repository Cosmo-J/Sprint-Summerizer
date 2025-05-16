import re


def text_length(text, avg_line_length=80):
    """
    Determines if the given text is longer than three lines based on average line length.

    Args:
        text (str): The input text to check.
        avg_line_length (int): The average number of characters per line to consider (default is 80).

    Returns:
        bool: True if the text exceeds three lines, False otherwise.
    """
    # Remove any leading/trailing whitespace
    text = text.strip()

    # Calculate the total number of characters in the text
    total_chars = len(text)

    # Calculate the number of lines based on average line length
    estimated_lines = total_chars / avg_line_length

    # Return True if it exceeds three lines, False otherwise
    return estimated_lines > 3

def compress_summary(parsed_data):
    
    """
    Compresses the 'Summary:' section by removing everything from the second subheading onwards.

    Args:
        parsed_data (str): The input text containing the 'Summary:' and other sections.

    Returns:
        str: The compressed text with only the 'Summary:' section.
    """
    # Regex pattern for a subheading (capitalized word followed by a colon)
    subheading_pattern = r"^[A-Z][a-zA-Z\s]*:$"

    # Split text into lines
    lines = parsed_data.split("\n")
    output_lines = []
    subheading_count = 0

    for line in lines:
        # Count subheadings
        if re.match(subheading_pattern, line.strip()):
            subheading_count += 1

        # Stop after the second subheading
        if subheading_count == 2:
            break

        output_lines.append(line)

    # Join the relevant lines back into a single string
    return "\n".join(output_lines)