import { useState,useContext } from 'react';
import axios from 'axios'; // Import axios
import loginPic from '../../assets/Login.svg';
import ErrorMsg from "../../components/ErrorMsg/ErrorMsg.jsx";
import SuccessMsg from "../../components/SuccessMsg/SuccessMsg.jsx";
import './Login.css';
import { authContext } from '../../context/Authcontext.jsx';

function Login() {
  const{
    usernameG, setUsernameG,
    role, setRole,
    entresprise, setEntresprise
  }= useContext(authContext);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic validation
    if (!username || !password) {
      setError('Both fields are required');
      return;
    }

    setError(null);

    // POST request for login authentication using axios
    try {
      const response = await axios.post('http://localhost:8000/api/login/', {
        username,
        password,
      });

      console.log('Login successful:', response.data);
      setSuccess(response.data.detail);
      // Handle successful login, e.g., store token or navigate to dashboard
      setUsernameG(response.data.user.username);
      setRole(response.data.role||null);
      setEntresprise(response.data.entreprise);
    } catch (err) {
      // Handle error (either network or server response errors)
      if (err.response) {
        // Server responded with a status other than 2xx
        setError(err.response.data.message || 'Login failed');
      } else {
        // Something went wrong with the request itself
        setError('An error occurred while logging in');
      }
    }
  };

  return (
    <div className="login-container">
      <div className="form-container">
        <h3>Welcome Back!</h3>
        <form onSubmit={handleSubmit}>
          <div className="input-grp">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="input-grp">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          {error && <p className="error-msg">{error}</p>}
          <button className="btn" type="submit">Login</button>
        </form>

        <div className="signup-link">
          Don't have an account? <a href="/signup">Sign Up</a>
        </div>
        {error && <ErrorMsg msg={error} closeError={() => setError(null)} />}
        {success && <SuccessMsg msg={success} closeSuccess={() => setSuccess(null)} />}
      </div>

      <div className="img-container">
        <img className="img" src={loginPic} alt="Login" />
      </div>
    </div>
  );
}

export default Login;
