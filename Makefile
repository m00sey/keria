.PHONY: build-keria
build-keria:
	@docker buildx build --platform=linux/amd64 --no-cache -f images/keria.dockerfile --tag m00sey/keria:nord-fix  .

publish-keria:
	@docker push m00sey/keria:nord-fix