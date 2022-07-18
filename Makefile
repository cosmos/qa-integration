
install-deps:
	@bash ./scripts/deps/prereq.sh

lint: install-deps
	PYTHONPATH=./internal pylint ./internal

setup-chain: install-deps stop-chain
	@bash ./scripts/chain/start_chain.sh 2
	@echo "Waiting for chain to start..."
	@sleep 7

pause-chain:
	@bash ./scripts/chain/pause_nodes.sh

resume-chain:
	@bash ./scripts/chain/resume_nodes.sh

stop-chain:
	@bash ./scripts/chain/shutdown_nodes.sh

test-all: setup-chain
	@bash ./scripts/chain/node_status.sh
	@bash ./scripts/chain/pause_nodes.sh
	@bash ./scripts/chain/resume_nodes.sh

	@echo "Waiting for chain to resume..."
	@sleep 7

	TEST_TYPE=multi-msg-load bash ./scripts/tests/multi_msg_load.sh -n 50
	TEST_TYPE=query-load bash ./scripts/tests/query_load.sh -n 50
	TEST_TYPE=send-load bash ./scripts/tests/send_load.sh -n 50
	TEST_TYPE=single-msg-load bash ./scripts/tests/single_msg_load.sh -n 50
	$(MAKE) stop-chain

test-all-modules: setup-chain
	@echo "Running all individual module tests..."
	TEST_TYPE=module bash ./scripts/tests/all_modules.sh
	$(MAKE) stop-chain

test-multi-msg: setup-chain
	@echo "Running multi msg load test..."
	TEST_TYPE=multi-msg-load bash ./scripts/tests/multi_msg_load.sh -n 50
	$(MAKE) stop-chain

test-query-load: setup-chain
	@echo "Running query load test..."
	TEST_TYPE=query-load bash ./scripts/tests/query_load.sh -n 50
	$(MAKE) stop-chain

test-send-load: setup-chain
	@echo "Running send msg load test..."
	TEST_TYPE=send-load bash ./scripts/tests/send_load.sh -n 50
	$(MAKE) stop-chain

test-single-msg: setup-chain
	@echo "Running single msg load test..."
	TEST_TYPE=single-msg-load bash ./scripts/tests/single_msg_load.sh -n 50
	$(MAKE) stop-chain
