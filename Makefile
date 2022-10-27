.PHONY: run

run:
	python3 folder_sync_script.py node1 node2 script_log.log 3

.DEFAULT_GOAL := run
