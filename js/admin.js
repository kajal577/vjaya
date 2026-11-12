
// ==========================================
// VJAYA ROBOTICS - ADMIN DASHBOARD
// ==========================================

const API_BASE = "https://vjaya-robotics-api.onrender.com/api";
const TOKEN_KEY = "vjaya_admin_token";
const EMAIL_KEY = "vjaya_admin_email";

let adminToken = sessionStorage.getItem(TOKEN_KEY);
let adminEmail = sessionStorage.getItem(EMAIL_KEY);

let allProducts = [];
let allOrders = [];

// ==========================================
// DOM ELEMENTS
// ==========================================

const loginScreen = document.getElementById("login-screen");
const adminApp = document.getElementById("admin-app");
const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-button");
const loginError = document.getElementById("login-error");

const adminEmailDisplay = document.getElementById("admin-email-display");
const pageTitle = document.getElementById("page-title");
const adminMessage = document.getElementById("admin-message");

const productsTableBody = document.getElementById("products-table-body");
const ordersTableBody = document.getElementById("orders-table-body");

const orderDialog = document.getElementById("order-dialog");
const orderDetailsContent = document.getElementById("order-details-content");

// ==========================================
// SAFE HTML OUTPUT
// ==========================================

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, character => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[character]);
}

// ==========================================
// API REQUEST HELPER
// ==========================================

async function apiRequest(path, options = {}) {
    const headers = {
        ...(options.headers || {})
    };

    if (adminToken) {
        headers.Authorization = `Bearer ${adminToken}`;
    }

    if (options.body !== undefined) {
        headers["Content-Type"] = "application/json";
    }

    const response = await fetch(`${API_BASE}${path}`, {
        ...options,
        headers
    });

    let data;

    try {
        data = await response.json();
    } catch {
        data = {};
    }

    if (response.status === 401) {
        logout("Your admin session has expired. Please sign in again.");
        throw new Error(data.message || "Admin session expired.");
    }

    if (!response.ok || data.success === false) {
        throw new Error(data.message || "Unable to complete request.");
    }

    return data;
}

// ==========================================
// MESSAGE DISPLAY
// ==========================================

let messageTimer;

function showMessage(message, type = "success") {
    adminMessage.textContent = message;
    adminMessage.className = `admin-message visible ${type}`;

    clearTimeout(messageTimer);

    messageTimer = setTimeout(() => {
        adminMessage.className = "admin-message";
    }, 3500);
}

// ==========================================
// LOGIN
// ==========================================

