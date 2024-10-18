var visitBar = `
<nav class="top-bar" xmlns="http://www.w3.org/1999/html">
<div class="logo-container">

   
</div>

<div class="top-bar-items">

    <div class="link_text">
        <a href="#">Landing Page</a>
        <a href="#a-propos-nous" id="propos">About us</a>
        <a href="#Contacts">Contacts</a>
    </div>


    <div class="button-two">
        
    
        <div class="dropdown2">
            <div class="filtrex">
                <div class="textBox-with-icon2">
                       
                  </div>
                  <div class="option2" style="font-size: 1vw;
                  padding-left: 3px;
                  padding-right: 3px;
                  padding-top: 3px;
                  padding-bottom: 3px;
                  position: absolute;
                  top: 140%;
                  background: white;
      
                  border: 2px solid #64379F ;
                  border-radius: 6px;
                  width: 20%;
                  margin-left: 0.3%;">
                        
                 </div>
            </div>
        </div>



         <button class="connect-button" onclick="redirectToSeConnecter()">Log in</button>


   </div>
</div>
</nav>  `



document.body.insertAdjacentHTML("afterbegin",visitBar)

function redirectToSeConnecter() {
        window.location.href = "../html/seconnecter.html";
    }
