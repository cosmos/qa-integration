NUM_VALS = 2

install-deps:
	@bash ./scripts/deps/prereq.sh

lint: install-deps
	pylint ./internal

setup-chain: install-deps stop-chain
	@bash ./provision/start_chain.sh $(NUM_VALS) 2
	@echo "Waiting for chain to start..."
	@sleep 7

pause-chain:
	@bash ./scripts/chain/pause_nodes.sh $(NUM_VALS)

resume-chain:
	@bash ./scripts/chain/resume_nodes.sh $(NUM_VALS)

stop-chain:
	@bash ./scripts/chain/shutdown_nodes.sh $(NUM_VALS)

test-all: setup-chain
	@bash ./scripts/chain/node_status.sh $(NUM_VALS)
	@bash ./scripts/chain/pause_nodes.sh $(NUM_VALS)
	@bash ./scripts/chain/resume_nodes.sh $(NUM_VALS)

	@echo "Waiting for chain to resume..."
	@sleep 7

	TEST_TYPE=multi-msg-load bash ./scripts/load-test/multi_msg_load.sh -n 50
	TEST_TYPE=query-load bash ./scripts/load-test/query_load.sh -n 50
	TEST_TYPE=send-load bash ./scripts/load-test/send_load.sh -n 50
	TEST_TYPE=single-msg-load bash ./scripts/load-test/single_msg_load.sh -n 50
	$(MAKE) stop-chain

test-multi-msg: setup-chain
	@echo "Running multi msg load test..."
	TEST_TYPE=multi-msg-load bash ./scripts/load-test/multi_msg_load.sh -n 50
	$(MAKE) stop-chain

test-query-load: setup-chain
	@echo "Running query load test..."
	TEST_TYPE=query-load bash ./scripts/load-test/query_load.sh -n 50
	$(MAKE) stop-chain

test-send-load: setup-chain
	@echo "Running send msg load test..."
	TEST_TYPE=send-load bash ./scripts/load-test/send_load.sh -n 50
	$(MAKE) stop-chain

test-single-msg: setup-chain
	@echo "Running single msg load test..."
	TEST_TYPE=single-msg-load bash ./scripts/load-test/single_msg_load.sh -n 50
	$(MAKE) stop-chain
