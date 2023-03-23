import { Search, SentimentDissatisfied } from "@mui/icons-material";
import {
  CircularProgress,
  Grid,
  InputAdornment,
  TextField,
} from "@mui/material";
import { Box } from "@mui/system";
import axios from "axios";
import { useSnackbar } from "notistack";
import React, { useEffect, useState } from "react";
import { config } from "../App";
import Footer from "./Footer";
import Header from "./Header";
import "./Products.css";
import ProductCard from "./ProductCard"
import Cart from "./Cart";
import { useHistory, Link } from "react-router-dom";
import {generateCartItemsFrom} from "./Cart.js"
 


/**
 * @typedef {Object} CartItem -  - Data on product added to cart
 * 
 * @property {string} name - The name or title of the product in cart
 * @property {string} qty - The quantity of product added to cart
 * @property {string} category - The category that the product belongs to
 * @property {number} cost - The price to buy the product
 * @property {number} rating - The aggregate rating of the product (integer out of five)
 * @property {string} image - Contains URL for the product image
 * @property {string} _id - Unique ID for the product
 */


const Products = () => {
  let history = useHistory(); //add this line

  const { enqueueSnackbar } = useSnackbar();
  const [products,setproducts] = useState([]);
  const [searchproducts,setsearchproducts] = useState([]);
  const [searchview,setsearchview] = useState(false);

  const [loading,setloading] = useState(true);
  const [fetcherror,setfetcherror] = useState(false);
  const [searchtext,setsearchtext] = useState("");
  const [clock,setclock] = useState("");
  const [loggedin,setloggedin] = useState(false);
  const [width,setwidth] = useState(12);
  const [comarr,setcomarr] = useState([]);
  const [cartitem,setcartitem] = useState([]);
  const [addnewitem,setaddnewitem] = useState(false);
  const [searchmobile,setsearchmobile] = useState("");


 
  // TODO: CRIO_TASK_MODULE_PRODUCTS - Fetch products data and store it
  /**
   * Make API call to get the products list and store it to display the products
   *
   * @returns { Array.<Product> }
   *      Array of objects with complete data on all available products
   *
   * API endpoint - "GET /products"
   *
   * Example for successful response from backend:
   * HTTP 200
   * [
   *      {
   *          "name": "iPhone XR",
   *          "category": "Phones",
   *          "cost": 100,
   *          "rating": 4,
   *          "image": "https://i.imgur.com/lulqWzW.jpg",
   *          "_id": "v4sLtEcMpzabRyfx"
   *      },
   *      {
   *          "name": "Basketball",
   *          "category": "Sports",
   *          "cost": 100,
   *          "rating": 5,
   *          "image": "https://i.imgur.com/lulqWzW.jpg",
   *          "_id": "upLK9JbQ4rMhTwt4"
   *      }
   * ]
   *
   * Example for failed response from backend:
   * HTTP 500
   * {
   *      "success": false,
   *      "message": "Something went wrong. Check the backend console for more details"
   * }
   */
  const performAPICall = async () => {
    
    let productarr = [];
    let status = "";
    try{
      status =  await axios
     .get(`${config.endpoint}/products`)
     setfetcherror(false);
     setproducts(status.data);
     setloading(false);
       // console.log("status await")
       // console.log(status);
       // console.log(status.data);
       return status.data;
     }
     catch(e){
       setloading(false);
       // console.log("await error");
       // console.log(e);
       setfetcherror(true);
 
     }
    };

    useEffect( async() => {
      const prorudctsarr = await performAPICall();
      if(localStorage.getItem('username') !== null)
      {
        setloggedin(true);
        history.push("/");
        setwidth(9);
        let retval = await fetchCart(localStorage.getItem('token'));
        setcartitem(retval);
        setcomarr(generateCartItemsFrom(cartitem,products));
      }
    },[addnewitem])

    useEffect( async() => {
      if(localStorage.getItem('username') !== null)
       setcomarr(generateCartItemsFrom(cartitem,products));

   },[cartitem])
 


  // TODO: CRIO_TASK_MODULE_PRODUCTS - Implement search logic
  /**
   * Definition for search handler
   * This is the function that is called on adding new search keys
   *
   * @param {string} text
   *    Text user types in the search bar. To filter the displayed products based on this text.
   *
   * @returns { Array.<Product> }
   *      Array of objects with complete data on filtered set of products
   *
   * API endpoint - "GET /products/search?value=<search-query>"
   *
   */
  const performSearch = async (text) => {
    axios
    .get(`${config.endpoint}/products/search?value=${text}`)
    .then((data) => {
      //console.log(data.data.message);
      setfetcherror(false);
      //console.log("inside then of perform search api calls" + text);
      setsearchproducts(data.data);
      setloading(false);
      // console.log("search array");
      // console.log(products );
    })
    .catch((e) => {
      setloading(false)
      setfetcherror(true);
      // console.log("inside error of perform search api calls")
      // console.log(text);
      // console.log("error");
      
    });

  };

  // TODO: CRIO_TASK_MODULE_PRODUCTS - Optimise API calls with debounce search implementation
  /**
   * Definition for debounce handler
   * With debounce, this is the function to be called whenever the user types text in the searchbar field
   *
   * @param {{ target: { value: string } }} event
   *    JS event object emitted from the search input field
   *
   * @param {NodeJS.Timeout} debounceTimeout
   *    Timer id set for the previous debounce call
   *
   */
  const debounceSearch = (event, debounceTimeout) => {
    clearTimeout(debounceTimeout);
    var clock = setTimeout(()=>performSearch(event),500);
    setclock(clock);

  };

  


  /**
   * Perform the API call to fetch the user's cart and return the response
   *
   * @param {string} token - Authentication token returned on login
   *
   * @returns { Array.<{ productId: string, qty: number }> | null }
   *    The response JSON object
   *
   * Example for successful response from backend:
   * HTTP 200
   * [
   *      {
   *          "productId": "KCRwjF7lN97HnEaY",
   *          "qty": 3
   *      },
   *      {
   *          "productId": "BW0jAAeDJmlZCF8i",
   *          "qty": 1
   *      }
   * ]
   *
   * Example for failed response from backend:
   * HTTP 401
   * {
   *      "success": false,
   *      "message": "Protected route, Oauth2 Bearer token not found"
   * }
   */

  
  const fetchCart = async (token) => {
    if (!token) return;
    try {
      // TODO: CRIO_TASK_MODULE_CART - Pass Bearer token inside "Authorization" header to get data from "GET /cart" API and return the response data
     
       let x = await axios.get(`${config.endpoint}/cart` , {
        headers: {
          'Authorization': `Bearer ${token}` 
        }
      });
      // console.log("printing x");
      // console.log(x.data);
      return x.data;
    } 
    catch (e) {
      if (e.response && e.response.status === 400) {
        enqueueSnackbar(e.response.data.message, { variant: "error" });
      } else {
        enqueueSnackbar(
          "Could not fetch cart details. Check that the backend is running, reachable and returns valid JSON.",
          {
            variant: "error",
          }
        );
      }
      return null;
    }
   
  };


  // TODO: CRIO_TASK_MODULE_CART - Return if a product already exists in the cart
  /**
   * Return if a product already is present in the cart
   *
   * @param { Array.<{ productId: String, quantity: Number }> } items
   *    Array of objects with productId and quantity of products in cart
   * @param { String } productId
   *    Id of a product to be checked
   *
   * @returns { Boolean }
   *    Whether a product of given "productId" exists in the "items" array
   *
   */
  const isItemInCart = (items, productId) => {
    // console.log("inside isitem in cart");
    // console.log(items);
    // items.forEach((x)=>{
    //   console.log(x.productId +"  from x" );
    //   console.log(productId +"  from idd" );
    //   if(x.productId === productId)
    //   {
    //     console.log("cameeeeeeeeeeeee in")
    //     return true;
    //   }
    // }
    // );
    for(var i =0;i<items.length;i++)
    {
      if(items[i].productId===productId)
      return true;
    }
  };

  /**
   * Perform the API call to add or update items in the user's cart and update local cart data to display the latest cart
   *
   * @param {string} token
   *    Authentication token returned on login
   * @param { Array.<{ productId: String, quantity: Number }> } items
   *    Array of objects with productId and quantity of products in cart
   * @param { Array.<Product> } products
   *    Array of objects with complete data on all available products
   * @param {string} productId
   *    ID of the product that is to be added or updated in cart
   * @param {number} qty
   *    How many of the product should be in the cart
   * @param {boolean} options
   *    If this function was triggered from the product card's "Add to Cart" button
   *
   * Example for successful response from backend:
   * HTTP 200 - Updated list of cart items
   * [
   *      {
   *          "productId": "KCRwjF7lN97HnEaY",
   *          "qty": 3
   *      },
   *      {
   *          "productId": "BW0jAAeDJmlZCF8i",
   *          "qty": 1
   *      }
   * ]
   *
   * Example for failed response from backend:
   * HTTP 404 - On invalid productId
   * {
   *      "success": false,
   *      "message": "Product doesn't exist"
   * }
   */
  const addToCart = async (
    token,
    items,
    product,
    productId,
    qty,
    options
  ) => {
    console.log("came inside add to cart");
    console.log(token);
    if(token)
    {
      // console.log("heree")
      // console.log(options);
      if(options)
      {
    if(isItemInCart(items,productId))
    {
      enqueueSnackbar("ITEM alreaDy in carT",{ variant: 'warning',autoHideDuration:3000 });
      return;
    }
      else{
      // console.log("add to cart function" + token);
      // console.log(productId);
      
      //   console.log("printing all essential values");
      //   console.log(productId );
      //   console.log(qty);
         let res = await axios.post(`${config.endpoint}/cart` , {
        'productId':`${productId}`,
        'qty': qty
      }, {
        headers: {
          'Authorization': `Bearer ${token}` 
        }
      });
    setcartitem(res.data);
      // setaddnewitem(!addnewitem);
    }
  }
  else{
        // console.log("pressed pluse or minus")
         let res = await axios.post(`${config.endpoint}/cart` , items, {
        headers: {
          'Authorization': `Bearer ${token}` 
        }
      });
    setcartitem(res.data);
      // setaddnewitem(!addnewitem);
  }
  }
  else{
    enqueueSnackbar("Please login to add to cart",{ variant: 'warning',autoHideDuration:3000 });
      return;
  }
  };


  return (
    <div>
      <Header
      children={true}
      setsearchtext={ setsearchtext}
      performSearch={performSearch}
      setsearchview={setsearchview}
      debounceSearch = {debounceSearch}
      clock={clock}
      >
        {/* TODO: CRIO_TASK_MODULE_PRODUCTS - Display search bar in the header for Products page */}
        
        </Header>
      <TextField
      onChange= {(e)=>{
        setsearchmobile(e.target.value)
        debounceSearch(e.target.value,clock);
        setsearchview(true);
      }}
        className="search-mobile"
        size="small"
        fullWidth
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <Search color="primary" />
            </InputAdornment>
          ),
        }}
        placeholder="Search for items/categories"
        name="search"
      />
      <Grid container spacing={0}>
      <Grid container xs={12}  md={width} spacing={2}>
         <Grid item className="product-grid">
           <Box className="hero">
             <p className="hero-heading">

               India’s <span className="hero-highlight">FASTEST DELIVERY</span>{" "}
               to your door step 
             </p>
             
           </Box>
         </Grid>
        
         {
          loading
           ? (
            <Grid container spacing={2}>
          <Grid item xs={12} md={12}>
          <div className="loading">
            <CircularProgress />
            <p>Loading Products...</p>
          </div>            
          </Grid>
</Grid>
          
          ) : (
            fetcherror ? ( 
            <Grid container spacing={2}>
              <Grid item xs={12} md={12}>
              <div className="loading">
              <h1>
                no products found
            </h1>
              </div>            
              </Grid>
    </Grid>
    ) : (
      searchview ? searchproducts.map((product, index) => {
	return (  
      <Grid item xs={6} md={3} spacing={2}>
      <ProductCard cartitem={cartitem} product={product} handleAddToCart={addToCart} />
      </Grid>
);
})  :(
      
      products.map((product, index) => {  
return (
      <Grid item xs={6} md={3} spacing={2}>
      <ProductCard cartitem={cartitem} product={product} handleAddToCart={addToCart} />
      </Grid>
);
} 
)
      
    )    
    ) )
          }
       </Grid>
       {loggedin ? (
        <Grid xs={12} md={3} style={{backgroundColor:"#E9F5E1"}}>
        <Cart products={products} items={comarr} handleQuantity={addToCart}/>
       </Grid>
       ):(<></>)}
       
      </Grid>
      <Footer />
    </div>
  );
};

export default Products;
