default:
	@echo "Please specify a target to build"

generate_ssl:
	mkdir ssl && cd ssl && \
	openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

get_simulated:
	@echo "Mine is https://pixabay.com/videos/owl-animal-bird-nature-feather-18244/"