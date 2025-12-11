```bash
docker pull ankane/pgvector

docker run -d --name postgres-vector `
>>   -e POSTGRES_DB=vectordb `
>>   -e POSTGRES_USER=postgres `
>>   -e POSTGRES_PASSWORD=19941126 `
>>   -p 5432:5432 `
>>   ankane/pgvector

```
