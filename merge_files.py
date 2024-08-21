import glob

path = "/Volumes/data/2023-09-address/data/nov-2023-rdf/datahub-ttl/rna-name-address/full-address"

merged_file_path = "merged_file.ttl"

header_lines = [
    "@prefix dct: <http://purl.org/dc/terms/> .\n",
    "@prefix koag: <http://vocab.datahub.kr/def/address/> .\n",
    "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n",
    "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n",
]

ttl_files = glob.glob(f"{path}/*.ttl")

with open(merged_file_path, "w", encoding="utf-8") as merged_file:
    # 맨 앞에 4줄 추가
    merged_file.writelines(header_lines)

    for file in ttl_files:
        print(f"{file} 파일을 병합 중입니다.")
        with open(file, "r", encoding="utf-8") as f:
            # 파일의 첫 4줄을 건너뛰고 나머지 줄을 읽음
            lines = f.readlines()[4:]
            # 병합 파일에 줄 단위로 내용을 작성
            merged_file.writelines(lines)

print("파일 병합이 완료되었습니다.")
