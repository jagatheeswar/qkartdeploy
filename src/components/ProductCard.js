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

const ProductCard = ({ product, handleAddToCart }) => {
 // console.log("inside product cards page")
  //console.log(product)
  return (
    <Card className="card">
      <CardMedia
      component="img"
      alt="green iguana"
        height="140"
        image={product.image}
      />
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
         {product.name}
        </Typography>
        <Typography gutterBottom variant="h3" component="div">
          ${product.cost}
        </Typography>
        
<Typography variant="body2" color="text.secondary">
<Rating name="read-only" value={product.rating}  readOnly size="large" />
</Typography>

      </CardContent>


      <CardActions>
      <Button variant="contained" className="card-button"> ADD TO CART</Button>

      </CardActions>
    </Card>
  );
};

export default ProductCard;
