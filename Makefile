NUM_VALS=3

docker-build:
	@bash ./scripts/build_binary.sh

init-testnet:
	@bash ./scripts/init_chain.sh 

start-docker-chain:
	docker-compose up -d

stop-docker-chain:
	docker-compose stop 

clean-docker-chain:
	docker-compose down -v

restart-docker-chain:
	docker-compose restart 

install-deps:
	@bash ./scripts/deps/prereq.sh

lint: install-deps
	PYTHONPATH=./internal pylint ./internal

setup-chain: install-deps stop-chain
	@bash ./scripts/chain/start_chain.sh 2
	@echo "Waiting for chain to start..."
	@sleep 7

test-all: start-docker-chain
	@sleep 5
	@bash ./scripts/chain/node_status.sh $(NUM_VALS)
	$(MAKE) stop-docker-chain
	@echo "Waiting for chain to restart..."
	$(MAKE) restart-docker-chain
	@sleep 7
	TEST_TYPE=multi-msg-load bash ./scripts/tests/multi_msg_load.sh
	TEST_TYPE=query-load bash ./scripts/tests/query_load.sh
	TEST_TYPE=send-load bash ./scripts/tests/send_load.sh
	TEST_TYPE=single-msg-load bash ./scripts/tests/single_msg_load.sh
	$(MAKE) stop-docker-chain

test-all-modules: start-docker-chain
	@echo "Running all individual module tests..."
	TEST_TYPE=module bash ./scripts/tests/all_modules.sh
	$(MAKE) stop-docker-chain

test-multi-msg: start-docker-chain
	@echo "Running multi msg load test..."
	TEST_TYPE=multi-msg-load bash ./scripts/tests/multi_msg_load.sh
	$(MAKE) stop-docker-chain

test-query-load: start-docker-chain
	@echo "Running query load test..."
	TEST_TYPE=query-load bash ./scripts/tests/query_load.sh
	$(MAKE) stop-docker-chain

test-send-load: start-docker-chain
	@echo "Running send msg load test..."
	TEST_TYPE=send-load bash ./scripts/tests/send_load.sh
	$(MAKE) stop-docker-chain

test-single-msg: start-docker-chain
	@echo "Running single msg load test..."
	TEST_TYPE=single-msg-load bash ./scripts/tests/single_msg_load.sh
	$(MAKE) stop-docker-chain
