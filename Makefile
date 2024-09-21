installpoetry:
	( \
	python3 -m venv venv; \
	. ./venv/bin/activate; \
	poetry install; \
	)

hw1: installpoetry
	( \
	. ./venv/bin/activate; \
	uvicorn hw.1_asgi:app --host 0.0.0.0 --port 8000 --reload; \
	)

test_hw1:
	( \
	. ./venv/bin/activate; \
	pytest ${CURDIR}/tests/test_homework_1.py \
	)
test_hw1_vals:
	( \
	. ./venv/bin/activate; \
	pytest ${CURDIR}/tests/test_homework_1_vals.py \
	)