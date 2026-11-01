
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

    document.getElementById("product-grid")
        .scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
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
        .addEventListener("click", () => {
            alert(
                "This is the starter demo. Online checkout and payments will be connected later."
            );
        });

    // Footer year
    document.getElementById("year").textContent =
        new Date().getFullYear();

    // Initial rendering
    renderProducts();
    renderCart();
});
