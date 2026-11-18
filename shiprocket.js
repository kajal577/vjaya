
const products = require("./catalogue");

const SHIPROCKET_BASE_URL =
    "https://apiv2.shiprocket.in/v1/external";

const PICKUP_PINCODE = "800001";

// Cache the API token in memory.
let cachedToken = null;
let tokenExpiresAt = 0;


// ------------------------------------------
// SHIPROCKET AUTHENTICATION
// ------------------------------------------

async function getShiprocketToken() {
    if (cachedToken && Date.now() < tokenExpiresAt) {
        return cachedToken;
    }

    const email = process.env.SHIPROCKET_EMAIL;
    const password = process.env.SHIPROCKET_PASSWORD;

    if (!email || !password) {
        throw new Error("Shiprocket credentials are missing.");
    }

    const response = await fetch(
        `${SHIPROCKET_BASE_URL}/auth/login`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                password
            })
        }
    );

    const data = await response.json();

    if (!response.ok || !data.token) {
        throw new Error("Shiprocket authentication failed.");
    }

    cachedToken = data.token;

    // Refresh before the documented 10-day token expiry.
    tokenExpiresAt = Date.now() + (9 * 24 * 60 * 60 * 1000);

    return cachedToken;
}


// ------------------------------------------
// CALCULATE PARCEL FROM CATALOGUE
// ------------------------------------------

function calculateParcel(items) {
    let totalWeightGrams = 0;
    let totalHeight = 0;
    let maximumLength = 0;
    let maximumBreadth = 0;

    for (const item of items) {
        const product = products.find(
            p => p.id === Number(item.id)
        );

        const quantity = Number(item.quantity);

        if (
            !product ||
            !Number.isInteger(quantity) ||
            quantity < 1 ||
            quantity > 20
        ) {
            throw new Error("Invalid cart product or quantity.");
        }

        const weight = Number(product.weightGrams);
        const length = Number(product.lengthCm);
        const breadth = Number(product.breadthCm);
        const height = Number(product.heightCm);

        if (
            !Number.isFinite(weight) || weight <= 0 ||
            !Number.isFinite(length) || length <= 0 ||
            !Number.isFinite(breadth) || breadth <= 0 ||
            !Number.isFinite(height) || height <= 0
        ) {
            throw new Error(
                `Shipping dimensions are missing for ${product.name}.`
            );
        }

        totalWeightGrams += weight * quantity;

        maximumLength = Math.max(maximumLength, length);
        maximumBreadth = Math.max(maximumBreadth, breadth);

        // Conservative stacking estimate for parcel height.
        totalHeight += height * quantity;
    }

    const weightKg = Math.ceil(totalWeightGrams) / 1000;

    return {
        weight: Number(weightKg.toFixed(3)),
        length: Math.ceil(maximumLength),
        breadth: Math.ceil(maximumBreadth),
        height: Math.ceil(totalHeight)
    };
}


// ------------------------------------------
// CHECK COURIER SERVICEABILITY
// ------------------------------------------

async function getShippingQuote(items, deliveryPincode) {
    if (
        typeof deliveryPincode !== "string" ||
        !/^[0-9]{6}$/.test(deliveryPincode)
    ) {
        throw new Error("Please enter a valid 6-digit delivery PIN code.");
    }

    if (!Array.isArray(items) || items.length === 0) {
        throw new Error("Your cart is empty.");
    }

    const parcel = calculateParcel(items);

    let token = await getShiprocketToken();

    async function checkServiceability(authToken) {
        const params = new URLSearchParams({
            pickup_postcode: PICKUP_PINCODE,
            delivery_postcode: deliveryPincode,
            cod: "0",
            weight: String(parcel.weight),
            length: String(parcel.length),
            breadth: String(parcel.breadth),
            height: String(parcel.height)
        });

        return fetch(
            `${SHIPROCKET_BASE_URL}/courier/serviceability/?${params}`,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${authToken}`
                }
            }
        );
    }

    let response = await checkServiceability(token);

    // Refresh an expired or rejected token once.
    if (response.status === 401) {
        cachedToken = null;
        tokenExpiresAt = 0;

        token = await getShiprocketToken();
        response = await checkServiceability(token);
    }

    const data = await response.json();

    if (!response.ok) {
        throw new Error("Shiprocket could not calculate the delivery rate.");
    }

    const couriers =
        data?.data?.available_courier_companies || [];

    const availableCouriers = couriers
        .filter(courier => Number(courier.blocked || 0) === 0)
        .map(courier => ({
            name: courier.courier_name,
            courierId: courier.courier_company_id,
            rate: Number(courier.rate ?? courier.freight_charge),
            deliveryEstimate:
                courier.etd || courier.estimated_delivery_days || null
        }))
        .filter(courier =>
            courier.name &&
            Number.isFinite(courier.rate) &&
            courier.rate > 0
        )
        .sort((a, b) => a.rate - b.rate);

    if (availableCouriers.length === 0) {
        throw new Error(
            "No courier service is available for this delivery PIN code."
        );
    }

    const cheapest = availableCouriers[0];

    return {
        deliveryPincode,
        pickupPincode: PICKUP_PINCODE,
        shippingCharge: Math.ceil(cheapest.rate),
        courierName: cheapest.name,
        deliveryEstimate: cheapest.deliveryEstimate,
        parcel,
        availableCouriers
    };
}


module.exports = {
    getShippingQuote
};
