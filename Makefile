installation:
	( \
	python3.12 -m venv venv; \
	. ./venv/bin/activate; \
	poetry install; \
	)

hw1: installation
	( \
	. ./venv/bin/activate; \
	uvicorn hw.1_asgi:app --host 0.0.0.0 --port 8000 --reload; \
	)
hw2run:
	( \
	. ./venv/bin/activate; \
	uvicorn lecture_2.hw.shop_api.main:app --host 0.0.0.0 --port 8000 --reload; \
	)
hw21runInnerTest:
	( \
	. ./venv/bin/activate; \
	poetry run python ${CURDIR}/lecture_2/hw/ws_rooms.py \
	)
hw21runInnerTest2:
	( \
	. ./venv/bin/activate; \
	poetry run python ${CURDIR}/tests/test_homework_2_1_ws.py \
	)
#hw2run:
#	( \
#	. ./venv/bin/activate; \
#	uvicorn hw.hw2.shop_api.main:app --host 0.0.0.0 --port 8000 --reload; \
#	)
hw2: installation hw2run

run_hw2_my:
	( \
	. ./venv/bin/activate; \
	poetry run python ${CURDIR}/lecture_2/hw/shop_api/main.py \
	)

test_hw1: installation
	( \
	. ./venv/bin/activate; \
	pytest ${CURDIR}/tests/test_homework_1.py \
	)
test_hw2: installation
	( \
	. ./venv/bin/activate; \
	poetry run pytest ${CURDIR}/tests/test_homework_2.py -vv --verbose --strict --showlocals \
	)
test_hw2_ws: installation
	( \
	. ./venv/bin/activate; \
	poetry run pytest ${CURDIR}/tests/test_homework_2_1_ws.py -rxXs -vv --verbose --strict --showlocals \
	)
#test_hw2_my:
#	( \
#	. ./venv/bin/activate; \
#	poetry run pytest ${CURDIR}/tests/test_homework_2_my.py -rxXs -vv --verbose --strict --showlocals \
#	)
test_hw1_vals:
	( \
	. ./venv/bin/activate; \
	pytest ${CURDIR}/tests/test_homework_1_vals.py \
	)