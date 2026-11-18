
 // =====================================
 // VJAYA ROBOTICS STORE - APP
 // =====================================

let selectedCategory = "All";
let currentSearch = "";
let sortOrder = "default";

// =====================================
// SHIPPING STATE
// =====================================

let currentShippingQuote = null;
let shippingRequestId = 0;

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
// PAYMENT API
// =====================================

const PAYMENT_API = "https://vjaya-robotics-api.onrender.com";

// =====================================
// SHIPPING HELPERS
// =====================================

function getDeliveryPincode() {
    const input = document.getElementById("delivery-pincode");

    return input ? input.value.trim() : "";
}

function getCartSignature() {
    return cart
        .map(item => `${item.id}:${item.quantity}`)
        .sort()
        .join("|");
}

function invalidateShippingQuote(message = "") {
    currentShippingQuote = null;

    // Cancel any previous quote request logically.
    shippingRequestId++;

    const shippingChargeElement =
        document.getElementById("shipping-charge");

    const finalTotalElement =
        document.getElementById("final-total");

    const shippingStatus =
        document.getElementById("shipping-status");

    const checkoutButton =
        document.getElementById("checkout-button");

    if (shippingChargeElement) {
        shippingChargeElement.textContent = "Not calculated";
    }

    if (finalTotalElement) {
        const subtotal = cart.reduce(
            (sum, item) => sum + item.price * item.quantity,
            0
        );

        finalTotalElement.textContent =
            `₹${subtotal.toLocaleString("en-IN")}`;
    }

    if (shippingStatus) {
        shippingStatus.textContent =
            message ||
            "Enter your delivery PIN code to calculate shipping automatically.";
    }

    if (checkoutButton) {
        checkoutButton.disabled = true;
    }
}

function updateCheckoutButton() {
    const checkoutButton =
        document.getElementById("checkout-button");

    if (!checkoutButton) return;

    const validQuote =
        currentShippingQuote &&
        currentShippingQuote.pincode === getDeliveryPincode() &&
        currentShippingQuote.cartSignature === getCartSignature();

    checkoutButton.disabled =
        !cart.length || !validQuote;

    checkoutButton.textContent = "Continue to checkout";
}

function displayShippingQuote(quote) {
    const shippingChargeElement =
        document.getElementById("shipping-charge");

    const finalTotalElement =
        document.getElementById("final-total");

    const shippingStatus =
        document.getElementById("shipping-status");

    const subtotal = cart.reduce(
        (sum, item) => sum + item.price * item.quantity,
        0
    );

    if (shippingChargeElement) {
        shippingChargeElement.textContent =
            `₹${quote.shippingCharge.toLocaleString("en-IN")}`;
    }

    if (finalTotalElement) {
        finalTotalElement.textContent =
            `₹${(subtotal + quote.shippingCharge).toLocaleString("en-IN")}`;
    }

    if (shippingStatus) {
        shippingStatus.textContent =
            `Courier: ${quote.courierName || "Available"} | ` +
            `Estimated delivery: ${quote.deliveryEstimate || "To be confirmed"}`;
    }

    updateCheckoutButton();
}

// =====================================
// AUTOMATIC SHIPPING CALCULATION
// =====================================

async function calculateShippingAutomatically() {

    const pincode = getDeliveryPincode();

    // No products in cart.
    if (!cart.length) {
        invalidateShippingQuote("Your cart is empty.");
        return;
    }

    // Wait until the customer enters a valid PIN.
    if (!/^[0-9]{6}$/.test(pincode)) {
        invalidateShippingQuote(
            "Enter a valid 6-digit delivery PIN code."
        );
        return;
    }

    const cartSignature = getCartSignature();

    // Avoid unnecessary duplicate API calls.
    if (
        currentShippingQuote &&
        currentShippingQuote.pincode === pincode &&
        currentShippingQuote.cartSignature === cartSignature
    ) {
        displayShippingQuote(currentShippingQuote);
        return;
    }

    const shippingStatus =
        document.getElementById("shipping-status");

    const checkoutButton =
        document.getElementById("checkout-button");

    if (shippingStatus) {
        shippingStatus.textContent =
            "Calculating delivery charge...";
    }

    if (checkoutButton) {
        checkoutButton.disabled = true;
    }

    const requestId = ++shippingRequestId;

    try {
        const response = await fetch(
            `${PAYMENT_API}/api/shipping-rate`,
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
                    deliveryPincode: pincode
                })
            }
        );

        const data = await response.json();

        // Ignore an outdated request.
        if (requestId !== shippingRequestId) {
            return;
        }

        if (!response.ok || !data.success) {
            throw new Error(
                data.message || "Unable to calculate shipping."
            );
        }

        currentShippingQuote = {
            shippingCharge: Number(data.shippingCharge),
            courierName: data.courierName,
            deliveryEstimate: data.deliveryEstimate,
            pincode: pincode,
            cartSignature: cartSignature
        };

        displayShippingQuote(currentShippingQuote);

    } catch (error) {

        if (requestId !== shippingRequestId) {
            return;
        }

        currentShippingQuote = null;

        if (shippingStatus) {
            shippingStatus.textContent =
                error.message ||
                "Unable to calculate delivery charge. Please try again.";
        }

        if (checkoutButton) {
            checkoutButton.disabled = true;
        }

        const shippingChargeElement =
            document.getElementById("shipping-charge");

        if (shippingChargeElement) {
            shippingChargeElement.textContent = "Unavailable";
        }

        console.error("Shipping calculation error:", error);
    }
}

