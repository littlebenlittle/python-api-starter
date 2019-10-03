
## Quickstart

	mkdir $HOME/.certs
	make gen-cert
	docker-compose up

navigate to [https://localhost:4443/auth](https://localhost:8080/auth)

## gRPC

    export UID=$UID  # hack to get Make to recognize the envvar
    make build-proto
