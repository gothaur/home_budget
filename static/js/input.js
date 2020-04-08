
document.addEventListener("DOMContentLoaded", function () {
    const inputAmount = document.getElementById("id_amount");
    // const btn = document.getElementById("amount_add");
    const btn = document.getElementById("expenses_form_id");

    btn.addEventListener('submit', function (event) {
        if(inputAmount.value.startsWith("=")){
            const eq = inputAmount.value.trim().substr(1);
            const numbers = /[a-zA-Z!@#$%^&]+/;
            if(eq.match(numbers)){
                alert('...');
            } else {
                let result = eval(eq);
                console.log(result);
                if(isNaN(result)){
                    alert('Aby możliwe było wykonywanie operacji matematycznych, wyrażenie musi się zaczynać od znaku "="');
                    event.preventDefault();
                } else {
                    inputAmount.value = result;
                    btn.submit();
                }
            }
        } else {
            if(isNaN(inputAmount.value)){
                alert('Wprowadź liczbę');
                event.preventDefault();
            } else if(inputAmount.value) {
                inputAmount.value = eval(inputAmount.value);
                btn.submit();
            } else {
                // alert('Kwota nie może być pusta');
                // event.preventDefault();
                // event.target.setCustomValidity("Kwota nie może pozostać pusta!")
            }
        }
        event.preventDefault();
    })
});


// document.addEventListener("DOMContentLoaded", function () {
//     let inputAmount = document.getElementById("id_amount").value;
//     console.log(inputAmount);
//     const btn = document.getElementById("amount_add");
//     btn.addEventListener('click', function (event) {
//         if(inputAmount.startsWith("=")){
//             const eq = inputAmount.trim().substr(1);
//             let result = eval(eq);
//             if(isNaN(result)){
//                 alert('Aby możliwe było wykonywanie operacji matematycznych, wyrażenie musi się zaczynać od znaku "="');
//                 event.preventDefault();
//             } else {
//                 inputAmount = result;
//                 btn.submit();
//             }
//         } else {
//             if(isNaN(inputAmount)){
//                 alert('Wprowadź liczbę');
//                 event.preventDefault();
//             } else {
//                 inputAmount = eval(inputAmount);
//                 btn.submit();
//             }
//         }
//     })
// });
