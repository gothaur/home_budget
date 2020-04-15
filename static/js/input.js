function checkInput() {
    const inputAmount = document.getElementById("id_amount");

    const forbidden = /[a-zA-Z!@#$%^&]+/;
    let inputValue = inputAmount.value.trim();
    inputValue = inputValue.replace(/,/g, ".");
    if (inputValue.match(forbidden)) {
        inputAmount.setCustomValidity('Dozwolone tylko podstawowe działania matematyczne na liczbach');
    } else if (!inputValue) {
        inputAmount.setCustomValidity('To pole nie może być puste');
    } else if (inputValue.startsWith("=")){
        // const eq = inputValue.substr(1);
        // return inputAmount.value = eval(eq);

        return inputAmount.value = math.evaluate(inputValue.substr(1)).toFixed(2);
    } else {
        inputAmount.setCustomValidity("");
        return inputAmount.value = math.evaluate(inputValue).toFixed(2);
    }
}
