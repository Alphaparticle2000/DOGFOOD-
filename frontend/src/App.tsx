import Homepage from './pages/Homepage';
import Login from "./pages/Login";
import Gallery from "./pages/Gallery";
import Myteam from "./pages/Myteam";
import { Routes, Route } from 'react-router-dom';

const App = () => {
  return (
    <>
    <Homepage />
    <Routes>
      <Route path='/login' element={<Login />}/>
      <Route path='/gallery' element={<Gallery />}/>
      <Route path='/myteam' element={<Myteam />}/>
    </Routes>
    </>
  )
}

export default App