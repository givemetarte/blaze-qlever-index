# Blazegraph 데이터로 qlever index 생성하기

### 실행방법

- `--endpoint`: blazegraph의 SPARQL endpoint 입력
- `--port`: index 서버를 실행할 포트 입력
- `--name`: index 서버의 이름 입력

```bash
python main.py --endpoint=http://165.194.115.79:9999/blazegraph/namespace/test/sparql --port=7080 --name=hike
```

### SPARQL 질의

- index 서버가 무사히 실행된 후 터미널에서 아래 코드 실행
- {port}는 본인이 입력한 포트로 수정

```bash
curl -s http://localhost:{port} \
  -H "Accept:text/csv" \
  -H "Content-type: application/sparql-query" \
  --data "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?label WHERE { ?s rdfs:label ?label . } LIMIT 10"
```

### qlever 실행

```bash
qlever get-data
qlever index
qlever index-stats
qlever start
qlever ui
```
