gen-cert:
		openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
			-keyout $(HOME)/.certs/localhost.key \
			-out $(HOME)/.certs/localhost.crt \
			-config $(CURDIR)/localhost.conf

build-proto:
		docker run -it \
		    -u ${UID} \
		    -v $(CURDIR)/proto/api.proto:/proto/api.proto \
		    -e PROTO_DIR=/proto \
		    -e PROTO_FILES=api.proto \
		    -v $(CURDIR)/tmp/python_pb:/python_pb \
		    -e PYTHON_OUT=/python_pb \
		    -e GRPC_PYTHON_OUT=/python_pb \
		    gcr.io/fruition-data-warehouse/proto-builder-python:dev
