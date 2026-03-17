import { BrowserRouter,Routes,Route } from "react-router-dom"
import AnalyzerPage from "./pages/AnalyzerPage"
import { SignUp } from "./pages/SignUp"
import { Login } from "./pages/Login"
import ProtectedRoute from "./components/ProtectedRoute"
import History from "./pages/History"
import Dashboard from "./pages/Dashboard"

const App = () => {
  return (
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<Login/>}/>
      <Route path='/login' element={<Login/>}/>
      <Route path='/signup' element={<SignUp/>}/>
      <Route 
      path='/analyzer' 
      element={
      <ProtectedRoute><AnalyzerPage/></ProtectedRoute>}
      />
      <Route 
      path='/history' 
      element={
      <ProtectedRoute><History/></ProtectedRoute>}
      />
      <Route 
      path='/dashboard' 
      element={
      <ProtectedRoute><Dashboard/></ProtectedRoute>}
      />
    </Routes>
    </BrowserRouter>
  )
}

export default App