// =====================================
// RAZORPAY CHECKOUT
// =====================================

async function startCheckout() {

    const checkoutButton =
        document.getElementById("checkout-button");

    if (!cart.length) {
        alert("Your cart is empty.");
        return;
    }

    const customerForm =
        document.getElementById("customer-details");

    if (!customerForm.reportValidity()) {
        return;
    }

    const deliveryPincode = getDeliveryPincode();

    if (!/^[0-9]{6}$/.test(deliveryPincode)) {
        alert("Please enter a valid 6-digit delivery PIN code.");
        return;
    }

    // Ensure the shipping quote matches the current cart and PIN.
    if (
        !currentShippingQuote ||
        currentShippingQuote.pincode !== deliveryPincode ||
        currentShippingQuote.cartSignature !== getCartSignature()
    ) {
        alert("Please wait while we calculate your delivery charge.");

        await calculateShippingAutomatically();

        if (!currentShippingQuote) {
            return;
        }
    }

    const customer = {
        name: document.getElementById("customer-name").value.trim(),
        email: document.getElementById("customer-email").value.trim(),
        phone: document.getElementById("customer-phone").value.trim(),
        address: document.getElementById("customer-address").value.trim()
    };

    if (typeof Razorpay === "undefined") {
        alert(
            "Razorpay Checkout could not load. Check your internet connection."
        );
        return;
    }

    checkoutButton.disabled = true;
    checkoutButton.textContent = "Preparing payment...";

    try {

        // ------------------------------------------
        // STEP 1: CREATE BACKEND ORDER
        // ------------------------------------------

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
                    customer: customer,
                    deliveryPincode: deliveryPincode
                })
            }
        );

        const orderData = await orderResponse.json();

        if (!orderResponse.ok || !orderData.success) {
            throw new Error(
                orderData.message || "Could not create order."
            );
        }

        // Update the cart with the final server-calculated shipping.
        if (
            typeof orderData.shippingCharge === "number" &&
            typeof orderData.finalTotal === "number"
        ) {
            currentShippingQuote = {
                shippingCharge: orderData.shippingCharge,
                courierName: orderData.courierName,
                deliveryEstimate: orderData.deliveryEstimate,
                pincode: deliveryPincode,
                cartSignature: getCartSignature()
            };

            displayShippingQuote(currentShippingQuote);
        }

        // ------------------------------------------
        // STEP 2: OPEN RAZORPAY CHECKOUT
        // ------------------------------------------

        const options = {
            key: orderData.key,
            amount: orderData.order.amount,
            currency: orderData.order.currency,
            name: "VJaYa Robotics",
            description: "Robotics Store Purchase",
            order_id: orderData.order.id,

            handler: async function (response) {

                try {

                    // ------------------------------------------
                    // STEP 3: VERIFY PAYMENT ON BACKEND
                    // ------------------------------------------

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

                    const verifyData =
                        await verifyResponse.json();

                    if (
                        !verifyResponse.ok ||
                        !verifyData.success
                    ) {
                        throw new Error(
                            verifyData.message ||
                            "Payment verification failed."
                        );
                    }

                    alert(
                        "Payment successful!\n" +
                        "Payment ID: " + verifyData.paymentId +
                        "\nOrder ID: " + verifyData.orderId
                    );

                    // ------------------------------------------
                    // CLEAR CART AFTER VERIFIED PAYMENT
                    // ------------------------------------------

                    cart.length = 0;

                    renderCart();

                    invalidateShippingQuote(
                        "Your cart is empty."
                    );

                    setCartOpen(false);

                } catch (error) {

                    alert(
                        "Payment verification issue: " +
                        error.message
                    );

                } finally {

                    checkoutButton.disabled = true;
                    checkoutButton.textContent =
                        "Continue to checkout";
                }
            },

            modal: {
                ondismiss: function () {
                    updateCheckoutButton();
                    checkoutButton.textContent =
                        "Continue to checkout";
                }
            },

            theme: {
                color: "#62e6c5"
            }
        };

        const razorpayCheckout =
            new Razorpay(options);

        razorpayCheckout.on(
            "payment.failed",
            function (response) {

                alert(
                    "Payment failed: " +
                    (
                        response.error.description ||
                        "Please try again."
                    )
                );

                updateCheckoutButton();

                checkoutButton.textContent =
                    "Continue to checkout";
            }
        );

        razorpayCheckout.open();

    } catch (error) {

        alert("Checkout error: " + error.message);

        updateCheckoutButton();

        checkoutButton.textContent =
            "Continue to checkout";
    }
}

