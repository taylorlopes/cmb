
# Certificados

Não use os certificados deste repositório, ao invés crie seu próprio.


## Criar um arquivo auto-assinado PEM:

```bash
openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem
```
