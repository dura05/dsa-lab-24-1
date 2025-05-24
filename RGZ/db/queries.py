async def is_registered(pool, chat_id):
    async with pool.acquire() as conn:
        return await conn.fetchval("SELECT EXISTS(SELECT 1 FROM users WHERE chat_id = $1)", chat_id)

async def register_user(pool, chat_id, name):
    async with pool.acquire() as conn:
        await conn.execute("INSERT INTO users (chat_id, name) VALUES ($1, $2)", chat_id, name)

async def insert_operation(pool, chat_id, sum_, date, type_op):
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO operations (date, sum, chat_id, type_operation) VALUES ($1, $2, $3, $4)",
            date, sum_, chat_id, type_op
        )

async def get_user_operations(pool, chat_id):
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            "SELECT id, date, sum, type_operation FROM operations WHERE chat_id = $1 ORDER BY date DESC",
            chat_id
        )
        return [dict(row) for row in rows]

async def update_operation(pool, chat_id, op_id, new_sum):
    async with pool.acquire() as conn:
        await conn.execute(
            "UPDATE operations SET sum = $1 WHERE id = $2 AND chat_id = $3",
            new_sum, op_id, chat_id
        )

async def operation_exists(pool, chat_id, op_id):
    async with pool.acquire() as conn:
        return await conn.fetchval(
            "SELECT EXISTS(SELECT 1 FROM operations WHERE id = $1 AND chat_id = $2)",
            op_id, chat_id
        )
