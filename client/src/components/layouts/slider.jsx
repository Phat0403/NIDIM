import ImageQuery from "../inputs/imageQuery"
import RateNum from "../inputs/RateNum"
import TextQuery from "../inputs/textQuery"
import OcrQuery from "../inputs/ocrQuery"
import { useState } from "react"

const SliderPage = (props)=>{
    const { setResult, setLoading} = props
    const [rateNum, setRateNum] = useState(0); // 
    return(
        <div className="flex flex-col border shadow-[0_0px_30px_-15px_rgba(0,0,0,0.3)] bg-[#EDE8F5]  w-[420px] pl-4 mt-1 rounded-lg overflow-y-auto">
            <RateNum setRateNum={setRateNum} />
            <TextQuery  setResult={setResult}  setLoading={setLoading} rateNum={rateNum}/>
            <ImageQuery  setResult={setResult}  setLoading={setLoading} rateNum={rateNum}/>
            <ImageQuery  setResult={setResult}  setLoading={setLoading} rateNum={rateNum}/>
            <OcrQuery  setResult={setResult}  setLoading={setLoading} />
        </div>
    )
}
export default SliderPage