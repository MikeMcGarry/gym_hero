docker build -t mikemcgarry/gym-hero-view:latest -t mikemcgarry/gym-hero-view:$SHA ./view
docker build -t mikemcgarry/gym-hero-controller:latest -t mikemcgarry/gym-hero-controller:$SHA ./controller
docker build -t mikemcgarry/gym-hero-datasource:latest -t mikemcgarry/gym-hero-datasource:$SHA ./datasource

docker push mikemcgarry/gym-hero-view:latest
docker push mikemcgarry/gym-hero-view:$SHA
docker push mikemcgarry/gym-hero-controller:latest
docker push mikemcgarry/gym-hero-controller:$SHA
docker push mikemcgarry/gym-hero-datasource:latest
docker push mikemcgarry/gym-hero-datasource:$SHA

kubectl apply -n gym-hero -f k8s

kubectl set image -n gym-hero deployment/controller-deployment controller=mikemcgarry/gym-hero-controller:$SHA
kubectl set image -n gym-hero deployment/controller-deployment datasource=mikemcgarry/gym-hero-datasource:$SHA
kubectl set image -n gym-hero deployment/view-deployment view=mikemcgarry/gym-hero-view:$SHA
