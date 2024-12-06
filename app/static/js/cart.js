document.addEventListener('DOMContentLoaded', function () {
    // Function to update cart count dynamically
    function updateCartCount(count) {
        document.getElementById('cart-count').textContent = count;
    }

    // Add event listeners for plus, minus, and remove buttons
    document.querySelectorAll('.plus-cart, .minus-cart, .remove-cart').forEach(button => {
        button.addEventListener('click', function (e) {
            const pid = this.getAttribute('pid');
            const action = this.classList.contains('plus-cart') ? 'add' :
                           this.classList.contains('minus-cart') ? 'subtract' : 'remove';

            // Make an AJAX call to update cart
            fetch(`/update-cart/${pid}/${action}/`, { method: 'POST', headers: { 'X-CSRFToken': csrftoken } })
                .then(response => response.json())
                .then(data => {
                    // Update quantity, total, and cart count
                    document.querySelector(`#quantity-${pid}`).textContent = data.quantity;
                    document.querySelector(`#cart-item-${pid} .item-total`).textContent = `Ksh. ${data.item_total}`;
                    document.getElementById('amount').textContent = `Ksh. ${data.cart_amount}`;
                    document.getElementById('total').textContent = `Ksh. ${data.cart_total}`;
                    updateCartCount(data.cart_count);

                    // If quantity is 0, remove item from cart
                    if (data.quantity === 0) {
                        document.getElementById(`cart-item-${pid}`).remove();
                    }
                });
        });
    });
});
