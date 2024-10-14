import react from 'react'
import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom"
import Login from './pages/Login'
import Register from './pages/Register'
import Home from './pages/Home'
import NotFound from './pages/NotFound'
import ProtectedRoute from './components/ProtectedRoute'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Sidebar from './components/Sidebar';
function Logout(){
  localStorage.clear()
  return <Navigate to="/login" />
}

function RegisterAndLogout(){
  localStorage.clear()
  return <Register />
}

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Sidebar />
      <Routes>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Home/>
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={<Login />}/>
        <Route path="/logout" element={<Logout />}/>
        <Route path="/register" element={<RegisterAndLogout />}/>
        <Route path="*" element={<NotFound />}></Route>
      </Routes>
      <Footer />
    </BrowserRouter>
    
  )
}

export default App