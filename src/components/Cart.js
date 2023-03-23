import {
  AddOutlined,
  RemoveOutlined,
  ShoppingCart,
  ShoppingCartOutlined,
} from "@mui/icons-material";
import { Button, IconButton, Stack } from "@mui/material";
import { Box } from "@mui/system";
import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import "./Cart.css";

// Definition of Data Structures used
/**
 * @typedef {Object} Product - Data on product available to buy
 * 
 * @property {string} name - The name or title of the product
 * @property {string} category - The category that the product belongs to
 * @property {number} cost - The price to buy the product
 * @property {number} rating - The aggregate rating of the product (integer out of five)
 * @property {string} image - Contains URL for the product image
 * @property {string} _id - Unique ID for the product
 */

/**
 * @typedef {Object} CartItem -  - Data on product added to cart
 * 
 * @property {string} name - The name or title of the product in cart
 * @property {string} qty - The quantity of product added to cart
 * @property {string} category - The category that the product belongs to
 * @property {number} cost - The price to buy the product
 * @property {number} rating - The aggregate rating of the product (integer out of five)
 * @property {string} image - Contains URL for the product image
 * @property {string} productId - Unique ID for the product
 */

/**
 * Returns the complete data on all products in cartData by searching in productsData
 *
 * @param { Array.<{ productId: String, qty: Number }> } cartData
 *    Array of objects with productId and quantity of products in cart
 * 
 * @param { Array.<Product> } productsData
 *    Array of objects with complete data on all available products
 *
 * @returns { Array.<CartItem> }
 *    Array of objects with complete data on products in cart
 *
 */

var comarr = [];
export const generateCartItemsFrom = (cartData, productsData) => {
  //console.log(productsData);
  //console.log(cartData);
   comarr = [];
  for(var i = 0;i<cartData.length;i++)
  {
    for(var j = 0;j<productsData.length;j++)
    {
      if(cartData[i].productId=== productsData[j]._id)
      {
        productsData[j].qty = cartData[i].qty;
        comarr.push(productsData[j]);
      }
    }
  }
  //console.log(comarr);
  getTotalCartValue(comarr)
  return comarr;
};

/**
 * Get the total value of all products added to the cart
 *
 * @param { Array.<CartItem> } items
 *    Array of objects with complete data on products added to the cart
 *
 * @returns { Number }
 *    Value of all items in the cart
 *
 */
export const getTotalCartValue = (items = []) => {
  //console.log("getotalcartvalue");
  var sum = 0;
  //console.log(items);
  items.map((item,index)=>{
    var costperitem = item.qty * item.cost;
    sum = sum +costperitem;
  })
  //console.log(sum);
  return sum;
};


/**
 * Component to display the current quantity for a product and + and - buttons to update product quantity on cart
 * 
 * @param {Number} value
 *    Current quantity of product in cart
 * 
 * @param {Function} handleAdd
 *    Handler function which adds 1 more of a product to cart
 * 
 * @param {Function} handleDelete
 *    Handler function which reduces the quantity of a product in cart by 1
 * 
 * @param {Boolean} isReadOnly
 *    If product quantity on cart is to be displayed as read only without the + - options to change quantity
 * 
 */
const ItemQuantity = ({
  value,
  handleAdd,
  handleDelete,
  isReadOnly
}) => {
  
  return (
    <Stack direction="row" alignItems="center">
      {
        !isReadOnly && (
          <IconButton size="small" color="primary" onClick={handleDelete}>
        <RemoveOutlined />
      </IconButton>
        )
      }
      
      <Box padding="0.1rem" data-testid="item-qty">
       {isReadOnly && <span>qty:</span>}{value}
      </Box>  
      {
        !isReadOnly && (
      <IconButton size="small" color="primary" onClick={handleAdd}>
        <AddOutlined />
      </IconButton>
      )
    }
    </Stack>
  );
};

/**
 * Component to display the Cart view
 * 
 * @param { Array.<Product> } products
 *    Array of objects with complete data of all available products
 * 
 * @param { Array.<Product> } items
 *    Array of objects with complete data on products in cart
 * 
 * @param {Function} handleDelete
 *    Current quantity of product in cart
 * 
 * @param {Boolean} isReadOnly
 *    If product quantity on cart is to be displayed as read only without the + - options to change quantity
 * 
 */
