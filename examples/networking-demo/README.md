# Networking demo

Two Compose services on the default project network.

- `web` serves `./site` on container port 8000 and publishes it to the host.
- `client` fetches `http://web:8000/index.html` using the **service name** as DNS.

Lesson: [21](../../lessons/21-docker-networking.md)

```bash
cd examples/networking-demo
docker compose up --abort-on-container-exit
```

The client prints `200` and the HTML. Your browser can open `http://localhost:8000` because of the port publish. Inside `client`, `localhost:8000` would **not** reach `web`. Use `http://web:8000`.

```bash
docker compose down
```
