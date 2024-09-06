import "./index.css";
import { useState } from "react";
import HeaderPage from "./components/layouts/header";
import SliderPage from "./components/layouts/slider";
import ContentPage from "./components/layouts/content";
function App() {
  const [result, setResult] = useState([])
  const [loading, setLoading] = useState(false)
  return (
    <div >
      <HeaderPage />
      <div className="fixed flex flex-row bg-[#f0d8e8] h-screen w-full">
        <SliderPage  setResult={setResult} setLoading={setLoading}/>
        <ContentPage result={result} loading={loading}/>
      </div>
    </div>
  );
}

export default App;

