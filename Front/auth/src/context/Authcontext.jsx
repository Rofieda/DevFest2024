import { createContext,useEffect,useState } from "react";

export const authContext= createContext(null);

const AuthContextProvider=({children})=>{
    const [usernameG, setUsernameG]=useState(()=>{
        const username = localStorage.getItem('username')
        return username ? JSON.parse(username): null
    })
    const [role, setRole]=useState(()=>{
        const username = localStorage.getItem('role')
        return username ? JSON.parse(username): null
    })
    const[entresprise, setEntresprise]=useState(()=>{
        const username = localStorage.getItem('entreprise')
        return username ? JSON.parse(username): null
    });


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