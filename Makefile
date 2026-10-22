.PHONY: up down torch keras logs check notebooks sop glossary links lessons numbers seo verify

up:    ; docker compose -f docker/compose.yaml up -d
down:  ; docker compose -f docker/compose.yaml down
torch: ; docker compose -f docker/compose.yaml up -d torch mlflow
keras: ; docker compose -f docker/compose.yaml up -d keras mlflow
logs:  ; docker compose -f docker/compose.yaml logs -f
check: ; bash scripts/check-env.sh
notebooks: ; python3 scripts/check_notebooks.py
sop: ; python3 scripts/build_sop.py
glossary: ; python3 scripts/check_glossary.py
links: ; python3 scripts/check_links.py
numbers: ; python3 scripts/check_numbers.py
seo: ; python3 scripts/build_seo.py
lessons: ; @for m in $$(ls scripts/content/*.py | xargs -n1 basename | sed 's/\.py//' | grep -v _notebooks); do python3 scripts/build_lessons.py $$m; done; python3 scripts/build_index.py; python3 scripts/build_knows.py; python3 scripts/build_seo.py
verify: glossary links numbers notebooks
