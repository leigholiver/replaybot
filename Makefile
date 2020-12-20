dev:
	make docker_daemon && make lamb

docker:
	make docker_daemon && sudo docker-compose logs -f

docker_daemon:
	sudo docker-compose build && . web/secrets.env && sudo -E docker-compose --compatibility up -d

lamb:
	cd web && ./lambctl dev
