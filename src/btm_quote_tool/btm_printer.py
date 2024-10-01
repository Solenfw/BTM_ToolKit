def print_btm_3d():
    """
    Prints a 3D block representation of the letters 'B', 'T', and 'M'.
    """
    b = [
        "BBBB ",
        "B   B",
        "BBBB ",
        "B   B",
        "BBBB "
    ]

    t = [
        "TTTTT",
        "  T  ",
        "  T  ",
        "  T  ",
        "  T  "
    ]

    m = [
        "M   M",
        "MM MM",
        "M M M",
        "M   M",
        "M   M"
    ]

    # Print the letters in block form side by side
    for line in zip(b, t, m):
        print("   ".join(line))