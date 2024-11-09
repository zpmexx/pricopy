var userCart = null;
var userCartItemsCount = 0;
const url = "/aip/"

function setCookie(cname, cvalue, exdays) {
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/; Secure";
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getUserCart() {
    $.ajax({
                url: "/api/menu/cart/"
            }).then(function(data) {
                userCart = data;
                $(document).trigger("userCartLoaded", userCart);
                return userCart;
            }).catch((error) => {
                if(error.status == 401)
                    $(document).trigger("userNotLoged");
                //console.log(error)
                return undefined;
    });
}

function getUserCartItem(idItem) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: "/api/menu/cartproduct/",
            data: {
                id: idItem
            },
        }).then(function (data) {
            $(document).trigger("userCartItemLoaded", data);
            resolve(data);
        }).catch((error) => {
            //console.log(error)
            reject(error);
        });
    })
}


function getProduct(idItem) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: "/api/menu/product/",
            data: {
                id: idItem
            },
        }).then(function (data) {
            resolve(data);
        }).catch((error) => {
            //console.log(error)
            reject(error);
        });
    })
}

function listUserCart(userCartM) {
    let innerHtml = "";
    let totalPrice = 0;
    userCartM.cart_items.map(
        (element, index, array) => {
            let name = element.product.name;
            let quantity = element.quantity;
            let price = element.product.is_promoted ? element.product.promotion_price : element.product.price;
            totalPrice += price*quantity;
            let productid = element.product.id;
            let productslug = element.product.slug;
            let itemid =  element.id;
            let imgSrc = element.product.image;
            innerHtml += "<div class=\"menu-cart-product\" id='" + itemid + "'>"
                            + "<div class=\"menu-cart-product-left\" onclick=\"showPopUp('"+productslug+"')\">"
                                + "<div class=\"menu-cart-product-img\" style=\"background-image: url('" + imgSrc + "')\"></div>"
                                    + "<div class=\"menu-cart-product-name\">" + quantity + " x " + name + "</div>"
                                + "</div>"
                                + "<div class=\"menu-cart-product-quantity\">"
                                + "<div class=\"menu-cart-product-price\">" + (quantity*price).toString() + " zł</div>"
                                + "<div class=\"menu-cart-product-change-quantity\">"
                                    + "<a onclick='setItemUserCart(" + productid + ", 1).catch(() => {})'>+</a>"
                                    + "<a onclick='setItemUserCart(" + productid + ", -1).catch(() => {})'>-</a>"
                                + "</div>"
                            + "</div>"
                        + "</div>";
        });
    if (innerHtml.length>0)
        $('#menu-cart-box').css("display", "block");
    else
        $('#menu-cart-box').css("display", "none");
    $('#menu-cart-product-quantity').html(totalPrice + parseInt(delivery_cost === undefined ? 19 : delivery_cost) + " zł");
    $('#menu-cart-content').html(innerHtml);

    if(userCartItemsCount !== userCartM.cart_items.length)
    {
        if($('#menu-category-box').css("display") != "none") {
            if(userCartItemsCount > userCartM.cart_items.length) {
                while (checkMenuCategoryHeight(true, "category")) ;
                while (checkMenuCategoryHeight(true, "cart")) ;
            } else {
                while (checkMenuCategoryHeight(false, "category")) ;
                while (checkMenuCategoryHeight(false, "cart")) ;
            }
                scrollMenuBoxes();
            }
    }
    userCartItemsCount = userCartM.cart_items.length;
}

function listUserCartMob(userCartM) {
    let innerHtml = "";
    let totalPrice = 0;
    userCartM.cart_items.map(
        (element, index, array) => {
            let name = element.product.name;
            let quantity = element.quantity;
            let price = element.product.is_promoted ? element.product.promotion_price : element.product.price;
            totalPrice += price*quantity;
            let productid = element.product.id;
            let productslug = element.product.slug;
            let itemid =  element.id;
            let imgSrc = element.product.image;
            innerHtml += "<div class=\"menu-cart-product\" id='mob-" + itemid + "'>"
                            + "<div class=\"menu-cart-product-left\" onclick=\"mobShowPopUp('"+productslug+"')\">"
                                + "<div class=\"menu-cart-product-img\" style=\"background-image: url('" + imgSrc + "')\"></div>"
                                    + "<div class=\"menu-cart-product-name\">" + quantity + " x " + name + "</div>"
                                + "</div>"
                                + "<div class=\"menu-cart-product-quantity\">"
                                + "<div class=\"menu-cart-product-price\">" + (quantity*price).toString() + " zł</div>"
                                + "<div class=\"menu-cart-product-change-quantity\">"
                                    + "<a onclick='setItemUserCart(" + productid + ", 1).catch(() => {})'>+</a>"
                                    + "<a onclick='setItemUserCart(" + productid + ", -1).catch(() => {})'>-</a>"
                                + "</div>"
                            + "</div>"
                        + "</div>";
        });
    if (innerHtml.length>0) {
        $('#mob-footer-cart-content').html(innerHtml);
        $('#mob-cart-items-count-box').css("display", "flex");
    }
    else {
        $('#mob-footer-cart-content').html("Brak produktów w koszyku");
        $('#mob-cart-items-count-box').css("display", "none");
    }
    $('#mob-menu-cart-product-quantity').html(totalPrice + parseInt(delivery_cost === undefined ? 19 : delivery_cost) + " zł");
}

