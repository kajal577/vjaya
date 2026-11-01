// Cart state and cart operations are kept separate from the page rendering.
const cart = [];

function addToCart(productId) {
  const product = products.find(item => item.id === productId);
  if (!product) return;
  const existing = cart.find(item => item.id === productId);
  if (existing) existing.quantity += 1;
  else cart.push({ ...product, quantity: 1 });
  renderCart();
}

function removeFromCart(productId) {
  const index = cart.findIndex(item => item.id === productId);
  if (index !== -1) cart.splice(index, 1);
  renderCart();
}

function renderCart() {
  const itemsElement = document.getElementById('cart-items');
  const count = cart.reduce((sum, item) => sum + item.quantity, 0);
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  document.getElementById('cart-count').textContent = count;
  document.getElementById('cart-total').textContent = `₹${total.toLocaleString('en-IN')}`;

  if (!cart.length) {
    itemsElement.innerHTML = '<p class="empty-cart">Your cart is empty.</p>';
    return;
  }
  itemsElement.innerHTML = cart.map(item => `
    <div class="cart-row">
      <div><strong>${item.name}</strong><small>₹${item.price} × ${item.quantity}</small></div>
      <div><strong>₹${(item.price * item.quantity).toLocaleString('en-IN')}</strong><br><button class="remove-button" data-remove="${item.id}" type="button">Remove</button></div>
    </div>`).join('');
}
