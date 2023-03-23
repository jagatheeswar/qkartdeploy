import { AddShoppingCartOutlined } from "@mui/icons-material";
import {
  Button,
  Card,
  CardActions,
  CardContent,
  CardMedia,
  Rating,
  Typography,
} from "@mui/material";
import React from "react";
import "./ProductCard.css";

const ProductCard = ({ product, handleAddToCart,cartitem }) => {
 // console.log("inside product cards page")
  //console.log(product)
  function handleclick(e){
    // console.log("came in side handle click");
    handleAddToCart(localStorage.getItem('token'),cartitem,product,e.target.value,1,true);
  }
  return (
    <Card className="card">
      <CardMedia
      component="img"
      alt="green iguana"
        image={product.image}
      />
      <CardContent>
        <Typography gutterBottom variant="h6" component="div">
         {product.name}
        </Typography>
        <Typography gutterBottom variant="body1" component="div">
          ${product.cost}
        </Typography>
        

<Rating name="read-only" value={product.rating}  readOnly size="large" />


      </CardContent>


      <CardActions>
      <Button variant="contained" value={product._id} className="card-button" onClick={handleclick} > add to cart</Button>

      </CardActions>
    </Card>
  );
};

export default ProductCard;
