# 🚦 Rate Limiter Service (FastAPI + Redis + Token Bucket)

## 📌 Overview

This project implements a **production-style rate limiter** using the **Token Bucket algorithm** with **FastAPI** and **Redis**.

It demonstrates key backend engineering concepts such as:

* Middleware-based request control
* Distributed rate limiting using Redis
* Atomic operations with Lua scripts
* Dockerized development environment
* Config-driven design

---

## 🎯 Features

* ✅ Token Bucket rate limiting algorithm
* ✅ Redis-backed state (scalable & shared)
* ✅ Lua script for atomic operations (no race conditions)
* ✅ FastAPI middleware integration
* ✅ Docker + Docker Compose setup
* ✅ Environment-based configuration
* ✅ Shell script for load testing

---

## 🧠 How It Works

Each request goes through the following flow:

```
Request → Middleware → Redis (Token Bucket via Lua) → Allow / Reject
```

### Token Bucket Logic

* Each user has:

  * `tokens`
  * `last request time`
* Tokens are refilled over time
* If no tokens remain → request is rejected

### Why Lua Script?

* Ensures **atomic execution** in Redis
* Prevents **race conditions** under concurrent requests

---

## 🏗️ Project Structure

```
.
├── main.py                 # FastAPI app + middleware
├── token_bucket.lua       # Token bucket implementation (Lua)
├── Dockerfile              # App container definition
├── docker-compose.yml      # App + Redis setup
├── test_rate_limiter.sh    # Load testing script
├── .env.example            # Environment variables template
└── requirements.txt        # Python dependencies
```

---

## ⚙️ Components

### 🔹 `main.py`

* Entry point of the application
* Contains:

  * FastAPI app
  * Middleware (`check_request`)
  * Redis initialization (`lifespan`)
  * Lua script loader (`get_script_hash`)

---

### 🔹 Redis

* Stores rate limiting state:

  * last available tokens
  * last refill timestamp
* Executes Lua script for atomic updates

---

### 🔹 Lua Script

* Implements Token Bucket logic
* Runs inside Redis
* Handles:

  * token refill
  * request allowance/rejection

---

### 🔹 Docker Setup

#### `Dockerfile`

* Builds the FastAPI application image

#### `docker-compose.yml`

* Spins up:

  * FastAPI app
  * Redis instance

---

### 🔹 Testing Script

#### `test_rate_limiter.sh`

* Sends multiple requests quickly
* Helps verify:

  * rate limiting behavior
  * rejection responses

---

### 🔹 Environment Config

#### `.env.example`

Example variables:

```
REDIS_HOST=redis
REDIS_PORT=6379
RATE_LIMIT=5
REFILL_RATE=1
```

---

## 🚀 Getting Started

### 1. Clone the repository

```
git clone git@github.com:rinkon/rate-limiter-redis.git
cd rate-limiter-redis
```

---

### 2. Setup environment

```
cp .env.example .env
```

---

### 3. Run with Docker

```
docker-compose up --build
```
or
```
docker compose up --build
```

---

### 4. Test the rate limiter

```
chmod +x test_rate_limiter.sh
./test_rate_limiter.sh
```

---

## 🧪 Example Behavior

* First few requests → ✅ Allowed **OK 200**
* Exceed limit → ❌ Rejected **Too Many Requests 429**
* After some time → ✅ Allowed again (token refill)

---

## 📊 Key Concepts Demonstrated

* Rate limiting strategies
* Token Bucket algorithm
* Distributed systems design
* Redis atomic operations
* Middleware architecture
* Docker-based development

---

## ⚠️ Limitations (Current)

* No authentication (static users / request-based identity)
* No per-route configuration (can be extended)
* No persistence beyond Redis


---

## 📚 Dependencies

* fastapi
* uvicorn
* redis
* python-dotenv

---

## 💡 Why This Project Matters

This project goes beyond a simple API and demonstrates:

> “How to design and implement a scalable, distributed rate limiter with correctness under concurrency.”

It’s highly relevant for backend and system design interviews.

---

## 🧑‍💻 Author

Built as part of backend system design and interview preparation.
