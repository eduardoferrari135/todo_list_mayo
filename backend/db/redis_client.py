import redis
import os
from dotenv import load_dotenv

load_dotenv()

# Coleta variávies de ambiente
REDIS_HOST=os.getenv("REDIS_HOST", "localhost")
REDIS_PORT=os.getenv("REDIS_PORT", 6379)

# Estabelece conexão com o banco de dados
r = redis.Redis(
  host=REDIS_HOST,
  port=int(REDIS_PORT),
  ssl_cert_reqs=None
)
