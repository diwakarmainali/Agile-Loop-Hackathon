import React, { useState } from 'react'
import axios from 'axios';
//import { useHistory } from 'react-router-dom';
import Cookies from 'universal-cookie';
import NavbarTwo from '../components/NavbarTwo';
import Footer from '../components/Footer';
import { useNavigate } from 'react-router-dom';
import { FaApple, FaGoogle, FaMicrosoft } from 'react-icons/fa';
import { FaApplePay } from 'react-icons/fa6';
import 'regenerator-runtime/runtime'
const cookies = new Cookies();

function Login() {
  const [message, setMessage] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  //const history = useHistory();
  const navigate = useNavigate()

  const handleLogin = async (e) => {
    e.preventDefault();
    //for rapid testing
    if (email === "devquix@gmail.com" && password === "Dev1@p@ss") {
      navigate('/dashboard');
    } else {
      try {
        const response = await axios.post(_BACKEND_URL_ + '/api/auth/login/', {
          email,
          password,
        });
        if (response.status === 200) {
          cookies.set('access_token', response.data.access, { path: '/' });
          cookies.set('refresh_token', response.data.refresh, { path: '/' });
          navigate('/dashboard');
        } else {

          setMessage(`Login failed .Check details and try again`)
        }
      } catch (error) {
        setMessage(`Login failed .Check details and try again`)
        console.error('Login failed', error);
      }

    }

  };

  return (
    <div className='text-gray-300 min-h-screen flex flex-col '>
      <NavbarTwo />
      <div className='container mx-auto px-4 py-8 flex-grow px-4 sm:px-6 lg:px-8' >
        <div className='flex flex-col lg:flex-row gap-8 items-center justify-center lg:justify-between'>
          {/* Left side - Welcome and Image */}
          <div className="w-full lg:w-1/2 flex flex-col items-center lg:items-start">
            <h1 className="font-['Haskoy-ExtraBold',Helvetica] font-extrabold text-white text-3xl sm:text-4xl lg:text-5xl mb-6 text-center lg:text-left">
              Welcome Back!
            </h1>
            <div className="w-full max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg">
              <img
                className="w-full h-auto"
                alt="Mask group"
                src="/images/mask-group.png"
              />
            </div>
          </div>

          {/* Right side - Login Form */}
          <div className='w-full lg:w-1/2 max-w-md'>
            <form onSubmit={handleLogin} className='mb-8'>
              <h2 className='mb-4 font-semibold text-2xl'>Login</h2>
              {message && (
                <div>
                  <p className='mb-2'>{message}</p>
                </div>
              )}
              <div className='mb-4'>
                <input
                  placeholder='Email'
                  className="w-full px-4 py-3 mt-1 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <div className='mb-4'>
                <input
                  placeholder='Password'
                  className="w-full px-4 py-3 mt-1 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              <button type="submit"
                className='bg-blue-500 w-full px-6 py-2 mb-3 mt-4 text-white rounded-lg hover:bg-blue-700 transition duration-300'
              >
                Login
              </button>
              <div className='flex flex-col sm:flex-row gap-2 sm:gap-4 items-center justify-center mt-6'>
                <p>Don't have an account?</p>
                <a href='/signup' className='text-blue-500'>
                  Sign Up
                </a>
              </div>
            </form>

            {/* Social Login Options */}
            <div className='text-center'>
              <p className='text-2xl font-bold mb-4'>OR</p>
              <div className='flex justify-center gap-8'>
                <a href='' className='transition-transform hover:scale-110'>
                  <FaGoogle className='h-10 w-10' />
                </a>
                <a href='' className='transition-transform hover:scale-110'>
                  <FaApple className='h-10 w-10' />
                </a>
                <a href='' className='transition-transform hover:scale-110'>
                  <FaMicrosoft className='h-10 w-10' />
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  )
}

export default Login