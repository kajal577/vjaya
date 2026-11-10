
require("dotenv").config();

const express = require("express");
const cors = require("cors");
const Razorpay = require("razorpay");
const crypto = require("crypto");

const products = require("./catalogue");
const db = require("./database");

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

            const inventoryItem = db.prepare(`
    SELECT stock FROM inventory
    WHERE product_id = ?
`).get(productId);

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


const saveOrder = db.transaction(() => {
    db.prepare(`
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
        VALUES (?, ?, ?, ?, ?, ?, ?, 'pending'')
    `).run( order.id,
    customerName,
    customerEmail,
    customerPhone,
    shippingAddress,
    order.amount,
    order.currency);

    const insertItem = db.prepare(`
        INSERT INTO order_items (
            order_id, product_id, product_name,
            unit_price, quantity
        )
        VALUES (?, ?, ?, ?, ?)
    `);

    for (const item of orderItems) {
        const product = products.find(p => p.id === item.id);

        insertItem.run(
            order.id,
            item.id,
            item.name,
            product.price,
            item.quantity
        );
    }
});

saveOrder();


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
const savedOrder = db.prepare(`
    SELECT * FROM orders WHERE order_id = ?
`).get(razorpay_order_id);

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
const processPayment = db.transaction(() => {

    // Prevent duplicate stock deductions.
    if (savedOrder.status === "paid") {
        if (savedOrder.payment_id === payment.id) {
            return "already_processed";
        }

        throw new Error("Order has already been paid.");
    }

    if (savedOrder.status !== "pending") {
        throw new Error("Order is not pending.");
    }

    const items = db.prepare(`
        SELECT product_id, quantity
        FROM order_items
        WHERE order_id = ?
    `).all(razorpay_order_id);

    if (items.length === 0) {
        throw new Error("No products found in this order.");
    }

    const updateStock = db.prepare(`
        UPDATE inventory
        SET stock = stock - ?
        WHERE product_id = ? AND stock >= ?
    `);

    for (const item of items) {
        const result = updateStock.run(
            item.quantity,
            item.product_id,
            item.quantity
        );

        if (result.changes !== 1) {
            throw new Error("Insufficient stock for a paid order.");
        }
    }

    db.prepare(`
        UPDATE orders
        SET payment_id = ?,
            status = 'paid',
            paid_at = CURRENT_TIMESTAMP
        WHERE order_id = ? AND status = 'pending'
    `).run(payment.id, razorpay_order_id);

    return "processed";
});

let processingResult;

try {
    processingResult = processPayment();
} catch (error) {
    console.error("Order processing failed:", error.message);

    return res.status(409).json({
        success: false,
        message: error.message
    });
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

app.listen(PORT, () => {
    console.log("--------------------------------");
    console.log("VJaYa Robotics Payment Server");
    console.log(`Running on port ${PORT}`);
    console.log("--------------------------------");
});
