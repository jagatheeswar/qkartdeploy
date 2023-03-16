import { Button, CircularProgress, Stack, TextField } from "@mui/material";
import { Box } from "@mui/system";
import axios from "axios";
import { useSnackbar } from "notistack";
import React, { useState } from "react";
import { useHistory, Link } from "react-router-dom";
import { config } from "../App";
import Footer from "./Footer";
import Header from "./Header";
import "./Login.css";
import { Redirect } from 'react-router-dom';
import { Navigate } from "react-router-dom";


const Login = () => {
  let history = useHistory(); //add this line

  const [username,setusername] = useState("");
  const [password,setpassword] = useState("");
  const [load,setload] = useState(false);

  const { enqueueSnackbar } = useSnackbar();
  const usernamehandle = (e)=>{
    setusername(e.target.value);
  }
  const passwordhandle = (e)=>{
    setpassword(e.target.value);
  }

  // TODO: CRIO_TASK_MODULE_LOGIN - Fetch the API response
  /**
   * Perform the Login API call
   * @param {{ username: string, password: string }} formData
   *  Object with values of username, password and confirm password user entered to register
   *
   * API endpoint - "POST /auth/login"
   *
   * Example for successful response from backend:
   * HTTP 201
   * {
   *      "success": true,
   *      "token": "testtoken",
   *      "username": "criodo",
   *      "balance": 5000
   * }
   *
   * Example for failed response from backend:
   * HTTP 400
   * {
   *      "success": false,
   *      "message": "Password is incorrect"
   * }
   *
   */

  const login = async (formData) => {
    formData = {
      "username":username,
      "password":password
    };
    // console.log(formData)

    if(validateInput(formData))
     {
      setload(true);
      // console.log("came inside if validate input")
      axios.post(`${config.endpoint}/auth/login`, formData
      ).then(
         (res)=> {
          // console.log("response");
          // console.log(res)
          enqueueSnackbar('logged in') 
          persistLogin(res.data.token,res.data.username,res.data.balance);
          setload(false)   
          history.push('/');
        }
      ).catch(
         (error)=> 
      {
        // console.log(error.response)
      if(error.response.status === 400)
      enqueueSnackbar(error.response.data.message)
      if(error.response.status === 404)
      enqueueSnackbar("backend error")
      //  setload(false);
      }
      );
     }
  };

  // TODO: CRIO_TASK_MODULE_LOGIN - Validate the input
  /**
   * Validate the input values so that any bad or illegal values are not passed to the backend.
   *
   * @param {{ username: string, password: string }} data
   *  Object with values of username, password and confirm password user entered to register
   *
   * @returns {boolean}
   *    Whether validation has passed or not
   *
   * Return false and show warning message if any validation condition fails, otherwise return true.
   * (NOTE: The error messages to be shown for each of these cases, are given with them)
   * -    Check that username field is not an empty value - "Username is a required field"
   * -    Check that password field is not an empty value - "Password is a required field"
   */
  const validateInput = (data) => {
    if(data.password.length <6 && data.password !=="")
    {
     enqueueSnackbar("password length is less than 6");
    }
 
    if(data.password.length===0)
    {
     enqueueSnackbar("password is required");
    }
 
    if(data.username.length<6 && data.username !=="")
    {
     enqueueSnackbar("username length is less than 6");
    }
 
    if(data.username.length===0)
    {
     enqueueSnackbar("username is required");
    }
 
    // console.log(data.username.length>=6);
    // console.log(data.password.length >= 6);

    if(data.username.length>=6 && data.password.length >= 6)
    {
      // console.log("returns true")
      return true;
    }
    return false;
  };

  // TODO: CRIO_TASK_MODULE_LOGIN - Persist user's login information
  /**
   * Store the login information so that it can be used to identify the user in subsequent API calls
   *
   * @param {string} token
   *    API token used for authentication of requests after logging in
   * @param {string} username
   *    Username of the logged in user
   * @param {string} balance
   *    Wallet balance amount of the logged in user
   *
   * Make use of localStorage: https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage
   * -    `token` field in localStorage can be used to store the Oauth token
   * -    `username` field in localStorage can be used to store the username that the user is logged in as
   * -    `balance` field in localStorage can be used to store the balance amount in the user's wallet
   */
  const persistLogin = (token, username, balance) => {
    // console.log("inside persistlogin")
    // console.log(token);
    // console.log(username);
    // console.log(balance);
    localStorage.setItem('username', username)
    localStorage.setItem('token', token)
    localStorage.setItem('balance', balance)
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      justifyContent="space-between"
      minHeight="100vh"
    >
      <Header hasHiddenAuthButtons />
      <Box className="content">
        <Stack spacing={2} className="form">
        <h2 className="title">Login</h2>
          <TextField
          onChange={usernamehandle}
            id="username"
            label="username"
            variant="outlined"
            title="Username"
            name="username"
            placeholder="Enter Username"
            fullWidth
          />
          
          <TextField
          onChange={passwordhandle}
            id="password"
            variant="outlined"
            label="password"
            name="password"
            type="password"
            helperText="Password must be atleast 6 characters length"
            fullWidth
            placeholder="Enter a password with minimum 6 characters"
          />
          <Button onClick={login} type="submit" variant="contained">
          login to qkart
           </Button>
          <p className="secondary-action">
            Dont't have an account?{" "}
             <a className="link" href="/register">
            Register now
             </a>
          </p>
        </Stack>
      </Box>
      <Footer />
    </Box>
  );
};

export default Login;
