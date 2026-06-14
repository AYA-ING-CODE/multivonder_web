
//csrf functios--------------------------------------
function getCSRF() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : null;
}
//open form functions--------------------------------------
let currentItemId = null;

function openModal(itemId){
    currentItemId = itemId;
     document.getElementById("formModal").classList.remove("hidden");
}

function closeModal(){
     document.getElementById("formModal").classList.add("hidden");
}



//cart requset-----------------------------------------------
function add_to_cart(id){
        fetch("/cart/add/", {

        method: "POST",
        credentials: "include",

        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRF()
        },

        body: JSON.stringify({
            id: id
        })

    })
    .then(res => res.json())
    .then(data => {

        console.log(data);

        if(data.message === "Added to cart"){
            alert("Product added to cart");
        }

    })
    .catch(err => console.log(err));


}

function remove_from_cart(id){

    const confirmDelete = confirm("Are you sure?");

    if(!confirmDelete){
        return;
    }


    fetch("/cart/remove/", {

        method: "DELETE",
        credentials: "include",

        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRF()
        },

        body: JSON.stringify({
            id: id
        })

    })
    .then(res => res.json())
    .then(data => {

        console.log(data);

        if(data.message === "Product deleted"){
            location.reload();
        }

    })
    .catch(err => console.log(err));

}

function updateQuantity(){

    console.log("clicked");

    const quantity = document.getElementById("quantity").value;

    fetch("/cart/update/", {

        method:"PUT",

        credentials:"include",

        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken": getCSRF()
        },

        body:JSON.stringify({
            item_id: currentItemId,
            quantity: quantity
        })

    })
    .then(res => res.json())
    .then(data => {

        
        if(data.message === "updated"){
            alert("quantity updated ");
            location.reload();
        }

    });

}


function creat_order(){

    const confirmDelete = confirm("Are you sure?");

    if(!confirmDelete){
        return;
    }


    fetch("/cart/creat_order/ ", {

        method: "POST",
        credentials: "include",

        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRF()
        },

        body: JSON.stringify({})

    })
    .then(res => res.json())
    .then(data => {

         

    })
    .catch(err => console.log(err));

}


