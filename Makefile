gen-cert:
		openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
			-keyout $(HOME)/.certs/localhost.key \
			-out $(HOME)/.certs/localhost.crt \
			-config $(CURDIR)/localhost.conf

update-conf:
		docker-compose exec web nginx -s reload

