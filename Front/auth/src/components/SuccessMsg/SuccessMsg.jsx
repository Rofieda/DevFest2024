import React from 'react';
import './SuccessMsg.css'; 
import { CiCircleCheck } from "react-icons/ci";
import { IoClose } from "react-icons/io5";
import { useEffect } from'react';

function SuccessMsg({msg,closeSuccess}) {
  useEffect(() =>{
    setTimeout(() =>closeSuccess(),5000)
   },[])
  return (
        <div className="success-container">
        <CiCircleCheck  className="success-icon"/>
        <div className="success-text">{msg}</div>
        <IoClose className="success-close" onClick={()=>{closeSuccess()}} />
        </div>
  );
}

export default SuccessMsg;
