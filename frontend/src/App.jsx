import { BrowserRouter,Routes,Route } from "react-router-dom"
import AnalyzerPage from "./pages/AnalyzerPage"
import { SignUp } from "./pages/SignUp"
import { Login } from "./pages/Login"

const App = () => {
  return (
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<Login/>}/>
      <Route path='/login' element={<Login/>}/>
      <Route path='/signup' element={<SignUp/>}/>
      <Route path='/analyzer' element={<AnalyzerPage/>}/>
    </Routes>
    </BrowserRouter>
  )
}

export default App