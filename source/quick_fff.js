function getUniqueFontFamilies() {
    const allElements = document.querySelectorAll('*'); // Select all elements on the page
    const fontFamilies = new Set(); // Use a Set to avoid duplicates

    allElements.forEach(element => {
        const style = window.getComputedStyle(element); // Get computed style of the element
        const fontFamily = style.fontFamily; // Get the font-family property
        fontFamilies.add(fontFamily); // Add to Set (Set ensures uniqueness)
    });

    return Array.from(fontFamilies); // Convert the Set to an array and return it
}

const fontList = getUniqueFontFamilies();
console.log(fontList); // Logs all unique font families to the console
