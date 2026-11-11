
require("dotenv").config();

const express = require("express");
const cors = require("cors");
const Razorpay = require("razorpay");
const crypto = require("crypto");

const products = require("./catalogue");
const { pool, initDatabase } = require("./postgres");

const app = express();
const PORT = process.env.PORT || 5000;

// ------------------------------------------
// CHECK PAYMENT CREDENTIALS
// ------------------------------------------

if (!process.env.RAZORPAY_KEY_ID ||
    !process.env.RAZORPAY_KEY_SECRET) {
    console.error("Razorpay credentials are missing in .env");
    process.exit(1);
}

const razorpay = new Razorpay({
    key_id: process.env.RAZORPAY_KEY_ID,
    key_secret: process.env.RAZORPAY_KEY_SECRET
});

// ------------------------------------------
// CORS CONFIGURATION
// ------------------------------------------

const allowedOrigins = [
    "https://kajal577.github.io",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
];

app.use(cors({
    origin: (origin, callback) => {
        if (!origin || allowedOrigins.includes(origin)) {
            return callback(null, true);
        }

        callback(new Error("Origin not allowed"));
    }
}));

app.use(express.json({ limit: "20kb" }));

// ------------------------------------------
// HEALTH CHECK
// ------------------------------------------

app.get("/api/health", (req, res) => {
    res.json({
        success: true,
        message: "VJaYa Robotics payment server is running."
    });
});

// ------------------------------------------
// CREATE RAZORPAY ORDER
// ------------------------------------------

app.post("/api/create-order", async (req, res) => {
    try {
        const { items, customer } = req.body;
        // Validate customer details.
if (
    !customer ||
    typeof customer.name !== "string" ||
    typeof customer.email !== "string" ||
    typeof customer.phone !== "string" ||
    typeof customer.address !== "string"
) {
    return res.status(400).json({
        success: false,
        message: "Please provide all customer details."
    });
}

const customerName = customer.name.trim();
const customerEmail = customer.email.trim();
const customerPhone = customer.phone.trim();
const shippingAddress = customer.address.trim();

if (
    !customerName ||
    customerName.length > 100 ||
    !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(customerEmail) ||
    customerEmail.length > 254 ||
    !/^[0-9+()\-\s]{7,20}$/.test(customerPhone) ||
    !shippingAddress ||
    shippingAddress.length > 1000
) {
    return res.status(400).json({
        success: false,
        message: "Please enter valid customer and delivery details."
    });
}

        if (!Array.isArray(items) || items.length === 0) {
            return res.status(400).json({
                success: false,
                message: "Your cart is empty."
            });
        }

        if (items.length > products.length) {
            return res.status(400).json({
                success: false,
                message: "Invalid cart."
            });
        }

        let totalPaise = 0;
        const orderItems = [];

        for (const item of items) {
            const productId = Number(item.id);
            const quantity = Number(item.quantity);

            if (
                !Number.isInteger(productId) ||
                !Number.isInteger(quantity) ||
                quantity < 1 ||
                quantity > 20
            ) {
                return res.status(400).json({
                    success: false,
                    message: "Invalid product or quantity."
                });
            }

            const product = products.find(
                p => p.id === productId
            );

            if (!product) {
                return res.status(400).json({
                    success: false,
                    message: "Product not found."
                });
            }

           const inventoryResult = await pool.query(
    `SELECT stock FROM inventory WHERE product_id = $1`,
    [productId]
);

const inventoryItem = inventoryResult.rows[0];

if (!inventoryItem || quantity > inventoryItem.stock) {
    return res.status(400).json({
        success: false,
        message: `${product.name} has insufficient stock.`
    });
}

            totalPaise += product.price * 100 * quantity;

            orderItems.push({
                id: product.id,
                name: product.name,
                quantity: quantity
            });
        }

        if (!Number.isSafeInteger(totalPaise) || totalPaise <= 0) {
            return res.status(400).json({
                success: false,
                message: "Invalid order amount."
            });
        }

        const order = await razorpay.orders.create({
            amount: totalPaise,
            currency: "INR",
            receipt: `vjaya_${Date.now()}`,
            notes: {
                store: "VJaYa Robotics",
                item_count: String(orderItems.length)
            }
        });


const client = await pool.connect();

try {
    await client.query("BEGIN");

    await client.query(`
        INSERT INTO orders (
            order_id,
            customer_name,
            customer_email,
            customer_phone,
            shipping_address,
            amount,
            currency,
            status
        )
        VALUES ($1, $2, $3, $4, $5, $6, $7, 'pending')
    `, [
        order.id,
        customerName,
        customerEmail,
        customerPhone,
        shippingAddress,
        order.amount,
        order.currency
    ]);

    for (const item of orderItems) {
        const product = products.find(p => p.id === item.id);

        await client.query(`
            INSERT INTO order_items (
                order_id,
                product_id,
                product_name,
                unit_price,
                quantity
            )
            VALUES ($1, $2, $3, $4, $5)
        `, [
            order.id,
            item.id,
            item.name,
            product.price,
            item.quantity
        ]);
    }

    await client.query("COMMIT");
} catch (error) {
    await client.query("ROLLBACK");
    throw error;
} finally {
    client.release();
}

        res.json({
            success: true,
            key: process.env.RAZORPAY_KEY_ID,
            order: order,
            items: orderItems
        });

    } catch (error) {
        console.error("Order creation failed:", error.message);

        res.status(500).json({
            success: false,
            message: "Unable to create payment order."
        });
    }
});

