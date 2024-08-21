# Qlever

### qlever 실행

```bash
qlever get-data
qlever index
qlever index-stats
qlever start
qlever ui
```

### SPARQL 질의

```bash
curl -s http://localhost:7001 \
  -H "Accept:text/csv" \
  -H "Content-type: application/sparql-query" \
  --data "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX koag: <http://vocab.datahub.kr/def/address/> SELECT ?label WHERE { ?s rdfs:label ?label . } LIMIT 10"
```
