let cost = null
let ispaid = null
let paid = null

document.addEventListener("DOMContentLoaded", function(){
    cost = document.querySelector("#id_cost")
    ispaid = document.querySelector("#id_is_paid")
    paid = document.querySelector("#id_paid")
    total_net = document.querySelector("#id_total_net")
    ispaid = document.querySelector("#id_is_paid")
    paid = document.querySelector("#id_paid")

    setTimeout(function(){
        initCost()
        initIsPaid()
        initPaid()

    })
})
function initCost() {
    cost.min = "0"
    let max = "100000"
    cost.value = Math.min(parseFloat(cost.value || cost.min), max).toFixed(2)
    cost.addEventListener("input", function(event){
        cost.value = Math.min(parseFloat(cost.value || 0), max).toFixed(2)
        ispaid.checked = false
        ispaid.dispatchEvent(new Event("change", { bubbles: true }));
    })
}
function initIsPaid() {
    const togglePaid = () => ispaid.checked ? roPaid() : droPaid();
    
    togglePaid();
    ispaid.addEventListener("change", togglePaid);
}
function initPaid() {
    paid.min = "0"
    let max = parseFloat(cost.value || 0)
    paid.value = Math.min(parseFloat(paid.value || 0), max).toFixed(2)
    paid.addEventListener("input", function(event) { 
        max = parseFloat(cost.value || 0)
        paid.value = Math.min(parseFloat(paid.value || 0), max).toFixed(2)
        if(paid.value == cost.value){
            if(!ispaid.checked){
                ispaid.checked = true
                ispaid.dispatchEvent(new Event("change", { bubbles: true }));
            }
        }
    })
}
function roPaid() {
    paid.readOnly = true
    paid.style.backgroundColor = "#e9ecef"
    paid.value = (parseFloat(cost.value) || 0).toFixed(2)
}

function droPaid() {
    paid.readOnly = false
    paid.style.backgroundColor = ""
    paid.value = (0).toFixed(2)
}