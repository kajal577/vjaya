
// =====================================
// VJAYA ROBOTICS STORE - APP
// =====================================

let selectedCategory = "All";
let currentSearch = "";
let sortOrder = "default";

// =====================================
// RENDER PRODUCTS
// =====================================

function renderProducts() {
    const grid = document.getElementById("product-grid");

    let filtered = products.filter(product => {
        const matchesCategory =
            selectedCategory === "All" ||
            product.category === selectedCategory;

        const searchContent =
            `${product.name} ${product.category} ${product.description}`.toLowerCase();

        const matchesSearch =
            searchContent.includes(currentSearch.toLowerCase());

        return matchesCategory && matchesSearch;
    });

    if (sortOrder === "low") {
        filtered.sort((a, b) => a.price - b.price);
    }

    if (sortOrder === "high") {
        filtered.sort((a, b) => b.price - a.price);
    }

    if (!filtered.length) {
        grid.innerHTML =
            '<p class="empty-cart">No matching products found.</p>';
        return;
    }

    grid.innerHTML = filtered.map(product => {

        const stock = Number(product.stock ?? 0);
        const outOfStock = stock <= 0;

        const productImage = product.image
            ? `
                <img
                    class="product-image"
                    src="${product.image}"
                    alt="${product.name}"
                    loading="lazy"
                    onerror="this.hidden=true; this.nextElementSibling.hidden=false;"
                >
                <div class="product-image-fallback" hidden>
                    ${product.icon}
                </div>
            `
            : `
                <div class="product-image-fallback">
                    ${product.icon}
                </div>
            `;

        return `
            <article class="product-card">

                <div class="product-art">
                    ${productImage}
                </div>

                <div class="product-info">

                    <p class="eyebrow">
                        ${product.category}
                    </p>

                    <h3>${product.name}</h3>

                    <p>${product.description}</p>

                    <p class="stock-status ${outOfStock ? "out-of-stock" : "in-stock"}">
                        ${outOfStock
                            ? "Out of stock"
                            : `In stock: ${stock}`}
                    </p>

                    <div class="product-bottom">

                        <span class="price">
                            ₹${product.price.toLocaleString("en-IN")}
                        </span>

                        <button
                            class="add-button"
                            data-add="${product.id}"
                            type="button"
                            ${outOfStock ? "disabled" : ""}>
                            ${outOfStock ? "Unavailable" : "Add to cart"}
                        </button>

                    </div>

                </div>
            </article>
        `;
    }).join("");
}

// =====================================
// CATEGORY FILTER
// =====================================

function filterCategory(category) {
    selectedCategory = category;

    document.querySelectorAll(".category-filters button")
        .forEach(button => {
            button.classList.toggle(
                "active",
                button.dataset.category === category
            );
        });

    renderProducts();
}

// =====================================
// PRODUCT SEARCH
// =====================================

function searchProducts(value) {
    currentSearch = value;
    renderProducts();
}

// =====================================
// PRICE SORTING
// =====================================

function sortProducts(value) {
    sortOrder = value;
    renderProducts();
}

// =====================================
// CART PANEL
// =====================================

function setCartOpen(isOpen) {
    document.getElementById("cart-panel")
        .classList.toggle("open", isOpen);

    document.getElementById("cart-panel")
        .setAttribute("aria-hidden", String(!isOpen));

    document.getElementById("cart-backdrop")
        .classList.toggle("show", isOpen);
}

// =====================================
// INITIALIZE WEBSITE
// =====================================


// ==========================================
// RAZORPAY CHECKOUT INTEGRATION
// ==========================================

// Local testing server.
// Change this URL when the backend is deployed.
const PAYMENT_API = "http://localhost:5000";