// ------------------------------------------
// VERIFY PAYMENT SIGNATURE AND STATUS
// ------------------------------------------

app.post("/api/verify-payment", async (req, res) => {
    console.log("VERIFY PAYMENT ROUTE REACHED:", req.body.razorpay_payment_id);
    try {
        const {
            razorpay_order_id,
            razorpay_payment_id,
            razorpay_signature
        } = req.body;

        if (
            typeof razorpay_order_id !== "string" ||
            typeof razorpay_payment_id !== "string" ||
            typeof razorpay_signature !== "string" ||
            !/^[a-f0-9]{64}$/i.test(razorpay_signature)
        ) {
            return res.status(400).json({
                success: false,
                message: "Invalid payment details."
            });
        }

        const body =
            razorpay_order_id + "|" + razorpay_payment_id;

        const expectedSignature = crypto
            .createHmac(
                "sha256",
                process.env.RAZORPAY_KEY_SECRET
            )
            .update(body)
            .digest();

        const receivedSignature = Buffer.from(
            razorpay_signature,
            "hex"
        );

        if (
            !crypto.timingSafeEqual(
                expectedSignature,
                receivedSignature
            )
        ) {
            return res.status(400).json({
                success: false,
                message: "Payment signature verification failed."
            });
        }

        // Confirm payment details directly with Razorpay.
        const payment = await razorpay.payments.fetch(
            razorpay_payment_id
        );

        const order = await razorpay.orders.fetch(
            razorpay_order_id
        );

        if (
            payment.order_id !== order.id ||
            payment.currency !== "INR" ||
            payment.amount !== order.amount
        ) {
            return res.status(400).json({
                success: false,
                message: "Payment details do not match."
            });
        }

        if (payment.status !== "captured") {
            return res.status(409).json({
                success: false,
                message: "Payment is verified but not yet captured.",
                paymentStatus: payment.status
            });
        }


// Confirm that this order exists in our database.
const savedOrderResult = await pool.query(
    "SELECT * FROM orders WHERE order_id = $1",
    [razorpay_order_id]
);

const savedOrder = savedOrderResult.rows[0];

if (!savedOrder) {
    return res.status(404).json({
        success: false,
        message: "Order not found in database."
    });
}

if (
    savedOrder.amount !== payment.amount ||
    savedOrder.currency !== payment.currency
) {
    return res.status(400).json({
        success: false,
        message: "Payment does not match the saved order."
    });
}

// Process payment and stock updates atomically.
// Process payment and stock updates atomically.
const client = await pool.connect();
let processingResult;

try {
    await client.query("BEGIN");

    // Lock the order to prevent duplicate stock deductions.
    const lockedOrderResult = await client.query(
        "SELECT * FROM orders WHERE order_id = $1 FOR UPDATE",
        [razorpay_order_id]
    );

    const lockedOrder = lockedOrderResult.rows[0];

    if (!lockedOrder) {
        throw new Error("Order not found.");
    }

    if (lockedOrder.status === "paid") {
        if (lockedOrder.payment_id === payment.id) {
            processingResult = "already_processed";
        } else {
            throw new Error("Order has already been paid.");
        }
    } else {
        if (lockedOrder.status !== "pending") {
            throw new Error("Order is not pending.");
        }

        const itemsResult = await client.query(
            `SELECT product_id, quantity
             FROM order_items
             WHERE order_id = $1`,
            [razorpay_order_id]
        );

        const items = itemsResult.rows;

        if (items.length === 0) {
            throw new Error("No products found in this order.");
        }

        for (const item of items) {
            const result = await client.query(
                `UPDATE inventory
                 SET stock = stock - $1
                 WHERE product_id = $2 AND stock >= $1`,
                [item.quantity, item.product_id]
            );

            if (result.rowCount !== 1) {
                throw new Error("Insufficient stock for a paid order.");
            }
        }

        await client.query(
            `UPDATE orders
             SET payment_id = $1,
                 status = 'paid',
                 paid_at = CURRENT_TIMESTAMP
             WHERE order_id = $2 AND status = 'pending'`,
            [payment.id, razorpay_order_id]
        );

        processingResult = "processed";
    }

    await client.query("COMMIT");

} catch (error) {
    await client.query("ROLLBACK");

    console.error("Payment processing failed:", error.message);

    return res.status(409).json({
        success: false,
        message: error.message
    });

} finally {
    client.release();
}



        res.json({
            success: true,
            message: "Payment verified successfully.",
            paymentId: payment.id,
            orderId: order.id
        });

    } catch (error) {
        console.error("Payment verification failed:", error.message);

        res.status(500).json({
            success: false,
            message: "Unable to verify payment."
        });
    }
});


