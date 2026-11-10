
const { Pool } = require("pg");
const products = require("./catalogue");

if (!process.env.DATABASE_URL) {
    throw new Error("DATABASE_URL is missing from .env");
}

const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: {
        rejectUnauthorized: false
    }
});

pool.on("error", (error) => {
    console.error("PostgreSQL connection error:", error.message);
});

async function initDatabase() {
    await pool.query(`
        CREATE TABLE IF NOT EXISTS inventory (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            price INTEGER NOT NULL,
            stock INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            payment_id TEXT UNIQUE,
            customer_name TEXT,
            customer_email TEXT,
            customer_phone TEXT,
            shipping_address TEXT,
            amount INTEGER NOT NULL,
            currency TEXT NOT NULL DEFAULT 'INR',
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            paid_at TIMESTAMPTZ
        );

        CREATE TABLE IF NOT EXISTS order_items (
            id SERIAL PRIMARY KEY,
            order_id TEXT NOT NULL REFERENCES orders(order_id),
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            unit_price INTEGER NOT NULL,
            quantity INTEGER NOT NULL
        );
    `);

    for (const product of products) {
        await pool.query(`
            INSERT INTO inventory
                (product_id, product_name, price, stock)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (product_id) DO NOTHING
        `, [
            product.id,
            product.name,
            product.price,
            product.stock
        ]);
    }

    console.log("VJaYa Robotics PostgreSQL initialized.");
}

module.exports = {
    pool,
    initDatabase
};
