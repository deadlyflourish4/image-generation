Init cluster
- minikube start
- minikube status

Enable impotance add-ons
- minikube addons enable metrics-server
- minikube addons enable ingress

Namespace
- kubectl create namespace

Deploy Redis
- kubectl get secret -n imagen redis -o jsonpath="{.data.redis-password}" | %{[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($_))}
- kubectl exec -it -n imagen redis-master-0 -- redis-cli
```qgsql
AUTH <password>
SET test "hello"
GET test
```

Deploy RabbitMQ
```bash
kubectl get secret rmq-default-user -n imagen -o jsonpath="{.data.username}" |
%{[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($_))}

kubectl get secret rmq-default-user -n imagen -o jsonpath="{.data.password}" |
%{[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($_))}
```

Login 

