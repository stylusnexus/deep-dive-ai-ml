.PHONY: up down torch keras logs check notebooks sop

up:    ; docker compose -f docker/compose.yaml up -d
down:  ; docker compose -f docker/compose.yaml down
torch: ; docker compose -f docker/compose.yaml up -d torch mlflow
keras: ; docker compose -f docker/compose.yaml up -d keras mlflow
logs:  ; docker compose -f docker/compose.yaml logs -f
check: ; bash scripts/check-env.sh
notebooks: ; python3 scripts/check_notebooks.py
sop: ; python3 scripts/build_sop.py
