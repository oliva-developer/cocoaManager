let price_unit = null
let units = null
let total_net = null
let ispaid = null
let paid = null

document.addEventListener("DOMContentLoaded", function(event){
    price_unit = document.querySelector("#id_price_unit")
    units = document.querySelector("#id_units")
    total_net = document.querySelector("#id_total_net")
    ispaid = document.querySelector("#id_is_paid")
    paid = document.querySelector("#id_paid")
    
    setTimeout(()=>{
       initPriceUnit()
       initUnits() 
       initTotalNet()
       initIsPaid()
       initPaid()
    })
})
function initPriceUnit(){
    price_unit.min = "5"
    setPriceUnit()
    price_unit.addEventListener("input", function(event){
        setPriceUnit()
    })
}
function setPriceUnit(max="200"){
    price_unit.value = Math.min(price_unit.value || 0, max).toFixed(2)
}
function initUnits(){
    units.min = "1"
    setUnits()
    units.addEventListener("input", function(event){
        setUnits()
    })
}
function setUnits(max="900000"){
    units.value = Math.min(units.value || 0, max).toFixed(3)
}
function initTotalNet() {
    total_net.min = "0"
    let max = "100000"
    total_net.value = Math.min(parseFloat(total_net.value || total_net.min), max).toFixed(2)
    total_net.addEventListener("input", function(event){
        total_net.value = Math.min(parseFloat(total_net.value || 0), max).toFixed(2)
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
    let max = parseFloat(total_net.value || 0)
    paid.value = Math.min(parseFloat(paid.value || 0), max).toFixed(2)
    paid.addEventListener("input", function(event) { 
        max = parseFloat(total_net.value || 0)
        paid.value = Math.min(parseFloat(paid.value || 0), max).toFixed(2)
        if(paid.value == total_net.value){
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
    paid.value = (parseFloat(total_net.value) || 0).toFixed(2)
}

function droPaid() {
    paid.readOnly = false
    paid.style.backgroundColor = ""
    paid.value = (0).toFixed(2)
}