const Cart = ({
  products,
  items,
  handleQuantity,
  isReadOnly
}) => {
  const [loggedin,setloggedin] = useState(false);
  const [user_token,setusertoken] = useState("");

  useEffect( async() => {
    if(localStorage.getItem('username') !== null)
    {
      setloggedin(true);
      setusertoken(localStorage.getItem('token'));
    }
  },[])

  //console.log("came inside cart")
  let history = useHistory(); //add this line
  
  function checkoutclick(e)
  {
    history.push("/checkout");
  }
  
  if (!items.length) {
    //console.log("inside if")
    return (
      <Box className="cart empty">
        <ShoppingCartOutlined className="empty-cart-icon" />
        <Box color="#aaa" textAlign="center">
          Cart is empty. Add more items to the cart to checkout.
        </Box>
      </Box>
    );
  }

  return (
    <>
    
      <Box className="cart">
        {/* TODO: CRIO_TASK_MODULE_CART - Display view for each cart item with non-zero quantity */}
        {items.map((product, index) => {
	    return (  
    <Box display="flex" alignItems="flex-start" padding="1rem">
    <Box className="image-container">
        <img
            // Add product image
            src={product.image}
            // Add product name as alt eext
            alt={product.name}
            width="100%"
            height="100%"
        />
    </Box>
    <Box
        display="flex"
        flexDirection="column"
        justifyContent="space-between"
        height="6rem"
        paddingX="1rem"
    >
        <div>{product.name}</div>
        <Box
            display="flex"
            justifyContent="space-between"
            alignItems="center"
        >
        <ItemQuantity isReadOnly={isReadOnly} value={product.qty} handleAdd =

 {

 async()=>{

 let new_val=product.qty+1

 handleQuantity(user_token,{"productId":product._id,"qty":new_val},products,new_val,false)

 }

 }

 handleDelete=

 {

 async()=>{

 let new_val=product.qty-1

 handleQuantity(user_token,{"productId":product._id,"qty":new_val},products,new_val,false)

 }

 }

 // Add required props by checking implementation

 />
        <Box padding="0.5rem" fontWeight="700">
            ${product.cost}
        </Box>
        </Box>
    </Box>
</Box>
  );
      }
        )}
        <Box
          padding="1rem"
          display="flex"
          justifyContent="space-between"
          alignItems="center"
        >
          <Box color="#3C3C3C" alignSelf="center">
            Order total
          </Box>
          <Box
            color="#3C3C3C"
            fontWeight="700"
            fontSize="1.5rem"
            alignSelf="center"
            data-testid="cart-total"
          >
            ${getTotalCartValue(items)}
          </Box>
        </Box>

        <Box display="flex" justifyContent="flex-end" className="cart-footer">
          {!isReadOnly && 
          <Button
          color="primary"
          variant="contained"
          startIcon={<ShoppingCart />}
          className="checkout-btn"
          onClick={checkoutclick}
        >
          Checkout
        </Button>
          }
        </Box>
      </Box>
      { isReadOnly &&
      <Box className="cart">
        <h1>Order details</h1>
        <Box
          padding="1rem"
          display="flex"
          justifyContent="space-between"
          alignItems="center"
        >
          <Box color="#3C3C3C" alignSelf="center">
            Products
          </Box>
          <Box
            color="#3C3C3C"
            fontWeight="700"
            fontSize="1.5rem"
            alignSelf="center"
            data-testid="cart-total"
          >
                        {items.length}
          </Box>
        </Box>

        <Box
          padding="1rem"
          display="flex"
          justifyContent="space-between"
          alignItems="center"
        >
          <Box color="#3C3C3C" alignSelf="center">
            Subtotal
          </Box>
          <Box
            color="#3C3C3C"
            fontWeight="700"
            fontSize="1.5rem"
            alignSelf="center"
            data-testid="cart-total"
          >
            ${getTotalCartValue(items)}
          </Box>
        </Box>


        <Box
          padding="1rem"
          display="flex"
          justifyContent="space-between"
          alignItems="center"
        >
          <Box color="#3C3C3C" alignSelf="center">
            Shipping Charges
          </Box>
          <Box
            color="#3C3C3C"
            fontWeight="700"
            fontSize="1.5rem"
            alignSelf="center"
            data-testid="cart-total"
          >
            $0
          </Box>
        </Box>


        <Box
          padding="1rem"
          display="flex"
          justifyContent="space-between"
          alignItems="center"
        >
          <Box color="#3C3C3C" alignSelf="center">
            Total
          </Box>
          <Box
            color="#3C3C3C"
            fontWeight="700"
            fontSize="1.5rem"
            alignSelf="center"
            data-testid="cart-total"
          >
            ${getTotalCartValue(items)}
          </Box>
        </Box>


      </Box>

      }
    </>
  );
};

export default Cart;
