from deploy import parse_text, create_deployment

with open("example.yml") as f:
    create_deployment("example", parse_text(f.read()))