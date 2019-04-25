docker build -t mikemcgarry/gym-hero-view ./view
docker build -t mikemcgarry/gym-hero-controller ./controller
docker build -t mikemcgarry/gym-hero-server ./datasource

docker push mikemcgarry/gym-hero-view
docker push mikemcgarry/gym-hero-controller
docker push mikemcgarry/gym-hero-datasource

kubectl apply -f k8s