// ------------------------------------------
// SECURE EXISTING PAYMENT RECOVERY
// ------------------------------------------

app.post("/api/recover-payment", async (req, res) => {
    const expectedSecret = process.env.RECOVERY_SECRET;
    const suppliedSecret = req.get("x-recovery-secret");

    if (!expectedSecret || !suppliedSecret) {
        return res.status(401).json({
            success: false,
            message: "Recovery authentication required."
        });
    }

    const expectedBuffer = Buffer.from(expectedSecret);
    const suppliedBuffer = Buffer.from(suppliedSecret);

    if (
        expectedBuffer.length !== suppliedBuffer.length ||
        !crypto.timingSafeEqual(expectedBuffer, suppliedBuffer)
    ) {
        return res.status(401).json({
            success: false,
            message: "Recovery authentication failed."
        });
    }

    const { orderId, paymentId } = req.body || {};

    if (
        typeof orderId !== "string" ||
        typeof paymentId !== "string"
    ) {
        return res.status(400).json({
            success: false,
            message: "Invalid order or payment ID."
        });
    }

    let client;
let recoveryStep = "Razorpay payment lookup";
    try {
        // Verify the existing payment directly with Razorpay.
        const payment = await razorpay.payments.fetch(paymentId);
        recoveryStep = "Razorpay order lookup";
        const razorpayOrder = await razorpay.orders.fetch(orderId);

        if (
            payment.id !== paymentId ||
            payment.order_id !== orderId ||
            razorpayOrder.id !== orderId ||
            payment.currency !== "INR" ||
            razorpayOrder.currency !== "INR" ||
            Number(payment.amount) !== Number(razorpayOrder.amount) ||
            payment.status !== "captured"
        ) {
            return res.status(409).json({
                success: false,
                message: "Razorpay payment details do not match or payment is not captured."
            });
        }

        client = await pool.connect();
        await client.query("BEGIN");

        // Lock the saved order to prevent duplicate processing.
        const result = await client.query(
            "SELECT * FROM orders WHERE order_id = $1 FOR UPDATE",
            [orderId]
        );

        const savedOrder = result.rows[0];

        if (!savedOrder) {
            throw new Error("The order does not exist in the database.");
        }

        if (
            Number(savedOrder.amount) !== Number(payment.amount) ||
            savedOrder.currency !== payment.currency
        ) {
            throw new Error("Payment does not match the saved order.");
        }

        if (savedOrder.status === "paid") {
            if (savedOrder.payment_id === paymentId) {
                await client.query("COMMIT");

                return res.json({
                    success: true,
                    message: "This payment was already processed.",
                    orderId,
                    paymentId
                });
            }

            throw new Error("This order has already been paid with another payment.");
        }

        if (
            savedOrder.status !== "pending" ||
            savedOrder.payment_id
        ) {
            throw new Error("This order is not eligible for recovery.");
        }

        // Prevent the same payment from being attached to another order.
        const duplicatePayment = await client.query(
            "SELECT order_id FROM orders WHERE payment_id = $1",
            [paymentId]
        );

        if (duplicatePayment.rows.length > 0) {
            throw new Error("This payment is already linked to an order.");
        }

        const itemsResult = await client.query(
            `SELECT product_id, quantity
             FROM order_items
             WHERE order_id = $1`,
            [orderId]
        );

        if (itemsResult.rows.length === 0) {
            throw new Error("No products were found in this order.");
        }

        // Deduct stock only once, inside the same transaction.
        for (const item of itemsResult.rows) {
            const stockResult = await client.query(
                `UPDATE inventory
                 SET stock = stock - $1
                 WHERE product_id = $2 AND stock >= $1`,
                [item.quantity, item.product_id]
            );

            if (stockResult.rowCount !== 1) {
                throw new Error("Insufficient stock for an item in this paid order.");
            }
        }

        await client.query(
            `UPDATE orders
             SET payment_id = $1,
                 status = 'paid',
                 paid_at = CURRENT_TIMESTAMP
             WHERE order_id = $2 AND status = 'pending'`,
            [paymentId, orderId]
        );

        await client.query("COMMIT");

        console.log("Existing payment recovered:", orderId);

        return res.json({
            success: true,
            message: "Existing payment recovered successfully.",
            orderId,
            paymentId
        });

    
    } catch (error) {
        if (client) {
            await client.query("ROLLBACK").catch(() => {});
        }

        const diagnostic = require("util").inspect(error, {
            depth: 6,
            colors: false,
            compact: true,
            breakLength: Infinity
        });

        const errorMessage =
            error?.error?.description ||
            error?.description ||
            error?.message ||
            (typeof error === "string" ? error : diagnostic);

        console.error("RECOVERY ERROR FULL:", diagnostic);

        return res.status(409).json({
            success: false,
            message: String(errorMessage).slice(0, 1500),
            code: error?.error?.code || error?.code || null,
            step: recoveryStep
        });

    } finally {
        if (client) {
            client.release();
        }
    }

});


// ------------------------------------------
// ERROR HANDLER
// ------------------------------------------

app.use((error, req, res, next) => {
    console.error(error.message);

    res.status(500).json({
        success: false,
        message: "Server error."
    });
});

// ------------------------------------------
// START SERVER
// ------------------------------------------

async function startServer() {
    try {
        await initDatabase();

        app.listen(PORT, "0.0.0.0", () => {
            console.log("--------------------------------");
            console.log("VJaYa Robotics Payment Server");
            console.log("PostgreSQL Connected");
            console.log(`Running on port ${PORT}`);
            console.log("--------------------------------");
        });

    } catch (error) {
        console.error("Failed to start payment server:", error.message);
        process.exit(1);
    }
}

startServer();