// =====================================
// INITIALIZE WEBSITE
// =====================================

document.addEventListener("DOMContentLoaded", () => {

    // ------------------------------------------
    // PRODUCT SEARCH
    // ------------------------------------------

    document.getElementById("product-search")
        .addEventListener("input", event => {
            searchProducts(event.target.value);
        });

    // ------------------------------------------
    // ADD AND REMOVE CART ITEMS
    // ------------------------------------------

    document.addEventListener("click", event => {

        const addButton =
            event.target.closest("[data-add]");

        const removeButton =
            event.target.closest("[data-remove]");

        if (addButton && !addButton.disabled) {

            addToCart(Number(addButton.dataset.add));

            // Cart changed. Shipping must be recalculated.
            invalidateShippingQuote(
                "Cart updated. Recalculating delivery charge..."
            );

            calculateShippingAutomatically();
        }

        if (removeButton) {

            removeFromCart(
                Number(removeButton.dataset.remove)
            );

            // Cart changed. Shipping must be recalculated.
            invalidateShippingQuote(
                "Cart updated. Recalculating delivery charge..."
            );

            calculateShippingAutomatically();
        }
    });

    // ------------------------------------------
    // CART CONTROLS
    // ------------------------------------------

    document.getElementById("cart-toggle")
        .addEventListener("click", () => setCartOpen(true));

    document.getElementById("cart-close")
        .addEventListener("click", () => setCartOpen(false));

    document.getElementById("cart-backdrop")
        .addEventListener("click", () => setCartOpen(false));

    // ------------------------------------------
    // AUTOMATIC SHIPPING WHEN PIN CODE CHANGES
    // ------------------------------------------

    const pincodeInput =
        document.getElementById("delivery-pincode");

    if (pincodeInput) {

        pincodeInput.addEventListener("input", () => {

            invalidateShippingQuote(
                "Enter a valid 6-digit PIN code to calculate shipping."
            );

            // Automatically calculate once the PIN is complete.
            if (/^[0-9]{6}$/.test(pincodeInput.value.trim())) {
                calculateShippingAutomatically();
            }
        });
    }

    // ------------------------------------------
    // REMOVE OLD CALCULATE SHIPPING BUTTON
    // ------------------------------------------

    const calculateShippingButton =
        document.getElementById("calculate-shipping-button");

    if (calculateShippingButton) {
        calculateShippingButton.remove();
    }

    // ------------------------------------------
    // CHECKOUT
    // ------------------------------------------

    document.getElementById("checkout-button")
        .addEventListener("click", startCheckout);

    // Checkout starts disabled.
    document.getElementById("checkout-button").disabled = true;

    // ------------------------------------------
    // FOOTER YEAR
    // ------------------------------------------

    document.getElementById("year").textContent =
        new Date().getFullYear();

    // ------------------------------------------
    // INITIAL RENDERING
    // ------------------------------------------

    renderProducts();
    renderCart();

    invalidateShippingQuote(
        "Enter your delivery PIN code to calculate shipping automatically."
    );
});
