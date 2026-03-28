// // generating tile logic


function displayTiles(articles) {

    const container = document.querySelector(".tile-container");

    container.innerHTML = "" // set everything blank

    if (!articles || articles.length === 0) {
        container.innerHTML = `
            <div class="title">
            <h2> No Results Yet </h2>
            <p> Enter a query to search for an article </p>
            </div>`;
        return; // this should be the default for the page when everything is loaded up
    }

    articles.forEach(article => {
    const tile = document.createElement("div");
    tile.classList.add("tile");

    tile.innerHTML = `
      <h2>${article.title}</h2>
      <p>${article.description}</p>
    `;
    // fetch every news article title and its content  and display in paragraph tag
    // may need to shortern this and include a preview button later.

    container.appendChild(tile);
  });


  

}



displayTiles([]); //by default assume we load blank page w no queriews 



class SearchForm {
    constructor() {
        this.form = document.getElementById("searchForm");
        this.form.addEventListener("submit",this.handleSubmit.bind(this));
        
    }

    handleSubmit(e) {
        e.preventDefault(); // this is what prevent a redirect to the JSON output

            const query = document.querySelector('input[name="query"]').value;
            const model = document.querySelector('select[name="model"]').value;
            const topN = document.querySelector('select[name="topN"]').value;
            fetch(`/search_api?query=${encodeURIComponent(query)}&model=${encodeURIComponent(model)}&topN=${encodeURIComponent(topN)}`).then(response => response.json()).then(data => {
            console.log(data); // just for debutging purposes 
            displayTiles(data); // update site with relevant articles
        })
        // simple fecth to out API 

        //TODO 
        //implement loading logic to communicate loading times

        //also our BM25 implementation could do with a Tad bit of a speed up --> remember to memoise the TF it could shave off seconds 
        

    }
}

new SearchForm();