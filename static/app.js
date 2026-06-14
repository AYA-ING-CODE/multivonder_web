//add animations------------------------------------------
const modal = document.getElementById("formModal");
let isEditMode = false;
let product_Id = null;

document.getElementById("open_addFormBtn").addEventListener("click", () => {
  modal.classList.remove("hidden");
  document.getElementById("submitBtn").textContent = "Add";
  isEditMode = false;
  product_Id = null;
});
function open_modifyFormBtn(productId,name, description, category, price){
  isEditMode = true;
  product_Id = productId;
  document.getElementById("name").value = name;
  document.getElementById("description").value = description;
  document.getElementById("category").value = category;
  document.getElementById("price").value = price;
  document.getElementById("submitBtn").textContent = "Save";
  document.querySelector(".modal-content h3").textContent = "Modify Product";
  modal.classList.remove("hidden");
}


function closeForm() {
  modal.classList.add("hidden");
}

function handleSubmit(){ //to know what us the form mod and wat we do withr data

    if(isEditMode){
        modifyProduct(product_Id);
    }
    else{
        add_product();
    }

}
//-------login request-------------------------------------

function getCSRF() {
    const match = document.cookie.match(/csrftoken=([^;]+)/);
    return match ? match[1] : null;
}

function login(){
    fetch("/loginBOUTOUN/", {
        method: "POST",
        credentials: "include",   // مهم للكوكيز
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRF() 
        },
        body: JSON.stringify({
            usernam : document.getElementById("usernam").value,
            password: document.getElementById("password").value
        })
    })
    .then(res => res.json())
    .then(data => {
    console.log("LOGIN:", data);

    if (data.message === "logged in") {
        window.location.href = "/home/";
    }
});
}
function register(){
    fetch("/registerBOUTOUN/", {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRF() 
        },
        body: JSON.stringify({
            usernam: document.getElementById("usernam").value,
            password: document.getElementById("password").value
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("REGISTER:", data);

         if (data.message === "user created") {
        window.location.href = "/home/";
    }
    });
}
//--------------add.delet. modifay.products rquest------------------------------

function add_product() {

  const formData = new FormData();

  formData.append("name", document.getElementById("name").value);
  formData.append("description", document.getElementById("description").value);
  formData.append("category", document.getElementById("category").value);
  formData.append("price", document.getElementById("price").value);

  const image = document.getElementById("image").files[0];
  formData.append("image", image);

    fetch("/profile/add-product/", {
        method: "POST",
        credentials: "include",
        headers: {
           
            "X-CSRFToken": getCSRF() 
        },
        body: formData    
    })
   .then(res => res.json())
   .then(data => {
    alert("Product added!");
    closeForm();
    if(data.message === "Product added successfully"){
            location.reload();
    }
   })
   .catch(err => console.log(err))
   
}

function modifyProduct(productId){

    const formData = new FormData();

    formData.append("name", document.getElementById("name").value);
    formData.append("description", document.getElementById("description").value);
    formData.append("category", document.getElementById("category").value);
    formData.append("price", document.getElementById("price").value);
    formData.append("id", productId);
    const image = document.getElementById("image").files[0];
    formData.append("image", image);


    fetch("/profile/modifyProduct/", {

        method: "POST", //لم نستعمل بوت  لكي تكون قرائة المعلومات سهلة من السرفر put
        credentials: "include",

        headers: {
            
            "X-CSRFToken": getCSRF()
        },

        body: formData    
    })

    .then(res => res.json())
    .then(data => {

        console.log(data);

        if(data.message === "Product modify successfully"){
            location.reload();
        }
  
    })
    .catch(err => console.log(err));
}


function deleteProduct(productId){

    const confirmDelete = confirm("Are you sure?");

    if(!confirmDelete){
        return;
    }


    fetch("/profile/delete-product/", {

        method: "DELETE",
        credentials: "include",

        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRF()
        },

        body: JSON.stringify({
            id: productId
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




