NUM_VALS = 3

docker-build:
	@bash ./scripts/build_binary.sh

start-docker-chain:
	docker-compose up -d

pause-docker-chain:
	docker-compose pause

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

pause-chain:
	@bash ./scripts/chain/pause_nodes.sh

resume-chain:
	@bash ./scripts/chain/resume_nodes.sh

stop-chain:
	@bash ./scripts/chain/shutdown_nodes.sh

test-all:
	# @bash ./scripts/chain/node_status.sh $(NUM_VALS)
	# @bash ./scripts/chain/pause_nodes.sh $(NUM_VALS)
	# @bash ./scripts/chain/resume_nodes.sh $(NUM_VALS)

	# @echo "Waiting for chain to resume..."
	# @sleep 7
	# @export NODE_HOME=${PWD}/localnet/${IMAGE}-1
	# @export CONTAINER_NAME=${IMAGE}node1
	# @echo ${CONTAINER_NAME}
	# @echo ${NODE_HOME}
	# $(MAKE) start-docker-chain
	# @sleep 5
	TEST_TYPE=multi-msg-load bash ./scripts/tests/multi_msg_load.sh -n 50
	TEST_TYPE=query-load bash ./scripts/tests/query_load.sh -n 50
	TEST_TYPE=send-load bash ./scripts/tests/send_load.sh -n 50
	TEST_TYPE=single-msg-load bash ./scripts/tests/single_msg_load.sh -n 50
	$(MAKE) stop-docker-chain

test-all-modules: start-docker-chain
	@echo "Running all individual module tests..."
	TEST_TYPE=module bash ./scripts/tests/all_modules.sh
	$(MAKE) stop-docker-chain

test-multi-msg:

test-multi-msg:
	@echo "Running multi msg load test..."
	# @IMAGE=${DAEMON}${CHAIN_VERSION}
	# export NODE_HOME=${PWD}/localnet/${IMAGE}-1
	# export CONTAINER_NAME=qa${IMAGE}node1
	TEST_TYPE=multi-msg-load bash ./scripts/tests/multi_msg_load.sh -n 50
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
