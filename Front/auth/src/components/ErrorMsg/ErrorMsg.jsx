import React from 'react';
import './ErrorMsg.css'; 
import { FaRegCircleXmark } from "react-icons/fa6";
import { IoClose } from "react-icons/io5";
import { useEffect } from 'react';
function ErrorMsg({msg,closeError}) {
   useEffect(() =>{
    setTimeout(() =>closeError(),5000)
   },[])
  return (
        <div className="error-container">
        < FaRegCircleXmark className="error-icon"/>
        <div className="error-text">{msg}</div>
        <IoClose className="error-close" onClick={()=>{closeError()}} />
        </div>
  );
}

export default ErrorMsg;
