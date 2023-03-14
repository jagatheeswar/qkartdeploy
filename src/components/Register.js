import { Button, CircularProgress, Stack, TextField, Snackbar } from "@mui/material";
import { Box } from "@mui/system";
import axios from "axios";
import { useSnackbar } from "notistack";
import React, { useState } from "react";
import { config } from "../App";
import Footer from "./Footer";
import Header from "./Header";
import "./Register.css";

const Register = () => {
  const [userName,SetuserName] = useState("");
  const [password,Setpassword] = useState("");
  const [cpassword,Setcpassword] = useState("");
  const { enqueueSnackbar, closeSnackbar } = useSnackbar()
  const [load,setload] = useState(false);

  function usernameChange(e){
    SetuserName(e.target.value);
    // console.log(userName);
  }

  function passwordChange(e){
    Setpassword(e.target.value);
    // console.log(password);
  }
  function cpasswordChange(e){
    Setcpassword(e.target.value);
    // console.log(cpassword);
  }
 
  console.log(config.endpoint+"/auth/register");



  // TODO: CRIO_TASK_MODULE_REGISTER - Implement the register function
  /**
   * Definition for register handler
   * - Function to be called when the user clicks on the register button or submits the register form
   *
   * @param {{ username: string, password: string, confirmPassword: string }} formData
   *  Object with values of username, password and confirm password user entered to register
   *
   * API endpoint - "POST /auth/register"
   *
   * Example for successful response from backend for the API call:
   * HTTP 201
   * {
   *      "success": true,
   * }
   *
   * Example for failed response from backend for the API call:
   * HTTP 400
   * {
   *      "success": false,
   *      "message": "Username is already taken"
   * }
   */
   const register = async (formData) => {

   if(validateInput({
    "username":userName,
    "password": password,
    "confirmPassword": cpassword
   }))

   {
    setload(true);
    console.log("came inside if validate input")
    axios.post(`${config.endpoint}/auth/register`, 
    {
      "username": userName,"password": password
  }
    ).then(
       (res)=> {
        console.log("response");
        console.log(res)
        enqueueSnackbar('success') 
        setload(false)       
    }
    ).catch(
       (error)=> 
    {
     if(error.response.status === 400)
     enqueueSnackbar("Username is already taken")
     if(error.response.status === 404)
     enqueueSnackbar("backend error")
     setload(false);
    }
    );
   }
  };

  // TODO: CRIO_TASK_MODULE_REGISTER - Implement user input validation logic
  /**
   * Validate the input values so that any bad or illegal values are not passed to the backend.
   *
   * @param {{ username: string, password: string, confirmPassword: string }} data
   *  Object with values of username, password and confirm password user entered to register
   *
   * @returns {boolean}
   *    Whether validation has passed or not
   *
   * Return false if any validation condition fails, otherwise return true.
   * (NOTE: The error messages to be shown for each of these cases, are given with them)
   * -    Check that username field is not an empty value - "Username is a required field"
   * -    Check that username field is not less than 6 characters in length - "Username must be at least 6 characters"
   * -    Check that password field is not an empty value - "Password is a required field"
   * -    Check that password field is not less than 6 characters in length - "Password must be at least 6 characters"
   * -    Check that confirmPassword field has the same value as password field - Passwords do not match
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
 
    if(data.password !== data.confirmPassword)
    {
      enqueueSnackbar("passwords do not match");
    }
    console.log(data.confirmPassword ===data.password);
    console.log(data.username.length>=6);
    console.log(data.password.length >= 6);

    if(data.confirmPassword===data.password && data.username.length>=6 && data.password.length >= 6)
    {
      console.log("returns true")
      return true;
    }
    return false;
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
          <h2 className="title">Register</h2>
          <TextField
          onChange={usernameChange}
            id="username"
            label="Username"
            variant="outlined"
            title="Username"
            name="username"
            placeholder="Enter Username"
            fullWidth
          />
           {/* <Button onClick={() => enqueueSnackbar('I love hooks')}>
      Show snackbar
    </Button> */}
    {/* <button onClick={() => enqueueSnackbar('That was easy!')}>Show snackbar</button> */}

          <TextField
          onChange={passwordChange}
            id="password"
            variant="outlined"
            label="Password"
            name="password"
            type="password"
            helperText="Password must be atleast 6 characters length"
            fullWidth
            placeholder="Enter a password with minimum 6 characters"
          />
          <TextField
            onChange={cpasswordChange}
            id="confirmPassword"
            variant="outlined"
            label="Confirm Password"
            name="confirmPassword"
            type="password"
            fullWidth
          />
           { load ? (
            <div id = "circular">
            <CircularProgress />
            </div>
           ):
           (
            <Button onClick={register} type="submit" className="button" variant="contained">
            Register Now
           </Button>
           )

           }
          <p className="secondary-action">
            Already have an account?{" "}
             <a className="link" href="#">
              Login here
             </a>
          </p>
        </Stack>
      </Box>
      <Footer />
    </Box>
  );
};

export default Register;
