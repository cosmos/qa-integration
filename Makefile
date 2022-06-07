NUM_VALS = 2

install-deps:
	bash ./deps/prereq.sh

lint: install-deps
	pylint ./python-qa-tools

setup-chain: install-deps
	bash ./node-management/shutdown_nodes.sh $(NUM_VALS)
	bash ./provision/start_chain.sh $(NUM_VALS) 2
	@echo "Waiting for chain to start..."
	sleep 10

test-all: install-deps setup-chain
	@bash ./node-management/node_status.sh $(NUM_VALS)
	@bash ./node-management/pause_nodes.sh $(NUM_VALS)
	@bash ./node-management/resume_nodes.sh $(NUM_VALS)

	@echo "Waiting for chain to resume..."
	@sleep 10

	@bash ./load-test/multi_msg_load.sh -n 50
	@bash ./load-test/query_load.sh -n 50
	@bash ./load-test/send_load.sh -n 50
	@bash ./load-test/single_msg_load.sh -n 50
	@bash ./node-management/shutdown_nodes.sh $(NUM_VALS)

test-multi-msg: install-deps setup-chain
	@echo "Running multi msg load test..."
	@bash ./load-test/multi_msg_load.sh -n 50

test-query-load: install-deps setup-chain
	@echo "Running query load test..."
	@bash ./load-test/query_load.sh -n 50

test-send-load: install-deps setup-chain
	@echo "Running send msg load test..."
	@bash ./load-test/send_load.sh -n 50

test-single-msg: install-deps setup-chain
	@echo "Running single msg load test..."
	@bash ./load-test/single_msg_load.sh -n 50