async function startCheckout() {
    const checkoutButton = document.getElementById("checkout-button");

    if (!cart.length) {
        alert("Your cart is empty.");
        return;
    }

    const customerForm = document.getElementById("customer-details");

if (!customerForm.reportValidity()) return;

const customer = {
    name: document.getElementById("customer-name").value.trim(),
    email: document.getElementById("customer-email").value.trim(),
    phone: document.getElementById("customer-phone").value.trim(),
    address: document.getElementById("customer-address").value.trim()
};

    if (typeof Razorpay === "undefined") {
        alert("Razorpay Checkout could not load. Check your internet connection.");
        return;
    }

    checkoutButton.disabled = true;
    checkoutButton.textContent = "Preparing payment...";

    try {
        // Step 1: Ask backend to create a trusted order.
        const orderResponse = await fetch(
            `${PAYMENT_API}/api/create-order`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    items: cart.map(item => ({
                        id: item.id,
                        quantity: item.quantity
                    })),
                     customer: customer
                })
            }
        );

        const orderData = await orderResponse.json();

        if (!orderResponse.ok || !orderData.success) {
            throw new Error(orderData.message || "Could not create order.");
        }

        // Step 2: Open Razorpay Checkout.
        const options = {
            key: orderData.key,
            amount: orderData.order.amount,
            currency: orderData.order.currency,
            name: "VJaYa Robotics",
            description: "Robotics Store Purchase",
            order_id: orderData.order.id,

            handler: async function (response) {
                try {
                    // Step 3: Verify payment on backend.
                    const verifyResponse = await fetch(
                        `${PAYMENT_API}/api/verify-payment`,
                        {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify(response)
                        }
                    );

                    const verifyData = await verifyResponse.json();

                    if (!verifyResponse.ok || !verifyData.success) {
                        throw new Error(
                            verifyData.message || "Payment verification failed."
                        );
                    }

                    alert(
                        "Payment successful!\n" +
                        "Payment ID: " + verifyData.paymentId
                    );

                    // Clear cart only after server verification.
                    cart.length = 0;
                    renderCart();
                    setCartOpen(false);

                } catch (error) {
                    alert("Payment verification issue: " + error.message);
                } finally {
                    checkoutButton.disabled = false;
                    checkoutButton.textContent = "Checkout";
                }
            },

            modal: {
                ondismiss: function () {
                    checkoutButton.disabled = false;
                    checkoutButton.textContent = "Checkout";
                }
            },

            theme: {
                color: "#62e6c5"
            }
        };

        const razorpayCheckout = new Razorpay(options);

        razorpayCheckout.on("payment.failed", function (response) {
            alert(
                "Payment failed: " +
                (response.error.description || "Please try again.")
            );

            checkoutButton.disabled = false;
            checkoutButton.textContent = "Checkout";
        });

        razorpayCheckout.open();

    } catch (error) {
        alert("Checkout error: " + error.message);

        checkoutButton.disabled = false;
        checkoutButton.textContent = "Checkout";
    }
}


document.addEventListener("DOMContentLoaded", () => {

    // Product search
    document.getElementById("product-search")
        .addEventListener("input", event => {
            searchProducts(event.target.value);
        });

    // Add and remove cart items
    document.addEventListener("click", event => {

        const addButton = event.target.closest("[data-add]");
        const removeButton = event.target.closest("[data-remove]");

        if (addButton && !addButton.disabled) {
            addToCart(Number(addButton.dataset.add));
        }

        if (removeButton) {
            removeFromCart(Number(removeButton.dataset.remove));
        }
    });

    // Cart controls
    document.getElementById("cart-toggle")
        .addEventListener("click", () => setCartOpen(true));

    document.getElementById("cart-close")
        .addEventListener("click", () => setCartOpen(false));

    document.getElementById("cart-backdrop")
        .addEventListener("click", () => setCartOpen(false));

    // Checkout demo
    
    document.getElementById("checkout-button")
    .addEventListener("click", startCheckout);

    // Footer year
    document.getElementById("year").textContent =
        new Date().getFullYear();

    // Initial rendering
    renderProducts();
    renderCart();
});
