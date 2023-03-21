"use strict";


const BASE_URL = "/api/cupcakes";
const $cupcakeList = $("#cupcake-list");
const $flavor = $("#flavor");
const $size = $("#size");
const $rating = $("#rating");
const $image = $("#image");
const $form = $("#new-cupcake-form")
/**
 * Gets info about all cupcakes from API
 * Returns array of cupcakes [{id, flavor, size, rating, image}...]
 */
async function getCupcakes() {
    const response = await axios.get(BASE_URL);

    return response.data.cupcakes;
}

/** Displays cupcakes */
async function displayCupakes() {

    const cupcakes = await getCupcakes();
    for (const cupcake of cupcakes) {
        displayCupcake(cupcake);
    }

}

/** takes a single cupcake and returns jquery cupcake */
function displayCupcake(cupcake) {
    const $cupcake = $("<div class = 'col-4'></div>");
    $cupcake.append(`<image src="${cupcake.image}" style= 'width:100%'></image>`);
    $cupcake.append(`<p>Flavor : ${cupcake.flavor}</p>`);
    $cupcake.append(`<p>Size : ${cupcake.size}</p>`);
    $cupcake.append(`<p>Rating : ${cupcake.rating}</p>`);
    $cupcakeList.append($cupcake);

}

/** Send cupcake to API and display in browser */
async function handleAddCupcake(evt) {
    evt.preventDefault();

    const response = await axios({
        method: "POST",
        url: BASE_URL,
        data: {
            flavor: $flavor.val(),
            size: $size.val(),
            rating: $rating.val(),
            image: $image.val()
        }
    })
    displayCupcake(response.data.cupcake);
}

$form.on("submit", handleAddCupcake)

displayCupakes();