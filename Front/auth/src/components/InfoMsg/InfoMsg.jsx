import React from 'react';
import './InfoMsg.css'; 
import { CiCircleAlert } from "react-icons/ci";
import { IoClose } from "react-icons/io5";
import { useEffect } from'react';
function InfoMsg({msg,closeInfo}) {
  useEffect(() =>{
    setTimeout(() =>closeInfo(),5000)
   },[])

  return (
    
        <div className="Info-container">
        <CiCircleAlert className="Info-icon"/>
        <div className="Info-text">{msg}</div>
        <IoClose className="Info-close" onClick={()=>{closeInfo()}} />
        </div>
 
  );
}

export default InfoMsg;
