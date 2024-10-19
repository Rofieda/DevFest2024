import { Link } from "react-router-dom"
import './Home.css'
function Home() {

    return (
    <div className="btn-container">
        <Link to="/login">
            <button className='btn'>
                Login
            </button>
        </Link>
        
        <Link to="/signup">
            <button className='btn'>
                Signup
            </button>
        </Link>
    </div>
    )
  }
  
  export default Home