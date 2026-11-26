# Check commit messages follow Conventional Commits. Usage: just commits [RANGE]
[group('quality')]
commits RANGE="HEAD":
    committed -vv {{ RANGE }}