function listUserCartMain(userCartM) {
    let innerHtml = "";
    let totalPrice = 0;
    userCartM.cart_items.map(
        (element, index, array) => {
            let name = element.product.name;
            let quantity = element.quantity;
            let price = element.product.is_promoted ? element.product.promotion_price : element.product.price;
            totalPrice += price*quantity;
            let productid = element.product.id;
            let productslug = element.product.slug;
            let itemid =  element.id;
            let imgSrc = element.product.image;
            innerHtml += "<div class=\"menu-cart-product\" id='" + itemid + "'>"
                            + "<div class=\"menu-cart-product-left\" onclick=\"mobShowPopUp('"+productslug+"')\">"
                                + "<div class=\"menu-cart-product-img\" style=\"background-image: url('" + imgSrc + "')\"></div>"
                                + "<div class=\"menu-cart-product-name\">" + quantity + " x " + name + "</div>"
                            + "</div>"
                            + "<div class=\"menu-cart-product-left\">"
                                + "<div class=\"menu-cart-product-quantity\">"
                                    + "<div class=\"menu-cart-product-price\">" + (quantity*price).toString() + " zł</div>"
                                    + "<div class=\"menu-cart-product-change-quantity\">"
                                        + "<a onclick='setItemUserCart(" + productid + ", 1).catch(() => {})'>+</a>"
                                        + "<a onclick='setItemUserCart(" + productid + ", -1).catch(() => {})'>-</a>"
                                    + "</div>"
                                + "</div>"
                                + "<div class=\"user-cart-product-delete\">"
                                    + "<a onclick='deleteItemUserCart(" + productid + ")'>USUŃ</a>"
                                + "</div>"
                            + "</div>"
                        + "</div>";
        });
    if(innerHtml.length>0) {
        $('#menu-cart-content-rest').css("display", "block");
        $('#menu-cart-content').html(innerHtml);
        $('#menu-cart-content').css("text-align", "right");
    }
    else {
        $('#menu-cart-content-rest').css("display", "none");
        $('#menu-cart-content').css("text-align", "left");
        $('#menu-cart-content').html("Brak produktów w koszyku. Aby dodać produkty do koszyka przejdź do strony z <a href=\"/menu/\">ofertą</a>");
    }
    $('#menu-cart-to-pay').html("Do zapłaty: " + (totalPrice + parseInt(delivery_cost === undefined ? 19 : delivery_cost)) + " zł");
}

function setItemUserCart(idItem, quantity=1) {

    return new Promise((resolve, reject) => {
        const csrftoken = getCookie('csrftoken');
        $.ajax({
            type: "PUT",
            url: "/api/menu/cart/",
            data: {
                id: idItem,
                quantity: quantity,
                csrftoken: csrftoken
            },
            headers: {"X-CSRFToken": csrftoken}
        }).then(function (data) {
            userCart = data;
            $(document).trigger("userCartLoaded", userCart);
            resolve(data);
        }).catch((error) => {
            //console.log(error);
            reject(error);
            if (error.status==401) {
                getProduct(idItem).then( data => {
                    setCookie('product_before_login',data.slug);
                    setCookie('product_bef_login_quantity', quantity);
                    window.location.href = "/logowanie/";
                }).catch(() => {
                      window.location.href = "/logowanie/";
                    }
                )
            }
        });
    })

}

function deleteItemUserCart(idItem) {
    return new Promise((resolve, reject) => {
        const csrftoken = getCookie('csrftoken');
        $.ajax({
            type: "DELETE",
            url: "/api/menu/cart/",
            data: {
                id: idItem,
                csrftoken: csrftoken
            },
            headers: {"X-CSRFToken": csrftoken}
        }).then(function (data) {
            userCart = data;
            $(document).trigger("userCartLoaded", userCart);
            resolve(data);
        }).catch((error) => {
            //console.log(error);
            reject(error);
            if (error.status==401)
                window.location.href = "/logowanie/";
        });
    })
}

function updateCartIcon(userCart) {
    let quantity = 0;
    userCart.cart_items.map(
        (element, index, array) => {
            quantity += element.quantity;
        });
    innerHtml = quantity > 99 ? "99+" : quantity.toString();
    $('#mob-cart-items-count').html(innerHtml);
}