loginForm.addEventListener("submit", async event => {
    event.preventDefault();

    loginError.textContent = "";
    loginButton.disabled = true;
    loginButton.textContent = "Signing in...";

    const email = document.getElementById("admin-email").value.trim();
    const password = document.getElementById("admin-password").value;

    try {
        const result = await fetch(`${API_BASE}/admin/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const data = await result.json();

        if (!result.ok || !data.success || !data.token) {
            throw new Error(data.message || "Login failed.");
        }

        adminToken = data.token;
        adminEmail = data.admin.email;

        // Keep the token only for this browser tab's session.
        sessionStorage.setItem(TOKEN_KEY, adminToken);
        sessionStorage.setItem(EMAIL_KEY, adminEmail);

        document.getElementById("admin-password").value = "";

        await openDashboard();

    } catch (error) {
        loginError.textContent = error.message || "Unable to sign in.";
    } finally {
        loginButton.disabled = false;
        loginButton.textContent = "Sign In";
    }
});

// ==========================================
// OPEN DASHBOARD
// ==========================================

async function openDashboard() {
    try {
        await loadDashboard();

        loginScreen.classList.add("hidden");
        adminApp.classList.remove("hidden");

        adminEmailDisplay.textContent = adminEmail || "Administrator";

        showSection("overview");

    } catch (error) {
        if (adminToken) {
            sessionStorage.removeItem(TOKEN_KEY);
            sessionStorage.removeItem(EMAIL_KEY);
        }

        adminToken = null;
        adminEmail = null;

        loginScreen.classList.remove("hidden");
        adminApp.classList.add("hidden");

        loginError.textContent = error.message;
    }
}

// ==========================================
// LOGOUT
// ==========================================

function logout(message = "You have signed out.") {
    adminToken = null;
    adminEmail = null;

    sessionStorage.removeItem(TOKEN_KEY);
    sessionStorage.removeItem(EMAIL_KEY);

    if (orderDialog.open) {
        orderDialog.close();
    }

    adminApp.classList.add("hidden");
    loginScreen.classList.remove("hidden");

    loginForm.reset();
    loginError.textContent = message;
}

document.getElementById("logout-button").addEventListener("click", () => {
    logout();
});

// ==========================================
// NAVIGATION
// ==========================================

const sectionTitles = {
    overview: "Dashboard Overview",
    products: "Product Management",
    orders: "Order Management"
};

function showSection(section) {
    if (!sectionTitles[section]) return;

    document.querySelectorAll(".content-section").forEach(element => {
        element.classList.add("hidden");
    });

    document.getElementById(`${section}-section`).classList.remove("hidden");

    document.querySelectorAll(".nav-link").forEach(button => {
        button.classList.toggle(
            "active",
            button.dataset.section === section
        );
    });

    pageTitle.textContent = sectionTitles[section];

    if (section === "products") {
        loadProducts();
    }

    if (section === "orders") {
        loadOrders();
    }
}

document.querySelectorAll("[data-section]").forEach(button => {
    button.addEventListener("click", () => {
        showSection(button.dataset.section);
    });
});

// ==========================================
// DASHBOARD STATISTICS
// ==========================================

async function loadDashboard() {
    const result = await apiRequest("/admin/dashboard");

    const sales = result.sales;
    const inventory = result.inventory;

    document.getElementById("stat-total-orders").textContent =
        Number(sales.total_orders || 0);

    document.getElementById("stat-paid-orders").textContent =
        Number(sales.paid_orders || 0);

    document.getElementById("stat-pending-orders").textContent =
        Number(sales.pending_orders || 0);

    document.getElementById("stat-total-sales").textContent =
        formatRupees(sales.total_sales);

    document.getElementById("stat-total-products").textContent =
        Number(inventory.total_products || 0);

    document.getElementById("stat-low-stock").textContent =
        Number(inventory.low_stock_products || 0);
}

function formatRupees(value) {
    const amount = Number(value || 0);

    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 2
    }).format(Number.isFinite(amount) ? amount : 0);
}

document.getElementById("refresh-dashboard").addEventListener("click", async () => {
    try {
        await loadDashboard();
        showMessage("Dashboard refreshed.");
    } catch (error) {
        showMessage(error.message, "error");
    }
});

// ==========================================
// PRODUCT MANAGEMENT
// ==========================================

async function loadProducts() {
    productsTableBody.innerHTML = `
        <tr><td colspan="5">Loading products...</td></tr>
    `;

    try {
        const result = await apiRequest("/admin/products");

        allProducts = result.products || [];

        renderProducts(allProducts);

    } catch (error) {
        productsTableBody.innerHTML = `
            <tr><td colspan="5">${escapeHTML(error.message)}</td></tr>
        `;
        showMessage(error.message, "error");
    }
}

function renderProducts(products) {
    document.getElementById("product-count").textContent =
        `${products.length} products`;

    if (!products.length) {
        productsTableBody.innerHTML = `
            <tr><td colspan="5">No products found.</td></tr>
        `;
        return;
    }

    productsTableBody.innerHTML = products.map(product => {
        const stock = Number(product.stock);
        const stockClass = stock <= 5 ? "stock-low" : "stock-good";

        return `
            <tr>
                <td>${Number(product.product_id)}</td>

                <td>${escapeHTML(product.product_name)}</td>

                <td>${formatRupees(product.price)}</td>

                <td class="${stockClass}">
                    ${stock}
                </td>

                <td>
                    <input
                        class="stock-input"
                        type="number"
                        min="0"
                        max="100000"
                        step="1"
                        value="${stock}"
                        id="stock-${Number(product.product_id)}"
                        aria-label="New stock quantity"
                    >

                    <button
                        type="button"
                        data-update-stock="${Number(product.product_id)}"
                    >
                        Save
                    </button>
                </td>
            </tr>
        `;
    }).join("");
}

document.getElementById("product-search").addEventListener("input", event => {
    const search = event.target.value.toLowerCase().trim();

    const filtered = allProducts.filter(product =>
        String(product.product_name).toLowerCase().includes(search) ||
        String(product.product_id).includes(search)
    );

    renderProducts(filtered);
});

productsTableBody.addEventListener("click", async event => {
    const button = event.target.closest("[data-update-stock]");

    if (!button) return;

    const productId = Number(button.dataset.updateStock);
    const stockInput = document.getElementById(`stock-${productId}`);

    if (!stockInput) return;

    const stock = Number(stockInput.value);

    if (
        !Number.isInteger(stock) ||
        stock < 0 ||
        stock > 100000
    ) {
        showMessage("Enter a whole stock quantity between 0 and 100000.", "error");
        return;
    }

    button.disabled = true;
    button.textContent = "Saving...";

    try {
        const result = await apiRequest(
            `/admin/products/${productId}/stock`,
            {
                method: "PATCH",
                body: JSON.stringify({ stock })
            }
        );

        showMessage(result.message || "Stock updated successfully.");

        await loadProducts();
        await loadDashboard();

    } catch (error) {
        showMessage(error.message, "error");
        button.disabled = false;
        button.textContent = "Save";
    }
});

document.getElementById("refresh-products").addEventListener("click", loadProducts);

// ==========================================
// ORDER MANAGEMENT
// ==========================================

async function loadOrders() {
    ordersTableBody.innerHTML = `
        <tr><td colspan="7">Loading orders...</td></tr>
    `;

    try {
        const result = await apiRequest("/admin/orders");

        allOrders = result.orders || [];

        renderOrders(allOrders);

    } catch (error) {
        ordersTableBody.innerHTML = `
            <tr><td colspan="7">${escapeHTML(error.message)}</td></tr>
        `;
        showMessage(error.message, "error");
    }
}

function formatDate(value) {
    if (!value) return "—";

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) return "—";

    return date.toLocaleString("en-IN", {
        dateStyle: "medium",
        timeStyle: "short"
    });
}

function renderOrders(orders) {
    document.getElementById("order-count").textContent =
        `${orders.length} recent orders`;

    if (!orders.length) {
        ordersTableBody.innerHTML = `
            <tr><td colspan="7">No orders found.</td></tr>
        `;
        return;
    }

    ordersTableBody.innerHTML = orders.map(order => {
        const status = String(order.status || "pending").toLowerCase();

        const statusClass = status === "paid"
            ? "payment-paid"
            : "payment-pending";

        return `
            <tr>
                <td>${escapeHTML(order.order_id)}</td>

                <td>${escapeHTML(order.customer_name)}</td>

                <td>${escapeHTML(order.customer_email)}</td>

                <td>${formatRupees(Number(order.amount || 0) / 100)}</td>

                <td class="${statusClass}">
                    ${escapeHTML(status.toUpperCase())}
                </td>

                <td>${escapeHTML(formatDate(order.created_at))}</td>

                <td>
                    <button type="button" data-order-id="${escapeHTML(order.order_id)}">
                        View
                    </button>
                </td>
            </tr>
        `;
    }).join("");
}

document.getElementById("order-search").addEventListener("input", event => {
    const search = event.target.value.toLowerCase().trim();

    const filtered = allOrders.filter(order =>
        [
            order.order_id,
            order.customer_name,
            order.customer_email,
            order.customer_phone
        ].some(value => String(value || "").toLowerCase().includes(search))
    );

    renderOrders(filtered);
});

ordersTableBody.addEventListener("click", event => {
    const button = event.target.closest("[data-order-id]");

    if (!button) return;

    const order = allOrders.find(
        item => String(item.order_id) === button.dataset.orderId
    );

    if (order) {
        showOrderDetails(order);
    }
});

// ==========================================
// ORDER DETAILS
// ==========================================

function showOrderDetails(order) {
    const items = Array.isArray(order.items) ? order.items : [];

    const itemHTML = items.map(item => `
        <div class="order-item">
            <strong>${escapeHTML(item.productName)}</strong><br>
            Quantity: ${Number(item.quantity)}<br>
            Unit price: ${formatRupees(item.unitPrice)}
        </div>
    `).join("");

    orderDetailsContent.innerHTML = `
        <p><strong>Order ID:</strong> ${escapeHTML(order.order_id)}</p>
        <p><strong>Payment ID:</strong> ${escapeHTML(order.payment_id || "—")}</p>
        <p><strong>Customer:</strong> ${escapeHTML(order.customer_name)}</p>
        <p><strong>Email:</strong> ${escapeHTML(order.customer_email)}</p>
        <p><strong>Phone:</strong> ${escapeHTML(order.customer_phone || "—")}</p>
        <p><strong>Address:</strong> ${escapeHTML(order.shipping_address || "—")}</p>
        <p><strong>Payment Status:</strong> ${escapeHTML(String(order.status || "").toUpperCase())}</p>
        <p><strong>Order Amount:</strong> ${formatRupees(Number(order.amount || 0) / 100)}</p>
        <p><strong>Created:</strong> ${escapeHTML(formatDate(order.created_at))}</p>
        <p><strong>Paid At:</strong> ${escapeHTML(formatDate(order.paid_at))}</p>

        <h3>Purchased Products</h3>
        ${itemHTML || "<p>No item details available.</p>"}
    `;

    orderDialog.showModal();
}

document.getElementById("close-order-dialog").addEventListener("click", () => {
    orderDialog.close();
});

orderDialog.addEventListener("click", event => {
    if (event.target === orderDialog) {
        orderDialog.close();
    }
});

// ==========================================
// INITIAL SESSION CHECK
// ==========================================

if (adminToken) {
    openDashboard();
} else {
    loginScreen.classList.remove("hidden");
    adminApp.classList.add("hidden");
}
