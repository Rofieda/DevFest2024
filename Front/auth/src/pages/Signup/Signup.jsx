import { useState,useContext } from 'react';
import signupPic from '../../assets/Signup.svg';
import ErrorMsg from "../../components/ErrorMsg/ErrorMsg.jsx";
import SuccessMsg from "../../components/SuccessMsg/SuccessMsg.jsx";
import './Signup.css';
import axios from "axios";
import { authContext } from '../../context/Authcontext.jsx';


function Signup() {
  const{
    usernameG, setUsernameG,
    role, setRole,
    entresprise, setEntresprise
  }= useContext(authContext);
  // State for the first form
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // State for the second form (company information)
  const [companyName, setCompanyName] = useState('');
  const [companyAddress, setCompanyAddress] = useState('');
  const [companyEmail, setCompanyEmail] = useState('');
  const [companyPhone, setCompanyPhone] = useState('');

  // State to show/hide second form
  const [showSecondForm, setShowSecondForm] = useState(false);

  // First form submission
  const handleSubmit1 = (e) => {
    e.preventDefault();

    // Basic validation
    if (!username || !password || !confirmPassword) {
      setError('All fields are required');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setError(null);
    setShowSecondForm(true); // Show company form
  };

  // Second form submission (company information)
  const handleSubmit2 = async (e) => {
    e.preventDefault();

    // Basic validation for the second form
    if (!companyName || !companyAddress || !companyEmail || !companyPhone) {
      setError('All fields in the company form are required');
      return;
    }

    setError(null);
    // Handle submission logic (e.g., API call)

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/signup/', {
        username,
        password,
        entreprise_name:companyName ,
        entreprise_email: companyEmail,
        entreprise_address: companyAddress,
        entreprise_phone: companyPhone
      });
  
      console.log('Company info submission successful:', response.data);
      setSuccess("Account created successfully");
      setUsernameG(response.data.user.username);
      setRole(response.data.role||null);
      setEntresprise(response.data.entreprise);
    } catch (error) {
      setError(error.response?.data?.message || 'Data submission failed, try again later');
    }
    setShowSecondForm(false);
  };

  return (
    <div className="login-container">
      <div className="form-container">
        
        {!showSecondForm ? (
          <form onSubmit={handleSubmit1}>
            <h3>Get Started</h3>
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
            <div className="input-grp">
              <label htmlFor="confirm-password">Confirm Password</label>
              <input
                type="password"
                id="confirm-password"
                placeholder="Confirm Password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
              />
            </div>
            <button className="btn" type="submit">Next</button>
          </form>
        ) : (
          <>
            <h4>Enter your company's information</h4>
            <form onSubmit={handleSubmit2}>
              <div className="input-grp">
                <label htmlFor="company-name">Company Name</label>
                <input
                  type="text"
                  id="company-name"
                  placeholder="Company Name (e.g., Meta)"
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                />
              </div>
              <div className="input-grp">
                <label htmlFor="company-address">Company Address</label>
                <input
                  type="text"
                  id="company-address"
                  placeholder="Company Address"
                  value={companyAddress}
                  onChange={(e) => setCompanyAddress(e.target.value)}
                />
              </div>
              <div className="input-grp">
                <label htmlFor="company-email">Company Email</label>
                <input
                  type="email"
                  id="company-email"
                  placeholder="Company Email"
                  value={companyEmail}
                  onChange={(e) => setCompanyEmail(e.target.value)}
                />
              </div>
              <div className="input-grp">
                <label htmlFor="company-phone">Company Phone</label>
                <input
                  type="tel"
                  id="company-phone"
                  placeholder="Company Phone"
                  value={companyPhone}
                  onChange={(e) => setCompanyPhone(e.target.value)}
                />
              </div>
              <button className="btn" type="submit">Sign up</button>
            </form>
          </>
        )}

        <div className="signup-link">
          Already have an account? <a href="/login">Log in</a>
        </div>
        {error && <ErrorMsg msg={error} closeError={() => setError(null)} />}
        {success && <SuccessMsg msg={success} closeSuccess={() => setSuccess(null)} />}
      </div>

      <div className="img-container">
        <img className="img" src={signupPic} alt="Signup" />
      </div>
    </div>
  );
}

export default Signup;
