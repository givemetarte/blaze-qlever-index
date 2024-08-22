# Qlever index from Blazegraph data

### How to run

- NOTE: Run blazegraph before running the codes

- `--endpoint`: blazegraph SPARQL endpoint
- `--port`: port number for qlever server (default: 7000)
- `--name`: qlever server name (default: random 6 digits)

```bash
# env
python -m venv env
source env/bin/activate
pip install -r requirements.txt
# run main.py
python main.py --endpoint=http://localhost:9999/blazegraph/namespace/test/sparql --port=7080 --name=test
```

### SPARQL query

- NOTE: Check qlever server is open
- {port}: replace the port number

```bash
curl -s http://localhost:{port} \
  -H "Accept:text/csv" \
  -H "Content-type: application/sparql-query" \
  --data "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?label WHERE { ?s rdfs:label ?label . } LIMIT 10"
```

### run qlever (command line)

```bash
qlever get-data
qlever index
qlever index-stats
qlever start
qlever ui
```
