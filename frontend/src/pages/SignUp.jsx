import React, { useState } from 'react'
import axios from 'axios';
import NavbarTwo from '../components/NavbarTwo';
import Footer from '../components/Footer';
import { useNavigate } from 'react-router-dom';
import { FaApple, FaGoogle, FaMicrosoft } from 'react-icons/fa';
import 'regenerator-runtime/runtime'

function SignUp() {
    const [message, setMessage] = useState('');
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState('');
    const navigate = useNavigate();

    const handleSignup = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/auth/register/', {
                name,
                email,
                password,
                password2,
            });

            if (response.status === 201) {
                navigate('/login')
            } else {
                setMessage(`Sign Up failed .${response.message}`)
            }
        } catch (error) {
            setMessage(`Sign Up failed .Check details and try again`)
            console.error('Signup failed', error);
        }
    };
    return (
        <div className='text-gray-300'>
            <NavbarTwo />
            <div className='max-w-7xl mx-auto py-2 px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row gap-4 items-center justify-center md:justify-between mb-4'>
                <div className="w-full md:w-1/2 flex flex-col items-center">
                    <h1 className="font-['Haskoy-ExtraBold',Helvetica] font-extrabold text-white text-2xl sm:text-3xl md:text-4xl lg:text-5xl mt-8 mb-6 text-center">
                        Create an account
                    </h1>
                    <div className="w-full max-w-xs sm:max-w-sm md:max-w-md lg:max-w-lg xl:max-w-xl">
                        <img 
                            className="w-full h-auto mt-4" 
                            alt="Mask group" 
                            src="/images/mask-group.png" 
                        />
                    </div>
                </div>
                <div className='w-full md:w-1/2 max-w-md'>
                    <form onSubmit={handleSignup}>
                        <h2 className='font-semibold text-2xl mb-4'>Sign Up</h2>
                        {message && <div><p className='mb-2'>{message}</p></div>}
                        <div className='flex flex-col sm:flex-row gap-4 mb-4'>
                            <div className="w-full sm:w-1/2">
                                <input
                                    placeholder='User Name'
                                    className="w-full px-3 py-2 mt-1 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                />
                            </div>
                            <div className="w-full sm:w-1/2">
                                <input
                                    placeholder='Email'
                                    className="w-full px-3 py-2 mt-1 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                />
                            </div>
                        </div>
                        <div className="mb-4">
                            <input
                                placeholder='Password'
                                className="w-full px-3 py-2 mt-1 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                        <div className='mb-4'>
                            <input
                                placeholder='Confirm Password'
                                className="w-full px-3 py-2 mt-1 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600"
                                type="password"
                                value={password2}
                                onChange={(e) => setPassword2(e.target.value)}
                            />
                        </div>
                        <button type="submit"
                            className='bg-blue-500 w-full sm:w-28 mb-3 text-white py-2 rounded-lg hover:bg-blue-700 transition duration-300'
                        >
                            Signup
                        </button>
                        <div className='flex flex-col sm:flex-row gap-2 sm:gap-4 justify-center items-center'>
                            <p>Already have an account?</p>
                            <a href='/login' className='text-blue-500'>
                                Log in
                            </a>
                        </div>
                    </form>

                    {/* New section for social media signup */}
                    <div className='text-center mt-8'>
                        <p className='text-2xl font-bold mb-4'>OR</p>
                        <div className='flex justify-center gap-8'>
                            <a href=''>
                                <FaGoogle className='h-10 w-10 sm:h-12 sm:w-12'/>
                            </a>
                            <a href=''>
                                <FaApple className='h-10 w-10 sm:h-12 sm:w-12'/>
                            </a>
                            <a href=''>
                                <FaMicrosoft className='h-10 w-10 sm:h-12 sm:w-12'/>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            <Footer />
        </div>
    )
}

export default SignUp



