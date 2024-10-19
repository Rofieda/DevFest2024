import { createContext,useEffect,useState } from "react";

export const authContext= createContext(null);

const AuthContextProvider=({children})=>{
    const [usernameG, setUsernameG]=useState(JSON.parse((localStorage.getItem('username'))));
    const [role, setRole]=useState(JSON.parse((localStorage.getItem('role'))))
    const[entresprise, setEntresprise]=useState(JSON.parse(localStorage.getItem('entreprise')));


    useEffect(()=>{
        localStorage.setItem('username', JSON.stringify(usernameG))
        localStorage.setItem('role', JSON.stringify(role))
        localStorage.setItem('entreprise', JSON.stringify(entresprise))
    },[usernameG,role,entresprise])
    

    return(
        <authContext.Provider value={{
            usernameG, setUsernameG,
            role, setRole,
            entresprise, setEntresprise
            }}>
            {children}
        </authContext.Provider>
    )
}

export default AuthContextProvider;