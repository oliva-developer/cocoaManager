document.addEventListener("DOMContentLoaded", function () {
    handlerTotal()
    handlerIsPaid()
});

charged = 0
function handlerIsPaid(){
    let isPaid = document.querySelector("#id_is_paid");  // Checkbox
    let chargedField = document.querySelector("#id_charged");  // Campo a deshabilitar
    let total = document.querySelector("#id_total");  

    function toggleCharged() {
        if (!isPaid.checked) {
            chargedField.value = charged.toFixed(2)
            chargedField.readOnly = false;
            chargedField.style.backgroundColor = "";  // Restaura el fondo por defecto
        } else {
            chargedField.readOnly = true;
            chargedField.style.backgroundColor = "#e9ecef";  // Color gris claro
            charged = (parseFloat(chargedField.value) || 0)
            chargedField.value = (parseFloat(total.value) || 0).toFixed(2);
        }
    }

    isPaid.addEventListener("change", toggleCharged);
    toggleCharged();  // Ejecutar al cargar la página
}


function handlerTotal(){
    let kilos = document.querySelector("#id_kilos");  
    let price_kilo = document.querySelector("#id_price_kilo");  
    let discount = document.querySelector("#id_discount");  
    let total = document.querySelector("#id_total");  
    total.readOnly = true;
    total.style.backgroundColor = "#e9ecef";

    // MAXIMOS Y MINIMOS
    kilos.min = 0
    price_kilo.min = 0
    discount.min = 0

    function calcTotal() {
        // Establecer límites
        kilos.min = "1";  // Mínimo 1 kilo
        // kilos.max = "50000";  // Máximo 1000 kilos

        price_kilo.min = "0.10";  // Precio mínimo 0.10
        let price_kilo_max = "100";  // Precio máximo 1000

        discount.min = "0";  // Descuento mínimo 0
        let discount_max = ((parseFloat(kilos.value) || 0) * (parseFloat(price_kilo.value) || 0)).toFixed(2); // Máximo = total sin descuento

        // Obtener valores convertidos a número
        let kilosValue = Math.max(parseFloat(kilos.value) || 0, kilos.min);
        let priceValue = Math.max(parseFloat(price_kilo.value) || 0, price_kilo.min);
        priceValue = Math.min(priceValue, price_kilo_max)
        let discountValue = Math.min(parseFloat(discount.value) || 0, discount_max);  

        // Calcular total
        let totalValue = (kilosValue * priceValue) - discountValue;
        total.value = totalValue.toFixed(2);  

        // Corregir valores fuera de rango
        kilos.value = kilosValue.toFixed(3);
        price_kilo.value = priceValue.toFixed(2);
        discount.value = discountValue.toFixed(2);
    }

    kilos.addEventListener("input", calcTotal);
    price_kilo.addEventListener("input", calcTotal);
    discount.addEventListener("input", calcTotal);
    calcTotal()
}