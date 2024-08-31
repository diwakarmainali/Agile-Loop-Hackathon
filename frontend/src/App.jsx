import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import LandingPage from './pages/Landing';
import Login from './pages/Login';
import SignUp from './pages/SignUp';
import Home from './pages/Home';
import Orders from './pages/Orders';
import Notifications from './pages/Notifications';
import Leaderboard from './pages/leaderboard';
import SpeechToText from './pages/SpeechToText';

function App() {
  return (
    <Router>
      <div className='h-full bg-[#0d0d0d] md:text-md text-sm '>
        <Routes>
          <Route path='/' element={<LandingPage />} />
          <Route path='/login' element={<Login />} />
          <Route path='/signup' element={<SignUp />} />
          <Route path='/dashboard' element={<Home />} />
          <Route path='/my-orders' element={<Orders />} />
          <Route path='/notifications' element={<Notifications/>} />
          <Route path='/leaderboard' element={<Leaderboard/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
