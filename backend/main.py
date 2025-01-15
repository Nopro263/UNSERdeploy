from deploy import parse_text

with open("example.yml") as f:
    print(parse_text(f.read()))