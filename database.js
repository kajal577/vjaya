
const Database = require("better-sqlite3");
const products = require("./catalogue");
const path = require("path");

// Create the VJaYa Robotics database.
const db = new Database(
    path.join(__dirname, "vjaya_orders.db")
);

// Enable database safety features.
db.pragma("journal_mode = WAL");
db.pragma("foreign_keys = ON");

// Store product inventory.
db.exec(`
    CREATE TABLE IF NOT EXISTS inventory (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        price INTEGER NOT NULL,
        stock INTEGER NOT NULL
    );
`);

// Store customer orders and payment information.
db.exec(`
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
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        paid_at TEXT
    );
`);

// Store individual products belonging to each order.
db.exec(`
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id TEXT NOT NULL,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        unit_price INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (order_id)
            REFERENCES orders(order_id)
    );
`);

// Add catalogue products to inventory on first startup.
// Existing stock quantities are not overwritten.
const insertProduct = db.prepare(`
    INSERT OR IGNORE INTO inventory
    (product_id, product_name, price, stock)
    VALUES (?, ?, ?, ?)
`);

const seedInventory = db.transaction(() => {
    for (const product of products) {
        insertProduct.run(
            product.id,
            product.name,
            product.price,
            product.stock
        );
    }
});

seedInventory();

console.log("VJaYa Robotics database initialized.");

module.exports = db;
