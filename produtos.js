let produtos = [
    {
        id: 1,
        name:"Nescafe",
        price: 5.00,
        Image: "../web_scrap_page/assets/buondi.webp"
    },
    {
        id: 2,
        name:"cafe",
        price: 7.00,
        Image: "../web_scrap_page/assets/continente.webp"
    },
    {
        id: 3,
        name:"nada de cafe",
        price: 8.00,
        Image: "../web_scrap_page/assets/cafe1.jpg"
    }
]

const card_area = document.getElementById("card_area")
function gerar_produtos() {
    
    produtos.forEach(produto => {
      card_area.innerHTML += `
          <div class="card" style="width: 18rem;">
            <img src="${produto.Image}" class="card-img-top" alt="...">
            <div class="card-body">
              <h5 class="card-title">${produto.name}</h5>
              <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
              <button class="price_button btn btn-primary">${produto.price}</button>
            </div>
          </div>
        `
    });
}
gerar_produtos()