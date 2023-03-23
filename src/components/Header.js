import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { Avatar, Button, Stack,TextField,InputAdornment } from "@mui/material";
import Box from "@mui/material/Box";
import React, { useState, useEffect } from 'react';
import "./Header.css";
import { useHistory, Link } from "react-router-dom";
import { Search, SentimentDissatisfied } from "@mui/icons-material";



const Header = ({children,hasHiddenAuthButtons,setsearchtext,performSearch,setsearchview,debounceSearch,clock}) => {
  let history = useHistory(); //add this line
  const [loggedin,setloggedin] = useState(false);
  const [username,setusername] = useState("");

  
  function searchtexthandle(e){
    // console.log(e.target.value);
    setsearchtext(e.target.value);
    //performSearch(e.target.value);
    debounceSearch(e.target.value,clock);
    setsearchview(true)

  }

  useEffect(() => {
    // Update the document title using the browser API\

    if(localStorage.getItem('username') !== null)
    {
      setloggedin(true);
      // history.push("/");
      setusername(localStorage.getItem('username'));
    }
  },[]);

  //   console.log(hasHiddenAuthButtons)
  // console.log(children);

  function backtoexporebutton(){
    history.push('/');

  }

  function logoutfunc(){
    // console.log("inside logout function");
    localStorage.clear();
    history.push('/');
    window.location.reload();
  }

  function login(){
    history.push("/login")
  }

  function register(){
    console.log("clicked register button")
    history.push("/register")
  }

    return (
      <Box className="header">
        <Box className="header-title">
            <img src="logo_light.svg" alt="QKart-icon"></img>
        </Box>

       { children && 
        <Box style={{width:"390px"}}>
        <TextField
        onChange= {searchtexthandle}
        className="search-desktop"
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
        </Box>
       } 
        
        { hasHiddenAuthButtons ? (
           <Button
          className="explore-button"
          startIcon={<ArrowBackIcon />}
          variant="text"
          onClick={backtoexporebutton}
        >
          Back to explore
        </Button>
        ):
        (
          
            loggedin ? (
                 <Stack direction="row" spacing={3}>
          <p > <Avatar alt="crio.do" src="avatar.png" /></p>
          <p className="crio.do" id="usernameid">{username}</p>

          <Button variant="text" className="register-button" onClick={logoutfunc}>Logout</Button>
        </Stack>  
        
            ) :
            (
              <Stack direction="row" spacing={3}>
              <Button variant="text" className="register-button" onClick={login}>Login</Button>
              <Button variant="contained" className="register-button" onClick={register}>Register</Button>
            </Stack>  
            )
          

        //   <Stack direction="row" spacing={3}>
        //   <p >Login</p>
        //   <Button variant="contained" className="register-button">Register</Button>
        // </Stack>       
        
        )

        }
       
       
      </Box>
    );
};

export default Header;
