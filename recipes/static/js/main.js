const onkeyupfun = e => {
	setTimeout(function(){
		search(e);
	}, 300);
}

const search = e => {
    fetch("/find?keyword="+e.target.value)
        .then(data => data.json())
        .then(data => {
            let elements = data.recipes.map(recipe => {
                return `
                    <div class="recipe-add-cell">
                        <h4>${recipe.title}</h4>
                        <a href="/recipe/${recipe.id}" class="btn btn-primary">View</a>
                    </div>
                `
            });

            document.getElementById("recipe-container").innerHTML = elements;
        })
        .catch(err => console.log(err))
};


