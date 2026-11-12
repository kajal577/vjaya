
const express = require("express");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");

module.exports = function createAdminRouter(pool, products) {
    const router = express.Router();

    // --------------------------------------
    // ADMIN LOGIN
    // --------------------------------------

    router.post("/login", async (req, res) => {
        try {
            const { email, password } = req.body || {};

            if (
                typeof email !== "string" ||
                typeof password !== "string" ||
                !email.trim() ||
                !password
            ) {
                return res.status(400).json({
                    success: false,
                    message: "Enter your admin email and password."
                });
            }

            const adminEmail = process.env.ADMIN_EMAIL;
            const passwordHash = process.env.ADMIN_PASSWORD_HASH;
            const jwtSecret = process.env.ADMIN_JWT_SECRET;

            if (!adminEmail || !passwordHash || !jwtSecret) {
                return res.status(503).json({
                    success: false,
                    message: "Admin login is not configured."
                });
            }

            const emailMatches =
                email.trim().toLowerCase() === adminEmail.trim().toLowerCase();

            const passwordMatches = await bcrypt.compare(
                password,
                passwordHash
            );

            if (!emailMatches || !passwordMatches) {
                return res.status(401).json({
                    success: false,
                    message: "Invalid admin email or password."
                });
            }

            const token = jwt.sign(
                {
                    role: "admin",
                    email: adminEmail
                },
                jwtSecret,
                {
                    expiresIn: "8h",
                    issuer: "vjaya-robotics"
                }
            );

            return res.json({
                success: true,
                message: "Admin login successful.",
                token,
                admin: {
                    email: adminEmail
                }
            });

        } catch (error) {
            console.error("Admin login error:", error.message);

            return res.status(500).json({
                success: false,
                message: "Unable to process admin login."
            });
        }
    });

    // --------------------------------------
    // PROTECT ADMIN ROUTES
    // --------------------------------------

    function requireAdmin(req, res, next) {
        const authorization = req.headers.authorization || "";

        if (!authorization.startsWith("Bearer ")) {
            return res.status(401).json({
                success: false,
                message: "Admin authentication required."
            });
        }

        const token = authorization.slice(7);
        const jwtSecret = process.env.ADMIN_JWT_SECRET;

        if (!jwtSecret) {
            return res.status(503).json({
                success: false,
                message: "Admin authentication is not configured."
            });
        }

        try {
            const decoded = jwt.verify(token, jwtSecret, {
                issuer: "vjaya-robotics"
            });

            if (decoded.role !== "admin") {
                return res.status(403).json({
                    success: false,
                    message: "Admin access denied."
                });
            }

            req.admin = decoded;
            next();

        } catch (error) {
            return res.status(401).json({
                success: false,
                message: "Your admin session is invalid or expired."
            });
        }
    }

    // --------------------------------------
    // DASHBOARD OVERVIEW
    // --------------------------------------

    router.get("/dashboard", requireAdmin, async (req, res) => {
        try {
            const salesResult = await pool.query(`
                SELECT
                    COUNT(*)::INTEGER AS total_orders,
                    COUNT(*) FILTER (
                        WHERE status = 'paid'
                    )::INTEGER AS paid_orders,
                    COUNT(*) FILTER (
                        WHERE status = 'pending'
                    )::INTEGER AS pending_orders,
                    COALESCE(
                        SUM(amount) FILTER (
                            WHERE status = 'paid'
                        ), 0
                    ) / 100.0 AS total_sales
                FROM orders
            `);

            const inventoryResult = await pool.query(`
                SELECT
                    COUNT(*)::INTEGER AS total_products,
                    COUNT(*) FILTER (
                        WHERE stock <= 5
                    )::INTEGER AS low_stock_products
                FROM inventory
            `);

            return res.json({
                success: true,
                sales: salesResult.rows[0],
                inventory: inventoryResult.rows[0]
            });

        } catch (error) {
            console.error("Admin dashboard error:", error.message);

            return res.status(500).json({
                success: false,
                message: "Unable to load dashboard."
            });
        }
    });

    // --------------------------------------
    // VIEW PRODUCTS AND INVENTORY
    // --------------------------------------

    router.get("/products", requireAdmin, async (req, res) => {
        try {
            const result = await pool.query(`
                SELECT product_id, product_name, price, stock
                FROM inventory
                ORDER BY product_id ASC
            `);

            return res.json({
                success: true,
                products: result.rows
            });

        } catch (error) {
            console.error("Admin products error:", error.message);

            return res.status(500).json({
                success: false,
                message: "Unable to load products."
            });
        }
    });

    // --------------------------------------
    // UPDATE PRODUCT STOCK
    // --------------------------------------

    router.patch(
        "/products/:id/stock",
        requireAdmin,
        async (req, res) => {
            try {
                const productId = Number(req.params.id);
                const stock = req.body?.stock;

                if (
                    !Number.isInteger(productId) ||
                    !products.some(product => product.id === productId) ||
                    !Number.isInteger(stock) ||
                    stock < 0 ||
                    stock > 100000
                ) {
                    return res.status(400).json({
                        success: false,
                        message: "Invalid product ID or stock quantity."
                    });
                }

                const result = await pool.query(`
                    UPDATE inventory
                    SET stock = $1
                    WHERE product_id = $2
                    RETURNING product_id, product_name, price, stock
                `, [stock, productId]);

                if (result.rowCount === 0) {
                    return res.status(404).json({
                        success: false,
                        message: "Product inventory not found."
                    });
                }

                return res.json({
                    success: true,
                    message: "Product stock updated successfully.",
                    product: result.rows[0]
                });

            } catch (error) {
                console.error("Stock update error:", error.message);

                return res.status(500).json({
                    success: false,
                    message: "Unable to update product stock."
                });
            }
        }
    );

    // --------------------------------------
    // VIEW CUSTOMER ORDERS
    // --------------------------------------

    router.get("/orders", requireAdmin, async (req, res) => {
        try {
            const result = await pool.query(`
                SELECT
                    o.order_id,
                    o.payment_id,
                    o.customer_name,
                    o.customer_email,
                    o.customer_phone,
                    o.shipping_address,
                    o.amount,
                    o.currency,
                    o.status,
                    o.created_at,
                    o.paid_at,
                    COALESCE(
                        json_agg(
                            json_build_object(
                                'productId', oi.product_id,
                                'productName', oi.product_name,
                                'unitPrice', oi.unit_price,
                                'quantity', oi.quantity
                            )
                        ) FILTER (WHERE oi.id IS NOT NULL),
                        '[]'
                    ) AS items
                FROM orders o
                LEFT JOIN order_items oi
                    ON oi.order_id = o.order_id
                GROUP BY o.order_id
                ORDER BY o.created_at DESC
                LIMIT 100
            `);

            return res.json({
                success: true,
                orders: result.rows
            });

        } catch (error) {
            console.error("Admin orders error:", error.message);

            return res.status(500).json({
                success: false,
                message: "Unable to load customer orders."
            });
        }
    });

    return router;
};
