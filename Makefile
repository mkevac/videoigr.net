.PHONY: deploy
deploy:
	docker build . -t mkevac/videoigrnet
	docker push mkevac/videoigrnet
