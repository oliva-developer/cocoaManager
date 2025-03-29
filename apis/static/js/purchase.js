
let total = null
let ispaid = null 
let paid = null
document.addEventListener("DOMContentLoaded", ()=> {
    total = document.querySelector("#id_total")
    ispaid = document.querySelector("#id_is_paid")  
    paid = document.querySelector("#id_paid")
    setTimeout(function(){
        initTotal()
        initIsPaid()
        initPaid()
        initUnitCost()
        initUnits()
        initCharge()
        initDeleteProduct()
        initAddArticle()
    })
})
function initTotal(){
    total.value = 0.00
    total.readOnly = true
    total.style.backgroundColor = "#e9ecef"
}
function calcTotal(total, charge){
    total.value = (parseFloat(total.value || 0) + parseFloat(charge || 0)).toFixed(2)
}
function initIsPaid(){
    const togglePaid = () => ispaid.checked ? roPaid() : droPaid();
    
    togglePaid();
    ispaid.addEventListener("change", togglePaid);
}
function initPaid(){
    paid.min = "0"
    let max = parseFloat(total.value || 0)
    paid.value = Math.min(parseFloat(paid.value || 0), max).toFixed(2)
    paid.addEventListener("input", function(event) { 
        max = parseFloat(total.value || 0)
        paid.value = Math.min(parseFloat(paid.value || 0), max).toFixed(2)
        if(paid.value == total.value){
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
    paid.value = (parseFloat(total.value) || 0).toFixed(2)
}

function droPaid() {
    console.log("ASD")
    paid.readOnly = false
    paid.style.backgroundColor = ""
    paid.value = (0).toFixed(2)
}
function initUnitCost (){
    document.querySelectorAll("#purchase_form .field-unit_cost input").forEach(function (input) {
        input.min = "0"
        const max = "10000"
        input.value = Math.min(parseFloat(input.value || 0), max).toFixed(2)
        input.addEventListener("input", function (event) {
            input.value = Math.min(parseFloat(input.value || 0), max).toFixed(2)
            initCharge()
        });
    });
}
function initUnits (){
    document.querySelectorAll("#purchase_form .field-units input").forEach(function (input) {
        input.min = "0"
        const max = "10000"
        input.value = Math.min(parseFloat(input.value || 0), max).toFixed(2)
        input.addEventListener("input", function (event) {
            input.value = Math.min(parseFloat(input.value || 0), max).toFixed(2)
            initCharge()
        });
    });
}
function initDeleteProduct (){
    document.querySelectorAll("#purchase_form .delete .inline-deletelink").forEach(function (btn) {
        btn.addEventListener("click", function (event) {
            setTimeout(()=>initCharge())
        });
    });
}
function initCharge(){
    initTotal()
    ispaid.checked = false
    ispaid.dispatchEvent(new Event("change", { bubbles: true }));
    document.querySelectorAll("#purchase_form .field-charge input").forEach(function (input) {
        input.readOnly = true
        input.style.backgroundColor = "#e9ecef"
        let field_charge = input.closest(".field-charge")
        let unit_cost = field_charge.parentElement.querySelector(".field-unit_cost input")
        let units = field_charge.parentElement.querySelector(".field-units input")
        input.value = (parseFloat(unit_cost.value || 0) * parseFloat(units.value || 0)).toFixed(2)
        calcTotal(total, input.value)
    });
}
function initAddArticle (){
    document.querySelector(".add-row a").addEventListener("click", function(event){
        initUnitCost()
        initUnits()
        initDeleteProduct()
    })
}
