.PHONY: build-keria
build-keria:
	@docker buildx build --platform=linux/amd64 --no-cache -f images/keria.dockerfile --tag m00sey/0.2.0-dev4-sig-fix .

publish-keria:
	@docker push m00sey/keria --all-tags