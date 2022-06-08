NUM_VALS = 2

install-deps:
	bash ./deps/prereq.sh

lint: install-deps
	pylint ./python-qa-tools

setup-chains: install-deps
	@bash ./provision/start_chain.sh $(NUM_VALS) 2
	@echo "Waiting for chain to start..."
	sleep 10

stop-chains:
	@bash ./node-management/shutdown_nodes.sh $(NUM_VALS)

test-all: setup-chains
	@bash ./node-management/node_status.sh $(NUM_VALS)
	@bash ./node-management/pause_nodes.sh $(NUM_VALS)
	@bash ./node-management/resume_nodes.sh $(NUM_VALS)

	@echo "Waiting for chain to resume..."
	@sleep 10

	@bash ./load-test/multi_msg_load.sh -n 50
	@bash ./load-test/query_load.sh -n 50
	@bash ./load-test/send_load.sh -n 50
	@bash ./load-test/single_msg_load.sh -n 50
	$(MAKE) stop-chains

test-multi-msg: setup-chains
	@echo "Running multi msg load test..."
	. ./load-test/multi_msg_load.sh -n 50
	$(MAKE) stop-chains

test-query-load: setup-chains
	@echo "Running query load test..."
	. ./load-test/query_load.sh -n 50
	$(MAKE) stop-chains

test-send-load: setup-chains
	@echo "Running send msg load test..."
	. ./load-test/send_load.sh -n 50
	$(MAKE) stop-chains

test-single-msg: setup-chains
	@echo "Running single msg load test..."
	. ./load-test/single_msg_load.sh -n 50
	$(MAKE) stop-chains
