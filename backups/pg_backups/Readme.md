To run the postgres dump manually, you can run this command from the root directory of this project
```
    docker run --rm \
    --name pg_dump_once \
    --network container:navatech_db \
    -e PGPASSWORD=secret \
    -v $(pwd)/backups/pg_backups:/backups \
    postgres:15 \
    pg_dump -h localhost -U admin -F c -d postgres_db -f /backups/backup_$(date +%Y%m%d_%H%M%S).dump
```